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
        p = (p or self.asset.best_price(self.sens)) + add
        if not q: return p
        allorders = self.get_live()
        x = exist = allorders[0] if len(allorders) else 0 # will modify the first order if it exists
        o = {"name":self.name, "price": p, "quantity": self.sens*abs(q), "order_type": lm}
        exc = lambda: [x.modify_order, o] if exist else [self.place_order, o]
        if x and abs(x.h["price"] - o["price"])<0.02: return p # nothing to do
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
        return [i for i in self.lst if self.cond(i)]


class SingleOrder():
    def __init__(self, all):
        self.logger = all.logger.thisClassLogger(self, all.logname)
        self.oklog = self.logger.ok(all.logname)
        self.all = all
        self.cancelled = 0
        self.quantity = 0
        self.filled = 0
        self.aorders = all.aorders
        # self.awo = all.awo
        self.modified = ""
        # self.kwo = lambda: f'{self.all.name}_{self.h["price"] or 0}_{self.h["quantity"]}'
        self.modify_order = getattr(self, all.modify_func)


    def show(self, h={}):
        if not self.oklog: return "nothing" # we don't want to spend cpu time on json.dumps for nothing
        s = u.update({"q": self.h["quantity"], "p": self.h["price"], "id": self.sid}, h)
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
        if self.h["qleft"] <= 0: self.mark_cancelled()
        # self.info("filled ", self.show({"this_fill": oq, "total_filled": self.filled}))
        return self

    def make_order(self, h):
        h["quantity"] = int(round(h["quantity"], 0))
        h["qleft"] = h["quantity"]
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
        # if self.all.name != "C100PHX": return
        if self.all.sens * h["quantity"] <= 0: return None # quantity and sens must be the same
        o = self.make_order(h)
        resp = await self.all.master.place_order(o)
        if type(resp) != PlaceOrderResponse:
            return self.error("Error, NOT place_order", h, resp)
        self.created = h["created"] = h["num"]; self.filled = 0; self.h = h
        self.oid = h["order_id"] = resp.order_id; self.sid = self.oid[-6:].lower()
        self.aorders[self.oid] = self # keep a reference in orders
        # self.awo[self.kwo()] = {"oid":self.oid, "num":self.created}
        self.debug("created", self.show())
        return self

    async def real_modify_order(self, h):
        # self.warning("REAL_modify..", self.show(h))
        if self.all.sens * h["quantity"] <= 0: return None # quantity and sens must be the same
        temp = u.update({}, self.h, {"modified": self.all.master.num}, h)
        o = self.make_order(temp)
        resp = await self.all.master.modify_order(self.oid, o)
        if type(resp) != ModifyOrderResponse:
            return self.error("Could NOT modify_order", self.sid, f'(created:{self.created}, last modif:{self.modified})', temp, resp)
        self.h = temp; self.modified = self.h["modified"]
        # self.awo[self.kwo()] = {"oid":self.oid, "num":self.modified}
        self.debug("modified", self.show())
        return self

    async def mock_modify_order(self, h):
        self.debug("mock_modify..", self.show(h))
        t1 = asyncio.create_task( self.cancel_order() )
        t2 = asyncio.create_task( self.all.place_order(h) )
        await t1
        if not t1.result(): return
        await t2; return t2.result()

    async def cancel_order(self):
        if self.cancelled: return
        resp = await self.all.master.cancel_order(self.oid)
        if type(resp) != CancelOrderResponse:
            return self.error("Could NOT cancel_order", self.sid, f'(created:{self.created}, last modif:{self.modified})', temp)
        self.mark_cancelled()
        self.debug("cancelled", self.show())

    def mark_cancelled(self):
        self.all.asset.to_clean.append(self.oid)
        # self.awo.pop(self.kwo(), 0)
        self.cancelled = self.all.master.num;  return self

    def delete(self):
        return self.all.delete_order(self)
