import json
import asyncio
from exchange.protos.order_book_pb2 import Order
from exchange.protos.service_pb2 import PlaceOrderResponse, ModifyOrderResponse, CancelOrderResponse

import src.utils as u

class Orders():
    def __init__(self, sens, name, asset):
        self.name = name
        self.asset = asset
        self.master = asset.master
        self.sens = sens
        self.typ = "bids" if sens == 1 else "asks"
        self.logger = u.log.classFilter(self, f"{name}_orders_{self.typ}")
        self.aorders = asset.orders
        self.lst = []
        self.cond = lambda i: i.h["quantity"] != 0 and not i.cancelled and i.h["order_type"] == 2
        self.modify_func = self.master.p["modify"]
        self.debug(self.modify_func)

    def order(self, ccy, p=0, q=0, add=0, lm="L"):
        t = self; m = t.master
        p = round((p or t.asset.best_price(t.sens)) + add, 2)
        nq = abs(m.sp.get("quantity") or 0) or 10
        if not q: return p
        allorders = t.get_live(); q = t.sens*abs(q)
        x = exist = allorders[0] if len(allorders) else 0 # will modify the first order if it exists
        o = {"price": p, "quantity": q, "order_type": lm, "name": t.name}
        exc = lambda: [x.modify_order, o] if exist else [t.place_order, o]
        if x and abs(x.h["price"] - o["price"])<0.02 and abs(q-x.h["qleft"])<abs(q/3): return p # nothing to do
        ccy.trades_to_execute.append(exc())
        return p

    def cancel_all(self, ccy):
        for o in self.get_live(): ccy.trades_to_execute.append([o.cancel_order])

    async def place_order(self, h):
        cls = SingleOrder(self); x = await cls.create(h)
        return u.push(self.lst, x) # returns a SingleOrder object if x is truthy

    def delete_order(self, o):
        o.deleted = self.master.num; self.lst = [i for i in self.lst if i != o]
        if not self.aorders.pop(o.oid): return self.error("order not found in orders, should be!", o.sid)
        return 1

    def lsth(self):
        return [i.h for i in self.lst if self.cond(i)]

    def order_at_price(self, p):
        a = [i for i in self.lst if self.cond(i) and i.h["price"] == p and i.h["num"] < self.master.num]
        return a[0] if len(a) else 0

    def get_live(self):
        # self.warning(self.lst)
        return [i for i in self.lst if self.cond(i) and not i.ishedge]


class SingleOrder():
    def __init__(self, all):
        self.logger = all.logger.thisClassLogger(self, all.logname)
        self.oklog = self.logger.ok(all.logname)
        self.all = all
        self.cancelled = 0
        self.quantity = 0
        self.filled = 0
        self.ishedge = 0
        self.aorders = all.aorders
        self.modified = ""
        self.modify_order = getattr(self, all.modify_func)

    def show(self, h={}): # just print for logs
        if not self.oklog: return "nothing" # we don't want to spend cpu time on json.dumps for nothing
        s = u.update({"p": self.h["price"], "q": self.h["quantity"], "r": self.h["qleft"]}, h)
        return f'{self.all.name}: {json.dumps(s)}'

    def fill(self, f):
        o = f.order; oid = o.order_id;
        op = round(f.fill_price,2); oq = round(f.filled_quantity * u.sign(o.quantity))
        if self.cancelled: self.warning("Sorry, cancelled order was filled:", self.show({"fill": oq}))

        def err(fv, typ, m): # check (well you never know....)
            msg = f'{self.all.name}: {m} {typ} when filling {self.sid}: {fv} vs {self.h[typ]} {self.h}'
            self.fatal(msg)
        diff_price = d = self.h["price"] - op if self.h["price"] else 0
        if d != 0 and d * self.all.sens < 0 : err(op, "price", "worse")
        if f.filled_quantity > abs(self.h["qleft"]): err(f.filled_quantity, 'quantity', 'too much')

        self.filled += oq; self.h["qleft"] -= oq
        self.h["size"] -= f.filled_quantity
        if self.h["size"] <= 0: self.mark_cancelled()
        self.debug(f"filled-{self.sid}", self.show())
        return self

    def make_order(self, h):
        h["quantity"] = int(round(h["quantity"], 0))
        h["qleft"] = h["quantity"]
        self.ishedge = h.get("ishedge")
        h["size"] = abs(h["quantity"])
        h["price"] = round(h["price"], 2) if h["price"] else None
        h["num"] = self.all.master.num
        default_ot = Order.ORDER_LMT; ot = h.get("order_type", 0)
        if ot == "M": ot = Order.ORDER_MKT
        if ot == "L": ot = Order.ORDER_LMT # =2
        h["order_type"] = default_ot if ot != Order.ORDER_MKT and ot != Order.ORDER_LMT else ot
        # self.error("make order", f'{h}')
        if ot == Order.ORDER_MKT: h["price"] = None
        if not h.get("alert", 0): h["alert"] = 0
        return Order(asset_code = self.all.name, quantity=h["quantity"], price = h["price"],
                 order_type = h["order_type"], competitor_identifier = self.all.master._comp_id)

    async def create(self, h):
        if self.all.sens * h["quantity"] <= 0: return None # quantity and sens must be the same
        o = self.make_order(h)
        resp = await self.all.master.place_order(o)
        if type(resp) != PlaceOrderResponse:
            return self.error("Error, NOT place_order", h, resp)
        self.created = h["created"] = h["num"]; self.filled = 0; self.h = h
        self.oid = h["order_id"] = resp.order_id; self.sid = self.oid[-6:].lower()
        self.aorders[self.oid] = self # keep a reference in orders
        self.debug(f"created-{self.sid}", self.show())
        return self

    async def real_modify_order(self, h):
        if self.all.sens * h["quantity"] <= 0: return None # quantity and sens must be the same
        temp = u.update({}, self.h, {"modified": self.all.master.num}, h)
        o = self.make_order(temp)
        resp = await self.all.master.modify_order(self.oid, o)
        if type(resp) != ModifyOrderResponse:
            return self.error("Could NOT modify_order", self.sid, f'(created:{self.created}, last modif:{self.modified})', temp, resp)
        self.h = temp; self.modified = self.h["modified"]
        self.debug(f"modified-{self.sid}", self.show())
        return self

    async def mock_modify_order(self, h):
        self.debug(f"mock_modify-{self.sid}", self.show(h))
        t1 = asyncio.create_task( self.cancel_order() )
        t2 = asyncio.create_task( self.all.place_order(h) )
        await t1
        if not t1.result(): return
        await t2; return t2.result()
        # x1 = await self.cancel_order()
        # return await self.all.place_order(h) if x1 else x1

    async def cancel_order(self):
        if self.cancelled: return
        resp = await self.all.master.cancel_order(self.oid)
        if type(resp) != CancelOrderResponse:
            return self.error("Could NOT cancel_order", self.sid, f'(created:{self.created}, last modif:{self.modified})', temp)
        self.mark_cancelled()
        self.debug(f"cancelled-{self.sid}", self.show())

    def mark_cancelled(self):
        self.all.asset.to_clean.append(self.oid)
        self.cancelled = self.all.master.num;  return self

    def delete(self):
        return self.all.delete_order(self)
