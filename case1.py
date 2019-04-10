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

        # init assets (=options or instruments)
        c = self.c
        # self.assets = {c["underlying"]: Instrument(c["underlying"], self)}
        # for k,v in c["options"].items(): self.assets[k] = Option(k, self, v)
        self.assets = {}
        for k,v in c["case1"].items(): self.assets[k] = Instrument(k, self, v)

        self.store = {} # if you want to store something across cycles
        self.every = 1 # ex: 2 will send only 1 out of 2 updates to the distributor
        self.fines = u.todict(["one"], self.fines_detail)

        # set logging filters (for development)
        self.logger.accept("main")
        # self.logger.accept("perf")
        self.logger.accept("orders")
        self.logger.accept("K_orders")

    async def init_update(self):
        self.do_not_trade_more = 0
        self.watch = ["one"]
        self.slowdown = 0 # in seconds. Artificially raises the time between each update
        self.traded = 0
        # self.debug("New Update:", self.num)

    async def onFilled(self, asset, fill):
        # self.debug("got filled", asset.name, fill)
        return

    async def onMarketChange(self, asset):
        return

    async def trade_christian(self):
        """
        given the rules, we have to trade so that it is IMPOSSIBLE to be over limits
        """
        self.fatal("pos====", self.pos_updated["pos"])
        pos = self.pos_updated["pos"]; sens = u.sign(pos); apos=abs(pos)
        bid_size = int((self.c["limits-fined"]["one"] - pos)/6)
        ask_size = int((-self.c["limits-fined"]["one"] - pos)/6)
        self.fatal("bid=", bid_size, "ask=", ask_size)
        tasks = []
        for k,a in self.assets.items(): # get trade options first
            for q in [bid_size, ask_size]:
                tasks.append( asyncio.create_task(self.best_order(a, q, force_mod=True)))
        for t in tasks: await t

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
