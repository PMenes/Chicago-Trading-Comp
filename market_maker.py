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
        self.assets[c["underlying"]] = Instrument(c["underlying"], self)
        for k,v in c["options"].items(): self.assets[k] = Option(k, self, v)

        self.store = {} # if you want to store something across cycles
        self.fines_detail = {"max":0, "seconds":0, "val":0}
        self.watch = ["delta","vega"]
        self.fines = u.todict(self.watch, self.fines_detail)
        self.mult = lambda s, p: {"pnl":1, "price":1, "pos":1}.get(p, s["pos"])

        self.slowdown = 0 # for dev. in seconds. Artificially raises the time between each update

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

    """
    lessons learned when we run always joining best bid and ask (no hedging, nothing, just best bid and ask)

    1- we make no money purely market-making options.
        we get filled only small amounts, and trade little (2 option trades / cycle)
        That should not be the case. Reason is probably the slowness of the exchange.
        (orders not taken into account until sometimes 4 cycles after, no modification that I could get working)
        I could never increase the number of trades (we do not trade much more constantly bettering bid and ask)
        Anyway, it means we will not be making money market-making, which is ironic.
        Note: that could change if the exchange gets better, but I don't expect it to happen.

    2- we always end up with opposite positions for puts and calls
        That suggests that market takers primary driver is underlying price, which is not surprising .
        It will probably get worse with competitors (amateurs).
        So we should raise call prices and underlying is up (op for puts) and vice-versa

    3- vol seems more or less stable
        it moves, but not like from 7 to 50. Seems stable around 30.
        Given that, plus the fact that we pay no theta, we should tend to be long vol.
        At least we could make a little bit on delta adjustments since we should be long gamma on average.
        It also means we do not trade vol (no point), we mock trading underlying with option (see point 2).
        So we have to adapt to the market conditions and trade like amateurs (ie not vol)

    try 1:
        * base target position +7 per option, should give a global vega around 10
        * when underlying is up, increase target pos for calls, decrease for puts (and vice-versa)
        * do not try to be on each trade, given how the exchange works it does not pay for the risk
        * adjust order price according to virtual position bias +7+price change impact (ie: short if pos+7<0)
        ------ result -------
        not great, about 200$ pnl after 1000 cycles, but consistent across all options, so seems "stable" (doh...)
        2 option trades per cycle, 5 contracts per fill on average
        nice is vega hedges itself, delta too but more capricious
    """

    async def christian(self): # this is stupid random trades.
        t = self; m = t.master
        if t.num < 25: return
        # parameters
        tps = target_pos = 7
        lbk = lookback = 10 # number of cycles to look back for price up/down determination
        q = nq = abs(m.sp.get("quantity") or 0) or 10  # normal trade size

            # if isGoodFor("vega", 10, sens, a) q=q*1.2 # vega target is around 10 (7 per option)
            # if isGoodFor("delta", 0, sens, a) q=q*1.3 # delta should be around 0
        pos = m.pos_updated
        # isGoodFor = lambda gk,tg,ss,a: 1 if u.sign(ss * a.status[gk]) != u.sign(tg - pos[gk]) else 0

        b = t.assets["IDX#PHX"]; lb = b.get_histo(lookback); mid=b.mid["price"]
        ch = math.log10( mid / lb)*5000 if lb and mid else 0 # increase || decrease in target pos
        for k,a in t.assets.items(): # place new option orders
            if k[:3] == "IDX": continue
            q = nq
            sp = max(a.get_spread(), 0.15) # spread to apply
            # first we set the price, measuring the different beteween the real pos and the target pos
            rp = a.status["pos"] # real pos
            tp = tps + (1 if a.name[:1] == "C" else -1) * ch # target pos

            # add = max(abs((tp-rp)/60*sp), 0.01) * u.sign(tp-rp) # pct of crossing the spread (60 diff to cross 100%)
            add = (tp-rp)/60*sp # pct of crossing the spread (60 diff to cross 100%)
            a.status["vpos"] = tp - rp
            a.status["pri"] = add
            if add > 0:
                p = a.obids.order(t, q=q, add=add); a.oasks.order(t, q=q, p=p+sp)
            else:
                p = a.oasks.order(t, q=q, add=add); a.obids.order(t, q=q, p=p-sp)


        # if abs(pos["vega"])>m.c["limits"]["vega"]: # if we will be over limits vega, increase size of "good" trades
        #     t.warning("over vega:", "vega=",pos["vega"], "delta=",pos["delta"])
        #     v = u.sign( pos["vega"] );
        #     for k,a in t.assets.items(): # place new option orders
        #         if k[:3] == "IDX": continue
        #         s = a.status
        #         sens = -1 if abs(s["vega"] + pos["vega"]) > abs(pos["vega"]) else 1
        #         cls = a.mbids if sens>0 else a.masks
        #         h = {"price": cls.oppo.best, "quantity": 3*sens, "ishedge":1} # 3 for each should lower vega by 5
        #         t.trades_to_execute.append([cls.orders.place_order, h])

        n="IDX#PHX"; a = t.assets[n]; th = to_hedge = pos["delta"] # hedge delta
        if abs(to_hedge)>m.c["limits"]["delta"]: # if we will be over limits delta, hedge it
            t.warning("over delta:", "vega=",round(pos["vega"]), "delta=",round(th))
            h = {"name":a.name, "price": None, "quantity": round( -th, 0), "order_type": "M"}
            a.obids.cancel_all(t); a.oasks.cancel_all(t);
            cls = a.mbids if th<0 else a.masks; cls.orders.order(t, q=th, p=cls.oppo.best)


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
