import src.utils as u
from src.trader.Markets import Markets
from src.trader.Orders import Orders

class Instrument():
    status0 = {k: {"delta":1, "one":1}.get(k,0) for k in "pos,vpos,pri,cash,pnl,price,one,delta,gamma,vega,sigma".split(",")}
    def __init__(self, name, master, opt={}):
        self.logname = f"{name}"
        self.logger = master.logger.thisClassLogger(self)
        x = opt.get("spread", 0); self.spread = x if x else 0.6
        self.name = name; self.master = master
        self.orders = {}; self.wo = {}

        self.obids = Orders(1, name, self); self.oasks = Orders(-1, name, self)
        self.mbids = Markets(1, name, self.obids); self.masks = Markets(-1, name, self.oasks)
        self.to_clean = []
        self.mid = {"num":0,"price":0}
        self.histo = []

        # greeks = "price,gamma,vega,sigma"
        self.status = u.update({"name":name}, self.status0)
        # for k in f"pos,cash,pnl,{greeks}".split(","): self.status[k] = 0
        self.greeks = ["price","delta","gamma","vega","sigma"]
        # if not Instrument.status0:
        #     Instrument.status0 = h = u.update({}, self.status); del h["name"]
        #     for k in h.keys(): h[k] = 0

    def best_price(self, sens):
        return self.mbids.best_price() if sens == 1 else self.masks.best_price()

    def get_spread(self):
        b = self.mbids.best_price(); a = self.masks.best_price()
        return abs(a-b) if a and b else 0.8

    def get_histo(self, lookback):
        return self.histo[max(-lookback, -len(self.histo))] if len(self.histo) else self.mid["price"]

    def set_mid(self, v):
        self.mid = {"price": round(v,3), "num":self.mid["num"]}
        if self.histo != False: self.histo.append(self.mid["price"])
        return
        x = self.mid_price()
        self.mid["eprice"] = v
        if(abs(v - x)/v > 0.02):
            self.error("??????????????", self.name, self.mid)
            u.makerr( NotImplementedError, self.logger,"mid price")

    def mid_price(self):
        if self.mid["num"] == self.master.num: return self.mid["price"] # do not recalc multiple times
        exist = lambda cls: 0 if len(cls.lst)==0 else cls.lst[0]
        bid = exist(self.mbids); ask = exist(self.masks)
        mp = 0; self.status["alert"] = 1
        if bid and ask:
            mp = (bid["price"]+ask["price"])/2; self.status["alert"] = 0
        elif bid and not ask:
            mp = bid["price"] + self.spread*2
        elif not bid and ask:
            mp = ask["price"] - self.spread*2
        self.mid = {"num":self.master.num, "price":mp}
        return mp

    def update_status(self):
        h = self.status
        h["price"] = self.mid_price()
        h["pnl"] = h["cash"] + h["pos"] * h["price"]
        return h

    def exist_order(self, oid, msg, silent=0, p=0, q=0):
        x = self.orders.get(oid); ret = []
        if x: return x
        if not silent: self.error(f"Could not find order (for {msg}):", oid or "NONE")
        if len(oid): return self.fatal(f".... and oid is known !!!:", oid or "NONE")
        if not p or not q: return x
        p = round(p, 2)
        for k,o in self.orders.items():
            if o.h["price"] == p and o.h["quantity"] == q: ret.append(o)
        if len(ret) == 1: self.error("but recovered it!", ret[0].sid); return ret[0]
        if not len(ret): return self.fatal(f"could not find any order matching p={p} and q={q}")
        self.fatal(f"found {len(ret)} orders matching p={p} and q={q}", [i.oid for i in ret])

    async def add_fill(self, f):
        o = f.order; oid = o.order_id
        fp = round(f.fill_price,2); fq = round(f.filled_quantity * u.sign(o.quantity))
        self.status["pos"] += fq; self.status["cash"] -= fq*fp
        h={"price":fp, "quantity":fq, "typ": "bids" if fq>0 else "asks"} #, "size":abs(fq)
        self.info(f"filled-{oid[-6:]} ({fq} at {fp})", h)

        ok = self.exist_order(oid, "fill_order", p=o.price, q=o.quantity); h["ok"] = 1 if ok else 0
        ok.fill(f) if ok else 0
        return [h, f]


    # def clean_dirty_fills(self, f):
    #     t = self; m = t.master
    #     o = f.order; oid = o.order_id; q = o.quantity
    #     k = f'{t.name}_{round(o.price,2) or 0}_{o.quantity}' # same as kwo in SingleOrder class
    #     self.warning("dirty fill, oid=", oid or "NONE", k, f'\nf: {f}')
    #     # try to find it anyway in bastardized workaround
    #     if not t.wo.get(k): return t.error("could not find {oid} ({k}) in work-around")
    #     ok = t.orders.get(t.wo[k]["oid"])
    #     if not ok: return t.error("could not find {oid} in self.orders")
    #     t.info("=======recovered order=============:", ok.oid)
    #     ok.fill(f)


    async def place_order(self, h):
        # if self.name != "C98PHX": return
        return await self.obids.place_order(h) or await self.oasks.place_order(h)

    async def modify_order(self, oid, h):
        ok = self.exist_order(oid, "modify_order")
        return ok if not ok else ok.modify_order(h)

    async def cancel_order(self, oid):
        ok = self.exist_order(oid, "cancel_order")
        return ok if not ok else await ok.cancel_order()

    def clean_cancelled(self, num):
        a = self.to_clean.copy()
        for oid in a:
            o = self.orders.get(oid)
            ok = o and o.cancelled and o.cancelled < self.master.num-1 and o.delete()
            if ok: self.to_clean.remove(oid)
