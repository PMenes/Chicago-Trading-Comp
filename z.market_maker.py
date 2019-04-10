import random
import json
import asyncio

import src.utils as u
from src.trader.Trader import Trader
from src.trader.Cycle import BaseCycle
from src.trader.Instrument import Instrument
from src.trader.Option import Option

class MarketMaker(Trader):
    def __init__(self, file=0):
        file = file or __file__
        Trader.__init__(self, file)

        #init assets (=options or instruments)
        c = self.c
        self.assets = {}
        self.assets[c["underlying"]] = Instrument(c["underlying"], self)
        for k,v in c["options"].items(): self.assets[k] = Option(k, self, v)

        # set strategy
        self.setStrategy({"paul": self.trade_paul, "christian": self.trade_christian, "random": self.trade_random})

        self.store = {} # if you want to store something across cycles
        self.fines_detail = {"max":0, "seconds":0, "val":0}
        self.watch = ["delta","vega"]
        self.fines = u.todict(self.watch, self.fines_detail)
        self.mult = lambda s, p: {"pnl":1, "price":1, "pos":1}.get(p, s["pos"])

        self.slowdown = 0 # in seconds. Artificially raises the time between each update

        # # set logging filters (for development)
        # self.logger.accept("main")
        # self.logger.accept("perf")
        self.logger.accept("C100PHX_orders")
        self.logger.accept("C100PHX")
        self.logger.setFilter(1,1) # filter BOTH console AND file
        # self.logger.accept("C98PHX_orders")

class Cycle(BaseCycle):
    def __init__(self, master):
        BaseCycle.__init__(self, master)
        self.trade = self.master.strategy.trade

    async def init_cycle(self):
        self.do_not_trade_more = 0
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
            self.warning("over vega:", "vega=",self.prep["vega"], "delta=",self.prep["delta"])
            v = u.sign( self.prep["vega"] )
            for t in self.prep["trades"]:
                s = self.assets[t["name"]].status; q = t["quantity"]
                if u.sign(s["vega"] * q) != v:
                    t["quantity"] *= 2; self.prep["delta"] += q*s["delta"]

        n="IDX#PHX"; a = self.assets[n]; th = to_hedge = self.prep["delta"] # +a.status["pos"]
        if abs(to_hedge)>self.c["limits"]["delta"]: # if we will be over limits delta, hedge it
            self.warning("over delta:", "vega=",round(self.prep["vega"]), "delta=",round(th))
            q = round( -th, 0); sens = u.sign(q)
            cls = a.mbids if q>0 else a.masks
            # px = cls.lst[0]["price"]+sens*0.01 # better order, wait to be hit
            px = (a.masks if q>0 else a.mbids).lst[0]["price"] # cross the spread
            self.prep["trades"].append( {"name":n, "price":px, "quantity": q, "live": 1} )

        self.perf.step("prepared")
        await self.bulk_trades(self.prep["trades"])
        # await u.concurrent_tasks(self.prep["trades"], self.execute_trade)
        # tasks = []
        # for o in self.prep["trades"]: tasks.append( asyncio.create_task( self.execute_trade(o) ))
        # for t in tasks: await t
        self.traded = 1

    def prepare_trade(self, order, repo, force_mod=False): # clsOrders: obids or oasks, order {"price":x,"quantity":y}
        o = order; a = self.assets[o["name"]]; cls = a.obids if o["quantity"] > 0 else a.oasks
        if not order["live"]: return [repo.append([i.cancel_order]) for i in cls.lst]
        all = cls.get_live()
        x = exist = all[0] if len(all) else 0 # will modify the first order if it exists
        def exc(): repo.append([x.modify_order, o] if exist else [cls.place_order, o])
        if force_mod: exc()
        return 0 if (x and abs(x.h["price"] - o["price"])<0.02) or not o["price"] or not o["quantity"] else exc()

    async def bulk_trades(self, trades):
        # await u.concurrent_tasks(trades, self.execute_trade)
        # return

        repo = []; await asyncio.sleep(self.rtt/2)
        for t in trades: self.prepare_trade(t, repo)
        for e in repo:
            await asyncio.sleep(0.01)
            fn = e.pop(0)
            await fn(*e)

        # repo = []; tasks = []; await asyncio.sleep(self.rtt/2)
        # for t in trades: self.prepare_trade(t, repo)
        # async def new_trade(e, i):
        #     await asyncio.sleep(0.001*i)
        #     fn = e.pop(0)
        #     await fn(*e)
        # for e,i in repo:
        #     tasks.append(asyncio.create_task(new_trade(e, i)))
        # for t in tasks: await t



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
price changes
make price even if missing price
    "host": "ec2-3-19-59-107.us-east-2.compute.amazonaws.com",
    "port": "80"

"""
