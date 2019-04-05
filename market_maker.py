import random
import json
import asyncio

import src.utils as u
from src.trader.Trader import Trader
from src.trader.Instrument import Instrument
from src.trader.Option import Option

class MarketMaker(Trader):
    def __init__(self, file=0):
        file = file or __file__
        Trader.__init__(self, file)

        #init assets (=options or instruments)
        c = self.c
        self.assets = {c["underlying"]: Instrument(c["underlying"], self)}
        for k,v in c["options"].items(): self.assets[k] = Option(k, self, v)

        self.store = {} # if you want to store something across cycles
        self.every = 1 # ex: 2 will send only 1 out of 2 updates to the distributor

        # # set logging filters (for development)
        # self.logger.accept("main")
        # self.logger.accept("perf")
        # self.logger.accept("orders")
        # self.logger.accept("C98PHX_orders")

    async def init_update(self):
        self.do_not_trade_more = 0
        self.watch = ["delta","vega"]
        self.slowdown = 0 # in seconds. Artificially raises the time between each update
        self.traded = 0
        # self.debug("New Update:", self.num)

    async def onFilled(self, asset, fill):
        # self.debug("got filled", asset.name, fill)
        return

    async def onMarketChange(self, asset):
        return

    async def trade_christian(self):
        if self.traded: return
        for k in self.watch: self.prep[k] = self.pos_updated[k] # init with current delta and vega
        q = self.sp["quantity"]
        for k,a in self.assets.items(): # get trade options first
            if a.name[:3] == "IDX": continue
            self.get_spread(a, abs(q))

        # self.warning("result:", "vega=",self.prep["vega"], "delta=",self.prep["delta"])

        if abs(self.prep["vega"])>self.c["limits"]["vega"]: # if we will be over limits vega, increase size of "good" trades
            # self.warning("over1:", "vega=",self.prep["vega"], "delta=",self.prep["delta"])
            v = u.sign( self.prep["vega"] )
            for t in self.prep["trades"]:
                s = self.assets[t["name"]].status; q = t["quantity"]
                if u.sign(s["vega"] * q) != v:
                    t["quantity"] *= 2; self.prep["delta"] += q*s["delta"]

            # self.warning("over2:", "vega=",self.prep["vega"], "delta=",self.prep["delta"])

        n="IDX#PHX"; a = self.assets[n]; th = to_hedge = self.prep["delta"]+a.status["pos"]
        if abs(to_hedge)>self.c["limits"]["delta"]: # if we will be over limits delta, hedge it
            self.warning("over delta:", "vega=",round(self.prep["vega"]), "delta=",round(th))
            q = round( -th, 0); sens = u.sign(q)
            cls = a.mbids if q>0 else a.masks
            # px = cls.lst[0]["price"]+sens*0.01 # better order, wait to be hit
            px = (a.masks if q>0 else a.mbids).lst[0]["price"] # cross the spread
            self.prep["trades"].append( {"name":n, "price":px, "quantity": q, "live": 1} )


    # task1 = asyncio.create_task(
    #     say_after(1, 'hello'))
    #
    # task2 = asyncio.create_task(
    #     say_after(2, 'world'))
    #
    # print(f"started at {time.strftime('%X')}")
    #
    # # Wait until both tasks are completed (should take
    # # around 2 seconds.)
    # await task1
    # await task2
        self.perf.step("prepared")
        tasks = []
        for o in self.prep["trades"]: tasks.append( asyncio.create_task( self.execute_trade(o) ))
        for t in tasks: await t
        self.traded = 1

    async def trade_paul(self):
        # your idea is to trade only on assets which would hedge BOTH our global vega and delta. Let's do that
        bound = self.sp["bound"]; q = quantity = self.sp["quantity"]; pu = self.pos_updated
        # if no match with you criteria, only trade random (otherwise there is never anything to hedge....)
        if not (abs(pu["delta"])> bound/2 and abs(pu["vega"]) > bound/4): return await self.trade_default(q*5)
        for k,a in self.assets.items(): # trade options first
            if a.name[:3] == "IDX": continue # underlying
            s = a.status
            x = "delta"; d = delta_will_be_better_if_buy = 1 if abs(pu[x] + s[x]) < abs(pu[x] - s[x]) else -1
            x = "vega";  v = vega_will_be_better_if_buy  = 1 if abs(pu[x] + s[x]) < abs(pu[x] - s[x]) else -1
            if abs(d+v) != 2: continue # we only want to trade options that will hedge BOTH our global delta and vega
            self.warning(f'delta={round(pu["delta"],1)} vega={round(pu["vega"],1)} {"sell" if d<0 else "buy"}ing {a.name}')
            await self.best_order(a, u.sign(d) * q)

    async def trade_random(self, q=0): # this is stupid random trades.
        q = q or self.sp["quantity"]
        if random.random() < 0.5: # only trade 25% (0.5*0.5) of the time
            for k,a in self.assets.items(): # place new orders
                if random.random() < 0.5: continue # cancel half the time
                await self.best_order(a, u.sign(random.random()-0.49) * (abs(q) or 1), "L")

if __name__ == "__main__":
    print(f"=========== Serving on {u.MyAddr().local()} ===========")
    u.launch_server_async(MarketMaker)

"""

"""
