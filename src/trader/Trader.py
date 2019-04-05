import random
import json
import asyncio

from exchange.protos.order_book_pb2 import Order
from exchange.protos.service_pb2 import PlaceOrderResponse

import src.utils as u
from src.trader.client_send import SendExchangeGrpcClient
# from src.trader.Trades import Trades

class Trader(SendExchangeGrpcClient):
    def __init__(self, file):
        SendExchangeGrpcClient.__init__(self, file)
        self.perf = u.Perf(0, self.logger)

        # set strategy and its parameters
        self.sp = {}; s = self.p["strategies"]; ms=self.p.get("strategy")
        u.update(self.sp, s["random"], s.get(ms))
        all = {"paul": self.trade_paul, "christian": self.trade_christian, "random": self.trade_random}
        print(self.sp)
        self.sp["proc"] = all.get(ms) or self.error(f"Sorry, can't find strategy '{s}'")

        self.every = 1
        self.pos_updated = {"delta":0,"gamma":0,"vega":0, "one": 0}


    # =====================================================================
    # =====================================================================
    # ======= these are the 3 functions specific to each trader ===========
    # ================ maybe_chock, protect, trade ========================
    # =================== you should define your own ======================
    # =====================================================================
    # =====================================================================

    async def init_update(self):
        return

    async def maybe_chock(self, greeks="old", market="old"): # "updated" or "old"(=greeks or market from previous update)
        return

    async def onFilled(self, asset, fill):
        return

    async def onMarketChange(self, asset):
        return

    async def trade(self):
        return

    # =====================================================================
    # =====================================================================
    # === you normally don't have to touch the following functions ========
    # =====================================================================
    # =====================================================================
    async def trade(self):
        await self.sp["proc"]() # apply the strategy set in config.jon. See __init__ for self.sp dict

    async def best_order(self, a, q, lm=0, better=0):
        better = better or self.sp["better"]
        sens = u.sign(q); cls = a.mbids if sens > 0 else a.masks
        p = cls.best_price()
        if not p: return {"price": 0} # there is no market price if best_price is 0
        return await self.execute_trade({"name":a.name, "price": p + sens*better, "quantity": q, "order_type": lm, "live": 1})

    async def execute_trade(self, order): # clsOrders: obids or oasks, order {"price":x,"quantity":y}
        o = order; a = self.assets[o["name"]]; cls = a.obids if o["quantity"] > 0 else a.oasks
        if not order["live"]: return [i.cancel_order() for i in cls.lst]
        all = cls.get_live()
        x = exist = all[0] if len(all) else 0 # will modify the first order if it exists
        if (x and abs(x.h["price"] - o["price"])<0.02) or not o["price"] or not o["quantity"]: return
        return await x.mock_modify_order(o) if exist else await cls.place_order(o)

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
            live = 0 if abs(p) > 50 and cls.sens == u.sign(p) else 1
            for k in ["delta","vega"]: self.prep[k] += cls.sens*q * self.assets[cls.name].status[k] # greeks if/after filled
            self.prep["trades"].append( {"name":cls.name, "price":price, "quantity": cls.sens*q, "live": live} )

    async def send_exchange_updates(self, num, upd):
        # if num > 11: return


        self.alerts = []; self.info = ''; self.meta = {} # reset alerts, info
        a = self.assets; perf = self.perf; self.num = num # ..meta, perf, num
        self.logger.setPrefix(format(num, "04d")) # logger prefix = new num
        perf.reset(num) # keep track of time and performance.

        await self.init_update() # all reset, user specific init

        x = upd.competitor_metadata
        self.meta["pnl"] = x.pnl; self.meta["fines"] = x.fines

        fills = {}; self.pos_dirty = self.pos_updated
        for f in upd.fills: # first handle any fills
            ast = f.order.asset_code; s = self.assets[ast].status
            if not fills.get(ast, 0): fills[ast] = {"bids":[], "asks":[]} # prepare the fills dict
            o = await a[ast].add_fill(f, fills[ast]) # add the fill
            for p in self.pos_dirty.keys(): self.pos_dirty[p] += s[p] * s["pos"] # recalc dirty pos
            await self.onFilled(self.assets[ast], o) # trigger onFilled
        perf.step("fills")

        # here we could immediately check if position
        #   has gone our way (or not!) after the fills: not done
        await self.maybe_chock()
        perf.step("chock 1")

        for u in upd.market_updates: # then markets, we need it to get underlying
            self.debug(u.asset.asset_code) # update bids and asks

        for u in upd.market_updates: # then markets, we need it to get underlying
            m = a[u.asset.asset_code] # update bids and asks
            m.mbids.update(u.bids); m.masks.update(u.asks)
            m.set_mid(u.mid_market_price) # set mid price
            await self.onMarketChange(m) # trigger onMarketChange
        perf.step("market")

        # here we check if chock BEFORE RECALCULATING OPTIONS (which is 5 ms)
        await self.maybe_chock(market="updated")
        perf.step("chock 2")

        self.pos_updated = self.pos = {"delta":0,"gamma":0,"vega":0, "one":0}
        for k in a: # update options, recalc iv and greeks
            a[k].update_status()
            for p in self.pos.keys(): self.pos[p] += a[k].status[p] * a[k].status["pos"]
        perf.step("options")

        await self.trade() # trade !!
        perf.step("traded")

        for k in a:  a[k].clean_cancelled(num) # cleaning cancelled orders

        await self.distribute(fills) # send status to distributor (for web)
        perf.step("send")
        perf.step("ALL", perf.reft)


    # normally, don't touch it
    async def distribute(self, fills):
        if not len(self.p["connect_to"]) or not self.num % int(self.every) == 0: return

        snd = {"action": "newMsg", "cycles": self.num, "info":self.info, "meta": self.meta, "assets":{}, "perf": self.perf.steps}
        for k,a in self.assets.items(): # send all assets
            snd["assets"][k] = {
                "status": a.status,
                "market": { "bids": a.mbids.lst, "asks": a.masks.lst},
                "orders": { "bids": a.obids.lsth(), "asks": a.oasks.lsth()},
                "fills": fills.get(k, { "bids": [], "asks": [] })
            }

        try:
            dist = self.p["connect_to"][0]
            await self.connections[dist]["ws"].send_json(snd, False)
        except Exception as e:
            print("Error sending", e)


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
