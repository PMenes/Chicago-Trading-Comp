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
        self.pairs = {}
        u.delfile(f'.logs/mas.txt')

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

    def tradeone(self, q, a):
        t = self; m = t.master
        cls = a.mbids if q>0 else a.masks
        # h = {"price": cls.oppo.best, "quantity": q, "ishedge":1}
        h = {"order_type": "M", "quantity": q, "ishedge":1}
        t.trades_to_execute.append([cls.orders.place_order, h])

    def tradespread(self, q, a1, a2):
        if q == 0: return
        self.warning("trading", f"{a1.name}{a2.name}", q)
        self.tradeone(q, a1); self.tradeone(-q, a2)

    async def christian(self): # this is stupid random trades.
        t = self; m = t.master
        # parameters:
        mxcycles=200
        if t.num == mxcycles:
            if collect:
                t.info("final=", m.pairs)
            else:
                for k,pr in m.pairs.items():
                    log.info(f'{k},{pr["tot"]/pr["len"]},{pr["min"]},{pr["max"]}')
        if t.num > mxcycles: return
        lbk = lookback = 30
        siz = size_of_spread = 9
        collect = 1 # collecting statistics only if truthy
        for k1,a1 in t.assets.items():
            if not (a1.mbids.best != 0 and a1.masks.best != 0): continue
            for k2,a2 in t.assets.items():
                if a2.infos["n"] <= a1.infos["n"]: continue
                if not (a2.mbids.best != 0 and a2.masks.best != 0): continue
                pair = f'{a1.name}{a2.name}'
                diff = round(a1.mid["price"] - a2.mid["price"], 2)
                if collect:
                    pr = m.pairs[f"{k1}{k2}"] = m.pairs.get(f"{k1}{k2}", {"tot":0, "len":0, "min":100000, "max":-100000})
                    pr["tot"] += diff; pr["len"] += 1
                    pr["max"] = max(diff, pr["max"]); pr["min"] = min(diff, pr["min"])
                else:
                    pr = m.pairs[f"{k1}{k2}"] = m.pairs.get(f"{k1}{k2}", {"histo":[], "ma":0, "pos":0, "dma":0, "res":0})
                    pr["histo"].append(diff)
                    if len(pr["histo"]) < lookback: continue # wait for full lookback history
                    if pr["ma"] == 0: # update movving averages
                        tot=0
                        for i in pr["histo"]: tot+=i
                        pr["ma"] = round(tot/lookback)
                    else:
                        pr["ma"] += -pr["histo"][0]/lbk + pr["histo"][-1]/lbk

                    dma = diff - pr["ma"]
                    th = treshold = 0.1
                    if pr["dma"] and u.sign(pr["dma"]) != u.sign(dma):
                        t.warning("closing", pair)
                        t.tradespread(siz * -pr["pos"], a1, a2) # will do nothing if pr["pos"] == sens
                        res = pr["pos"] * (pr["dma"] -dma)
                        pr["res"] += res
                        t.debug("traded", pair, "closed", "res=", res, "tot=", pr["res"])
                        pr["pos"] = 0; pr["dma"] = 0
                    if abs(dma) > abs(th):
                        sens = u.sign(dma-th)
                        if pr["pos"] != sens:
                            t.tradespread(siz * (sens - pr["pos"]), a1, a2) # will do nothing if pr["pos"] == sens
                            pr["pos"] = sens; pr["dma"] = dma
                            t.debug("traded", pair, "opened", sens, "diff=", diff, "dma=", dma)



                # t.logger.debug("cycle_ma", f',{pair},{diff}')

        #         sens = 1 if pr["histo"][-1] >= pr["ma"] else -1 # now trade!
        #         if pair == "KM":
        #             self.warning(sens, "last=", pr["histo"][-1], "ma=", pr["ma"], "a1", a1.mid["price"], "a2", a2.mid["price"])
        #         self.tradespread(siz * (sens - pr["pos"]), a1, a2) # will do nothing if pr["pos"] == sens
        #         pr["pos"] = sens
        #
        # self.info("keys", len(m.pairs.keys()), ",".join(m.pairs.keys()))

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
