import random
import asyncio
import math
import importlib

import src.utils as u
from src.trader.Trader import Trader
from src.trader.Cycle import BaseCycle
from src.trader.Instrument import Instrument
from src.trader.Option import Option

class MarketMaker(Trader):
    def __init__(self, file=0):
        file = file or __file__
        self.traderCycle = TraderCycle
        Trader.__init__(self, file)

        c = self.c #init assets (=options or instruments)
        self.assets = {}
        for k,v in c["case1"].items(): self.assets[k] = Instrument(k, self, v) #changed instrument to option

        self.store = {} # if you want to store something across cycles
        self.fines_detail = {"max":0, "seconds":0, "val":0}
        self.watch = ["delta","vega"]
        self.fines = u.todict(self.watch, self.fines_detail)
        self.mult = lambda s, p: {"pnl":1, "price":1, "pos":1}.get(p, s["pos"])

        self.slowdown = 0 # for dev. in seconds. Artificially raises the time between each update
        self.pairs = {
            "QU": {"mean": -0.05  , "diff": 0.1},
            "NU": {"mean":  0.05  , "diff": 0.1},
            "NQ": {"mean":  0.1 , "diff": 0.1},
            "MV": {"mean":  -0.8 , "diff": 0.15},
            "MQ": {"mean": -0.075  , "diff": 0.1},
            "MN": {"mean": -0.15 , "diff": 0.15},
            "KU": {"mean":  -0.95 , "diff": 0.1},
            "KM": {"mean":  -0.8 , "diff": 0.1}
        }

class TraderCycle(BaseCycle):
    def __init__(self, master):
        BaseCycle.__init__(self, master)
        # self.trade = self.allspreads
    async def init_cycle(self):
        self.do_not_trade_more = 0
        self.traded = 0
    async def onFilled(self, asset, fill):
        return
    async def onMarketChange(self, asset):
        return

    def makeo(self, q, a):
        t = self; m = t.master
        cls = a.mbids if q>0 else a.masks
        h = {"order_type": "M", "quantity": q, "ishedge":1}
        t.trades_to_execute.append([cls.orders.place_order, h])

    async def christian(self): # this is stupid random trades.
        t = self; m = t.master
        # self.pairs = {
        #     "QU": {"mean": -0.05  , "diff": 0.1},
        #     "NU": {"mean":  0.05  , "diff": 0.1},
        #     "NQ": {"mean":  0.1 , "diff": 0.1},
        #     "MV": {"mean":  -0.8 , "diff": 0.15},
        #     "MQ": {"mean": -0.075  , "diff": 0.1},
        #     "MN": {"mean": -0.15 , "diff": 0.15},
        #     "KU": {"mean":  -0.95 , "diff": 0.1},
        #     "KM": {"mean":  -0.8 , "diff": 0.1}
        # }
        for k,v in m.pairs.items():
            a1 = t.assets[k[:1]]; a2=t.assets[k[-1:]]
            if not (a1.mbids.best != 0 and a2.mbids.best != 0 and a1.masks.best != 0 and a2.masks.best != 0): continue
            diff = a1.mid["price"] - a2.mid["price"]
            d1 = v["mean"] - v["diff"]*2/3
            d2 = v["mean"] + v["diff"]*2/3
            sens =  1 if diff < d1 else 0
            sens = -1 if diff > d2 else 0
            if not sens or v.get("sens") == sens:continue
            diff = round(diff,2)
            self.info(k, v, diff, d1, d2)
            self.info(k, diff, sens, a1.mbids.best, a2.mbids.best, a1.masks.best, a2.masks.best)
            q = 9*sens
            if v.get("sens"): q*=2
            self.makeo(q, a1); self.makeo(-q, a2)
            v["sens"] = sens

if __name__ == "__main__":
    print(f"=========== Serving on {u.MyAddr().local()} ===========")
    u.launch_server_async(MarketMaker)

"""
never get filled on modified orders ???
worse price: modify modifies the wrong side (or order)
make price even if missing price
    "host": "ec2-3-19-59-107.us-east-2.compute.amazonaws.com",
    "port": "80"

"""
