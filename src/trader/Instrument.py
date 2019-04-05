import src.utils as u
from src.trader.Markets import Markets
from src.trader.Orders import Orders

class Instrument():
    def __init__(self, name, master, opt={}):
        self.logname = f"{name}"
        self.logger = master.logger.thisClassLogger(self)
        x = opt.get("spread", 0); self.spread = x if x else 0.6
        self.name = name; self.master = master; self.orders = {}

        self.obids = Orders(1, name, master); self.oasks = Orders(-1, name, master)
        self.mbids = Markets(1, name, self.obids); self.masks = Markets(-1, name, self.oasks)
        self.to_clean = []

        self.status = {"name":name, "one":1, "alert":0, "pos":0, "avg":0, "cash":0, "mkt":0, "pnl":0}
        self.keys = ["price", "delta","gamma","vega", "sigma"]
        for k in self.keys: self.status[k] = 0
        self.mid = {"num":0, "price":0}

    def set_mid(self, v):
        self.mid = {"price": v, "num":self.mid["num"]}; return
        x = self.mid_price()
        self.mid["eprice"] = v
        if(abs(v - x)/v > 0.02):
            print("??????????????", self.name, self.mid)
            u.makerr( NotImplementedError, self.logger,"mid price")

    def mid_price(self):
        if self.mid["num"] == self.master.num: return self.mid["price"] # do not recalc multiple times
        exist = lambda cls: 0 if len(cls.lst)==0 else cls.lst[0]
        bid = exist(self.mbids); ask = exist(self.masks)
        mp = 0; self.status["alert"] = 1
        if bid and ask:
            mp = (bid["price"]+ask["price"])/2; self.status["alert"] = 0
        elif bid and not ask:
            # print(bid, self.spread, self.name)
            mp = bid["price"] + self.spread*2
        elif not bid and ask:
            mp = ask["price"] - self.spread*2
        self.mid = {"num":self.master.num, "price":mp}
        return mp

    def update_status(self):
        h = self.status
        h["mkt"] = h["price"] = self.mid_price()
        h["pnl"] = h["cash"] + h["pos"] * h["mkt"]
        return h

    def exist_order(self, oid, msg):
        x = self.orders.get(oid, 0)
        return x if x else print(msg)

    async def add_fill(self, f, fills):
        o = f.order; oid = o.order_id
        ok = self.exist_order(oid, f"Error, could NOT fill order (not exist): {oid}")
        # this is a serious error if we don't have the order in the orders inventory
        if not ok: return u.makerr(ValueError, self.logger, "Could not find filled order", o.order_id, f'f: {f}', f'self.orders: {self.orders}')

        ok.fill(f, fills); q = ok.lastfill
        self.status["pos"] += q; self.status["cash"] -= q*o.price # for pnl purposes
        return ok

    async def place_order(self, h):
        # if self.name != "C98PHX": return
        await self.obids.place_order(h) or await self.oasks.place_order(h)

    async def modify_order(self, oid, h):
        ok = self.exist_order(oid, f"Error, could NOT modify order (not exist):")
        return ok if not ok else ok.modify_order(h)

    async def cancel_order(self, oid):
        ok = self.exist_order(oid, f"Error, could NOT cancel_order (not exist or cancelled): {oid}")
        return ok if not ok else await ok.cancel_order()

    def clean_cancelled(self, num):
        a = [] + self.to_clean
        for id in a:
            o = self.orders.get(id, 0)
            if not o: continue
            x = o.cancelled and o.cancelled < self.master.num -1
            if x:
                self.orders.pop(id, None)
                self.to_clean.remove(id)
