import random
import asyncio
import math

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

        #init assets (=options or instruments)
        c = self.c
        self.assets = {}
        self.assets[c["underlying"]] = Instrument(c["underlying"], self)
        for k,v in c["options"].items(): self.assets[k] = Option(k, self, v)

        self.store = {} # if you want to store something across cycles
        self.fines_detail = {"max":0, "seconds":0, "val":0}
        self.watch = ["delta","vega"]
        self.fines = u.todict(self.watch, self.fines_detail)
        self.mult = lambda s, p: {"pnl":1, "price":1, "pos":1}.get(p, s["pos"])

        self.slowdown = 0 # in seconds. Artificially raises the time between each update

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

    #
    # def prepare_trade(self, order, repo, force_mod=False): # clsOrders: obids or oasks, order {"price":x,"quantity":y}
    #     o = order; a = self.assets[o["name"]]; cls = a.obids if o["quantity"] > 0 else a.oasks
    #     if not order["live"]: return [repo.append([i.cancel_order]) for i in cls.lst]
    #     all = cls.get_live()
    #     x = exist = all[0] if len(all) else 0 # will modify the first order if it exists
    #     def exc(): repo.append([x.modify_order, o] if exist else [cls.place_order, o])
    #     if force_mod: exc()
    #     return 0 if (x and abs(x.h["price"] - o["price"])<0.02) or not o["price"] or not o["quantity"] else exc()
    #
    # async def bulk_trades(self, trades):
    #     # await u.concurrent_tasks(trades, self.execute_trade)
    #     # return
    #
    #     repo = []; await asyncio.sleep(self.rtt/2)
    #     for t in trades: self.prepare_trade(t, repo)
    #     for e in repo:
    #         await asyncio.sleep(0.01)
    #         fn = e.pop(0)
    #         await fn(*e)
    #
    #     # repo = []; tasks = []; await asyncio.sleep(self.rtt/2)
    #     # for t in trades: self.prepare_trade(t, repo)
    #     # async def new_trade(e, i):
    #     #     await asyncio.sleep(0.001*i)
    #     #     fn = e.pop(0)
    #     #     await fn(*e)
    #     # for e,i in repo:
    #     #     tasks.append(asyncio.create_task(new_trade(e, i)))
    #     # for t in tasks: await t
    #
    #
    #
    # async def trade_paul(self):
    #     # your idea is to trade only on assets which would hedge BOTH our global vega and delta. Let's do that
    #     bound = self.sp["bound"]; q = quantity = self.sp["quantity"]; pu = self.pos_updated
    #     # if no match with you criteria, only trade random (otherwise there is never anything to hedge....)
    #     if not (abs(pu["delta"])> bound/2 and abs(pu["vega"]) > bound/4): return await self.trade_default(q*5)
    #     for k,a in self.assets.items(): # trade options first
    #         if a.name[:3] == "IDX": continue # underlying
    #         s = a.status
    #         x = "delta"; d = delta_will_be_better_if_buy = 1 if abs(pu[x] + s[x]) < abs(pu[x] - s[x]) else -1
    #         x = "vega";  v = vega_will_be_better_if_buy  = 1 if abs(pu[x] + s[x]) < abs(pu[x] - s[x]) else -1
    #         if abs(d+v) != 2: continue # we only want to trade options that will hedge BOTH our global delta and vega
    #         self.warning(f'delta={round(pu["delta"],1)} vega={round(pu["vega"],1)} {"sell" if d<0 else "buy"}ing {a.name}')
    #         await self.best_order(a, u.sign(d) * q)
    #
    # async def trade_random(self, q=0): # this is stupid random trades.
    #     q = q or self.sp["quantity"]
    #     if random.random() < 0.5: # only trade 25% (0.5*0.5) of the time
    #         for k,a in self.assets.items(): # place new orders
    #             if random.random() < 0.5: continue # cancel half the time
    #             await self.best_order(a, u.sign(random.random()-0.49) * (abs(q) or 1), "L")

    # async def christian(self): # this one run in the cycle
    #     t = self; m = t.master
    #     if t.traded: return
    #     for k in m.watch: t.prep[k] = pos[k] # init with current delta and vega
    #     q = m.sp["quantity"]
    #     for k,a in t.assets.items(): # get trade options first
    #         if a.name[:3] == "IDX": continue
    #         self.get_spread(a, abs(q))
    #
    #     # self.warning("result:", "vega=",self.prep["vega"], "delta=",self.prep["delta"])
    #
    #     if abs(self.prep["vega"])>self.c["limits"]["vega"]: # if we will be over limits vega, increase size of "good" trades
    #         self.warning("over vega:", "vega=",self.prep["vega"], "delta=",self.prep["delta"])
    #         v = u.sign( self.prep["vega"] )
    #         for t in self.prep["trades"]:
    #             s = self.assets[t["name"]].status; q = t["quantity"]
    #             if u.sign(s["vega"] * q) != v:
    #                 t["quantity"] *= 2; self.prep["delta"] += q*s["delta"]
    #
    #     n="IDX#PHX"; a = self.assets[n]; th = to_hedge = self.prep["delta"] # +a.status["pos"]
    #     if abs(to_hedge)>self.c["limits"]["delta"]: # if we will be over limits delta, hedge it
    #         self.warning("over delta:", "vega=",round(self.prep["vega"]), "delta=",round(th))
    #         q = round( -th, 0); sens = u.sign(q)
    #         cls = a.mbids if q>0 else a.masks
    #         # px = cls.lst[0]["price"]+sens*0.01 # better order, wait to be hit
    #         px = (a.masks if q>0 else a.mbids).lst[0]["price"] # cross the spread
    #         self.prep["trades"].append( {"name":n, "price":px, "quantity": q, "live": 1} )
    #
    #     self.perf.step("prepared")
    #     await self.bulk_trades(self.prep["trades"])
    #     # await u.concurrent_tasks(self.prep["trades"], self.execute_trade)
    #     # tasks = []
    #     # for o in self.prep["trades"]: tasks.append( asyncio.create_task( self.execute_trade(o) ))
    #     # for t in tasks: await t
    #     self.traded = 1

    """
    lessons learned when we run always joining best bid and ask (no hedging, nothing, just best bid and ask)

    1- we make no money on options. we get filled small amounts, and trade little (2 option trades / cycle)
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

    async def christian(self, q=0): # this is stupid random trades.
        t=self; m = t.master
        # parameters
        tps = target_pos = 7
        lbk = lookback = 10 # number of cycles to look back for price up/down determination
        q = 6 # normal trade size
        nq = abs(q) or abs(m.sp["quantity"]) or 10

        b = t.assets["IDX#PHX"]; lb = b.get_histo(lookback); mid=b.mid["price"]
        ch = math.log10( mid / lb)*5000 if lb and mid else 0 # increase || decrease in target pos
        for k,a in t.assets.items(): # place new option orders
            if k[:3] == "IDX": continue
            rp = a.status["pos"] # real pos
            tp = tps + (1 if a.name[:1] == "C" else -1) * ch # target pos
            sp = max(a.get_spread(), 0.15) # spread to apply
            add = abs(m.sp["better"]) * int(abs((tp-rp)/ nq))**3 # better price in our way
            add = min(add, sp)
            sens = u.sign(tp - rp)
            a.status["vpos"] = (1 if a.name[:1] == "C" else -1) * ch
            a.status["pri"] = add * sens
            if sens == 1:
                p = a.obids.order(t, q=q, add=add); a.oasks.order(t, q=q, p=p+sp)
            else:
                p = a.oasks.order(t, q=q, add=-add); a.obids.order(t, q=q, p=p-sp)

        # u.push(repo, m.best_order(t.assets["IDX#PHX"], -pos["delta"], add=0))
        #
        #
        # if abs(pos["vega"])>m.c["limits-fined"]["vega"]: # if we will be over limits vega, increase size of "good" trades
        #     t.warning("over vega:", "vega=",pos["vega"], "delta=",pos["delta"])
        #     v = u.sign( pos["vega"] );
        #     for fn,r in repo:
        #         a = t.assets[r["name"]]; s = a.status; q = r["quantity"]
        #         if u.sign(s["vega"] * q) != v:
        #             h = {"name":a.name, "price": None, "quantity": nq*u.sign(q), "order_type": "M"}
        #             cls = a.obids if q>0 else a.oasks; u.push(addmkt, [cls.place_order, h])
        #
        pos = m.pos_updated
        n="IDX#PHX"; a = t.assets[n]; th = to_hedge = pos["delta"] # +a.status["pos"]
        if abs(to_hedge)>m.c["limits"]["delta"]: # if we will be over limits delta, hedge it
            t.warning("over delta:", "vega=",round(pos["vega"]), "delta=",round(th))
            h = {"name":a.name, "price": None, "quantity": round( -th, 0), "order_type": "M"}
            # a.obids.cancel_all(t); a.oasks.cancel_all(t);
            # cls = a.obids if th<0 else a.oasks; cls.order(t, q=th)


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
