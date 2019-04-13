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
        u.delfile(f'.logs/mas.txt')

        self.pairs = {
            "KM":{"avg":-0.85},
            "KN":{"avg":-0.96},
            "MN":{"avg":-0.11},
            "KQ":{"avg":-0.84},
            "KU":{"avg":-0.90},
            "MQ":{"avg":0.01},
            "NQ":{"avg":0.12},
            "MU":{"avg":-0.05},
            "NU":{"avg":0.06},
            "QU":{"avg":-0.06},
            "KV":{"avg":-1.74},
            "MV":{"avg":-0.89},
            "NV":{"avg":-0.78},
            "QV":{"avg":-0.90},
            "UV":{"avg":-0.84}
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



    async def stats(self):
        t = self; m = t.master
        mxcycles=1000
        if t.num == mxcycles:
            t.info(m.pairs)
            for k,pr in m.pairs.items():
                t.info(f',{k},{round(pr["tot"]/pr["len"],2)},{pr["min"]},{pr["max"]}')
            throw(ValueError("done"))

        for k1,a1 in t.assets.items():
            if not (a1.mbids.best != 0 and a1.masks.best != 0): continue
            for k2,a2 in t.assets.items():
                if a2.infos["n"] <= a1.infos["n"]: continue
                if not (a2.mbids.best != 0 and a2.masks.best != 0): continue
                pair = f'{a1.name}{a2.name}'
                diff = round(a1.mid["price"] - a2.mid["price"], 2)
                pr = m.pairs[f"{k1}{k2}"] = m.pairs.get(f"{k1}{k2}", {"tot":0, "len":0, "min":100000, "max":-100000})
                pr["tot"] += diff; pr["len"] += 1
                pr["max"] = max(diff, pr["max"]); pr["min"] = min(diff, pr["min"])

    def tradeone(self, q, a):
        t = self; m = t.master; cls = a.obids if q>0 else a.oasks
        t.trades_to_execute.append([cls.place_order, {"order_type": "M", "quantity": q, "ishedge":1}])

    def limitsok(self, q, pair):
        t = self; m = t.master
        def okone(qq, a):
            m.store[a.name] = (m.store.get(a.name) or a.status["pos"]) + qq
            return abs(m.store[a.name]) < 1000
        return okone(q, t.assets[pair[:1]]) and okone(-q, t.assets[pair[-1:]])

    def tradespread(self, q, pair):
        t = self; m = t.master
        if q == 0 or not self.limitsok(q, pair): return
        self.tradeone(q, t.assets[pair[:1]]); self.tradeone(-q, t.assets[pair[-1:]])
        return 1

    def buildsnd(self):
        t = self; m = t.master
        snd = super().buildsnd()
        snd["limits"] = m.store
        snd["assets"] = {}
        for k,v in m.pairs.items():
            snd["assets"][k] = {"status":v}
        return snd

    def pairdiff(self, pair):
        t = self; m = t.master
        price = lambda a: a.mid["price"] if a.mbids.best != 0 and a.masks.best != 0 else 0
        p1 = price(t.assets[pair[:1]]); p2 = price(t.assets[pair[-1:]])
        return round(p1-p2, 2) if p1 and p2 else 0

    async def christian(self): # this is stupid random trades.
        t = self; m = t.master
        # mxcycles=2000
        # if t.num == mxcycles:
        #     t.info("final=", m.pairs)
        #     throw(ValueError("done"))

        # parameters
        siz = size_of_spread = m.sp["quantity"] # todo: put in config both siz and step
        step = m.sp["step"] # we probably pay 0.04 to open and cancel spread, no point for less. To be tested

        m.store = {}
        for pair,pr in m.pairs.items():
            pri = self.pairdiff(pair)
            if not pri: continue

            if not pr.get("pos"): pr.update({"pos":0, "cur": 0})

            pr["cur"] = pri                             # current price
            pos = pr["pos"]                             # current pos
            dma = pr["dma"] = pri - pr["avg"]           # difference with the "real" price
            tgt = pr["tgt"] = - int(round(dma/step, 0)) # if dma > 0, we should sell
            sens = u.sign(tgt - pos) or 1;              # ex: dma>0 -> tgt = -10, pos = -7, sign = sign(-3) = -1

            def trade():
                for i in range(pos, tgt, sens):
                    if t.tradespread(siz * sens, pair): pr["pos"] += sens
                return pr["pos"]

            if tgt == 0 or u.sign(tgt) != u.sign(pr["pos"]): pos = trade() # came back to mean: liquidate position

            # if abs(pr["pos"]) - abs(tgt) > 6: pos = trade() # not yet to mean, but lock in some profit in case it goes back

            if abs(tgt) > abs(pos): trade() # increase position


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
