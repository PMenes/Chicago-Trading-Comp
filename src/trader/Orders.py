import json
import asyncio
from exchange.protos.order_book_pb2 import Order
from exchange.protos.service_pb2 import PlaceOrderResponse, ModifyOrderResponse

import src.utils as u

class Orders():
    def __init__(self, sens, name, master):
        self.sens = sens
        self.typ = "bids" if sens == 1 else "asks"
        self.logname = f"{name}_orders_{self.typ}"
        self.logger = master.logger.thisClassLogger(self)
        self.name = name
        self.master = master
        self.lst = []

    async def place_order(self, h):
        cls = SingleOrder(self); x = await cls.create(h)
        return u.push(self.lst, x) # returns a SingleOrder object if x is truthy

    def delete_order(self, o):
        x = o.cancelled and o.cancelled < self.master.num -1
        if x:
            self.lst = [i for i in self.lst if i != o]
            self.master.assets[self.name].orders.pop(o.oid, None)
        return x

    def lsth(self):
        return [i.h for i in self.lst if i.h["quantity"] != 0 and not i.cancelled]

    def order_at_price(self, p):
        for o in self.lst:
            if not o.cancelled and o.h["price"] == p and o.h["num"] < self.master.num: return o
        return 0

    def get_live(self):
        return [i for i in self.lst if i.h["quantity"] != 0 and not i.cancelled]


class SingleOrder():
    def __init__(self, all):
        self.logger = all.logger.thisClassLogger(self, all.logname)
        self.oklog = self.logger.ok(all.logname)
        self.all = all
        self.cancelled = 0
        self.quantity = 0
        self.filled = 0
        self.rtt = self.all.master.rtt

    def show(self, h={}):
        if not self.oklog: return "nothing" # we don't want to spend cpu time on json.dumps for nothing
        s = u.update({"q": self.h["quantity"], "p": self.h["price"], "id": self.oid[-6:].lower()}, h)
        return f'{self.all.name}: {json.dumps(s)}'

    def make_order(self, h):
        h["quantity"] = int(round(h["quantity"], 0))
        h["size"] = abs(h["quantity"])
        h["price"] = round(h["price"], 2)
        h["num"] = self.all.master.num
        default_ot = Order.ORDER_MKT; ot = h.get("order_type", 0)
        if ot == "M": ot = Order.ORDER_MKT
        if ot == "L": ot = Order.ORDER_LMT
        h["order_type"] = default_ot if ot != Order.ORDER_MKT and ot != Order.ORDER_LMT else ot
        if not h.get("alert", 0): h["alert"] = 0
        return Order(asset_code = self.all.name, quantity=h["quantity"], price = h["price"],
                 order_type = h["order_type"], competitor_identifier = self.all.master._comp_id)

    def fill(self, f, fills):
        o = f.order; oid = o.order_id; hq=self.h["quantity"]
        q = round(self.all.sens * f.filled_quantity) # signed quantity
        if self.cancelled: self.warning("Sorry, cancelled order filled:", self.show({"fill": q}))
        u.push(self.all.master.alerts, self.h["alert"]) # take care of alerts !!!

        def err(fv, typ, m): # check (well you never know....)
            msg = f'current={self.all.master.num}, ${self.all.name}: {m} {typ} when filling {self.oid}: {fv} vs {self.h[typ]} {self.h}'
            u.makerr( ValueError, self.logger, msg)
        if round(o.price,2) != self.h["price"] and self.h["num"]<self.all.master.num-1: err(o.price, "price", "not same")
        if f.filled_quantity > abs(hq): err(f.filled_quantity, 'quantity', 'too much')

        self.filled += q; self.lastfill = q
        dist = {"price":o.price, "size":abs(q), "quantity":q, "alert": self.h["alert"]}
        fills[self.all.typ].append(dist)
        self.h["quantity"] -= q; self.h["size"] -= f.filled_quantity
        if self.h["quantity"] <= 0: self.all.delete_order(self)
        self.info("filled ", self.show({"this_fill": q, "total_filled": self.filled}))
        return self

    async def create(self, h):
        if self.all.sens * h["quantity"] < 0: return None # quantity and sens must be the same
        o = self.make_order(h)
        await asyncio.sleep(self.rtt/2)
        resp = await self.all.master.place_order(o)
        await asyncio.sleep(self.rtt/2)
        if type(resp) != PlaceOrderResponse:
            u.makerr(ValueError, self.logger,"Error, could NOT place_order", resp, h); return
        self.oid = h["order_id"] = resp.order_id; self.filled = 0; self.h = h
        self.all.master.assets[self.all.name].orders[self.oid] = self
        self.debug("created", self.show())
        return self

    async def modify_order(self, h):
        if not h.get("alert", 0): h["alert"] = 0 # reset alert
        u.update(self.h, {"ori": self.h["num"], "oripx": self.h["price"]}, h)
        o = self.make_order(self.h)
        resp = await self.all.master.modify_order(self.oid, o)
        if type(resp) != ModifyOrderResponse:
            log.warning("Error, could NOT modify_order, mocking", resp, h)
            return await self.mock_modify_order(h)
        self.debug("modified", self.show())
        return self

    async def mock_modify_order(self, h):
        self.debug("mock_modify..", self.show(h))
        t1 = asyncio.create_task( self.cancel_order() )
        t2 = asyncio.create_task( self.all.place_order(h) )
        await t1; await t2
        return t2.result()
        # x = await self.cancel_order()
        # return await self.all.place_order(h) if x else 0

    async def cancel_order(self):
        if self.cancelled: return
        await asyncio.sleep(self.rtt/2)
        resp = await self.all.master.cancel_order(self.oid)
        await asyncio.sleep(self.rtt/2)
        if not resp.success: return self.warning("Error, could NOT cancel order", self.oid)
        self.debug("cancelled", self.show())
        self.all.master.assets[self.all.name].to_clean.append(self.oid)
        self.cancelled = self.all.master.num;  return self

    def delete(self):
        return self.all.delete_order(self)
