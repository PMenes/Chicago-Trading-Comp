import random
import json
import asyncio

from exchange.protos.order_book_pb2 import Order
from exchange.protos.service_pb2 import PlaceOrderResponse

import src.utils as u
from src.trader.client_send import SendExchangeGrpcClient
from src.trader.Instrument import Instrument

class Trader(SendExchangeGrpcClient):
    def __init__(self, file):
        SendExchangeGrpcClient.__init__(self, file)
        self.perf = u.Perf(0, self.logger)

        s=self.p["strategies"]; self.sp = u.update({}, s["random"], s.get(self.p.get("strategy")))

        self.pos_updated = Instrument.status0.copy()
        self.pos_model = self.pos_updated.copy()

        self.trades = 0; self.volume = 0
        self.mult = lambda s, p: {"pnl":1, "price":1, "pos":1}.get(p, s["pos"])
        self.fines_detail = {"max":0, "seconds":0, "val":0}

    # =====================================================================
    # =====================================================================
    # === you normally don't have to touch the following functions ========
    # =====================================================================
    # =====================================================================

    def best_order(self, a, q, name="standing", lm="L", add=None, better=None, force_mod=False):
        if not q: return
        sens = u.sign(q); mcls = a.mbids if sens > 0 else a.masks; ocls = mcls.orders
        if lm == "M": return [ocls.place_order, {"name":a.name, "quantity": q, "order_type": lm}]

        p = mcls.best_price()
        if not p: return # there is no market price if best_price is 0
        better = better if better != None else (self.sp["better"] or 0.01)
        pa = p+add if add != None else p + sens*better
        o = {"name":a.name, "price": pa, "quantity": q, "order_type": lm}
        allorders = ocls.get_live()
        x = exist = allorders[0] if len(allorders) else 0 # will modify the first order if it exists
        exc = lambda: [x.mock_modify_order, o] if exist else [ocls.place_order, o]
        return 0 if (x and abs(x.h["price"] - o["price"])<0.02) else exc()

    async def best_order1(self, a, q, lm=0, better=0, force_mod=False):
        better = better or self.sp["better"]
        sens = u.sign(q); cls = a.mbids if sens > 0 else a.masks
        p = cls.best_price()
        if not p: return {"price": 0} # there is no market price if best_price is 0
        h = {"name":a.name, "price": p + sens*better, "quantity": q, "order_type": lm, "live": 1}
        self.debug("trading:", h)
        return await self.execute_trade(h, force_mod)

    async def execute_trade(self, order, force_mod=False): # clsOrders: obids or oasks, order {"price":x,"quantity":y}
        o = order; a = self.assets[o["name"]]; cls = a.obids if o["quantity"] > 0 else a.oasks
        if not order["live"]: return await u.concurrent_tasks([u.act(i.cancel_order()) for i in cls.lst])
        all = cls.get_live()
        x = exist = all[0] if len(all) else 0 # will modify the first order if it exists
        async def exc(): await x.modify_order(o) if exist else await cls.place_order(o)
        if force_mod: await exc()
        return 0 if (x and abs(x.h["price"] - o["price"])<0.02) or not o["price"] or not o["quantity"] else await exc()

    def get_spread(self, a, q=5, bias=0, spread_size=0.5, better=0):
        better = better or self.sp["better"]
        p = a.status["pos"]; q=abs(q)
        if not bias: bias = -p or q*u.sign(random.random()-0.49) # slight buy bias (:
        get = lambda cls,i: cls.lst[i]["price"] if len(cls.lst)-i>0 else 0
        if not get(a.mbids, 0) or not get(a.masks, 0): return # get_out if no bid or no ask !
        wbid, wask = [a.mbids.lst[-1]["price"] - better, a.masks.lst[-1]["price"] + better]
        for cls in [a.mbids, a.masks]:
            price = get(cls, 0) + better * min(1, bias / q) # increase with position
            price = u.between(wbid, price, wask)
            live = 0 if abs(p) > 3*q and cls.sens == u.sign(p) else 1
            for k in self.watch: self.prep[k] += cls.sens*q * self.assets[cls.name].status[k] # greeks if/after filled
            self.prep["trades"].append( {"name":cls.name, "price":price, "quantity": cls.sens*q, "live": live} )

    # async def send_exchange_updates(self, num, upd):
    #     # if num > 11: return
    #     a = self.assets; perf = self.perf
    #     def prepare(force=0):
    #         if not force and self.prepared : return
    #         self.alerts = []; self.fills = {}
    #         self.prep = {"trades": []}; self.watch = []; self.meta = {}
    #         self.pos_updated = self.pos_updated or u.update({}, Instrument.status0)
    #         self.save_pu = u.update({}, self.pos_updated) # calculate fines later
    #         for k,v in a.items(): self.fills[k] = {"bids":[], "asks":[]} # prepare the fills dict
    #         self.fills_to_clean = []
    #         self.prepared = 1
    #
    #     prepare()
    #     self.finished = 0
    #     self.num = num; perf.reset(num) # keep track of time and performance.
    #     self.logger.setPrefix(format(num, "05d")) # logger prefix = new num
    #
    #     await self.init_update() # all reset, user specific init
    #
    #     self.trades += len(upd.fills); h = self.meta = {}; x = upd.competitor_metadata
    #     h["pnl"] = x.pnl; h["fines"] = x.fines; h["cycles"] = num; h["trades"] = self.trades
    #
    #     self.pos_dirty = self.pos_updated
    #     for f in upd.fills: # first handle any fills
    #         ast = f.order.asset_code; s = self.assets[ast].status
    #         # fills[ast] = fills.get(ast, {"bids":[], "asks":[]})  # prepare the fills dict
    #         o = await a[ast].add_fill(f) # add the fill
    #         for p in self.pos_dirty.keys(): self.pos_dirty[p] += s[p] * self.mult(s, p) # recalc dirty pos
    #         await self.onFilled(self.assets[ast], o) # trigger onFilled
    #     perf.step("fills")
    #
    #     # here we could immediately check if position
    #     #   has gone our way (or not!) after the fills: not done
    #     await self.maybe_chock()
    #     perf.step("chock 1")
    #
    #     for x in upd.market_updates: # then markets, we need it to get underlying
    #         m = a[x.asset.asset_code] # update bids and asks
    #         m.mbids.update(x.bids); m.masks.update(x.asks)
    #         m.set_mid(x.mid_market_price) # set mid price
    #         await self.onMarketChange(m) # trigger onMarketChange
    #     perf.step("market")
    #
    #     # here we check if chock BEFORE RECALCULATING OPTIONS (which is 5 ms)
    #     await self.maybe_chock(market="updated")
    #     perf.step("chock 2")
    #
    #     # self.pos_updated = self.pos = {"delta":0,"gamma":0,"vega":0, "one":0}
    #     self.pos_updated = self.pos = u.update({}, Instrument.status0)
    #     for k in a: # update options, recalc iv and greeks
    #         a[k].update_status()
    #         # for p in self.pos_dirty.keys(): self.pos_dirty[p] += s[p] * self.mult(s, p) # recalc dirty pos
    #         for p in self.pos.keys(): self.pos[p] += a[k].status[p] * self.mult(a[k].status, p)
    #     perf.step("options")
    #
    #     await self.trade() # trade !!
    #     perf.step("traded")
    #
    #     for k in self.fines: # calcultate fines
    #         if abs(self.save_pu[k]) > self.c["limits-fined"][k]:
    #             h = self.fines[k]
    #             secs = 0.5 # assume 2 cycles every second
    #             h["val"] -= 0.01 * (abs(self.save_pu[k]) - self.c["limits-fined"][k])**2 * secs
    #             h["seconds"] += secs
    #             h["max"] = abs(self.save_pu[k]) if abs(self.save_pu[k]) > h["max"] else h["max"]
    #
    #     for k,v in a.items(): v.clean_cancelled(num) # cleaning cancelled orders
    #
    #     for f in self.fills_to_clean: a[f.order.asset_code].clean_dirty_fills(f) # clean dirty fills
    #
    #     perf.step("clean")
    #
    #     await self.distribute() # send status to distributor (for web)
    #     perf.step("send")
    #     perf.step("ALL", perf.reft)
    #     upd=0; prepare(1)
    #     self.finished = 1
    #
    #
    # # normally, don't touch it
    # async def distribute(self):
    #     if not len(self.p["connect_to"]) or not self.num % int(self.every) == 0: return
    #
    #     snd = {"action": "newMsg", "gpos": self.pos, "assets":{}, "perf": self.perf.steps}
    #     for k in "fines,meta".split(","): snd[k] = getattr(self, k)
    #     for k,a in self.assets.items(): # send all assets
    #         snd["assets"][k] = {
    #             "status": a.status,
    #             "market": { "bids": a.mbids.lst, "asks": a.masks.lst},
    #             "orders": { "bids": a.obids.lsth(), "asks": a.oasks.lsth()},
    #             "fills": self.fills
    #         }
    #
    #     try:
    #         dist = self.p["connect_to"][0]
    #         await self.connections[dist]["ws"].send_json(snd, False)
    #         snd=0
    #     except Exception as e:
    #         self.error("Error sending", e)


    async def handle_recvd(self, msg, origin):
        """
        Where we receive messages from cooperating computers
        Not used for the moment, because with only 10 options, shipping away
        computing is not worth is: it cost 2 to 4 ms round trip time, and the
        most heavy option computing (for 10 options) is only 3ms.

        But obviously, in real markets there are many more options than 10, so you
        could not calculate on one cpu only and would need to offload processing.
        """
        rcd = json.loads(msg.data)
