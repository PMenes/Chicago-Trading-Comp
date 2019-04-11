from py_vollib.black_scholes import black_scholes as oprice
from py_vollib.black_scholes.implied_volatility import implied_volatility as iv
from py_vollib.black_scholes.greeks.analytical import (delta, gamma, vega)

from src.trader.Instrument import Instrument
import src.utils as u

class Option(Instrument):
    def __init__(self, name, master, o={}, opt={}):
        if not o.get("flag", 0) in ["c", "p"]: raise NotImplementedError("no valid flag set")
        if not o.get("K", 0): raise NotImplementedError("no valid strike set")
        self.opt = u.update(o, {"r":0, "t": 1/6})

        x = opt.get("spread", 0); self.spread = x if x else 0.6
        x = opt.get("rounding", 0); self.rounding = x if x else 2
        Instrument.__init__(self, name, master, o)
        self.histo = False

    def update_status(self):
        und = self.master.assets[self.master.c["underlying"]]
        h = self.calc_all({"F": und.mid_price(), "price": self.mid_price()})
        if h:
            for k in self.greeks: self.status[k] = h[k]
        super().update_status()
        return self.status

    def all_set(self, h):
        errs=[]; b = u.update( {"F":0,"sigma":0,"price":0}, h, self.opt)
        for k in ["F"]: errs.append(f'missing {k}') if b[k] == 0 else 0
        e = 'need either sigma or price, both are missing'
        errs.append(e) if not b.get("sigma", 0) and not b.get("price", 0) else 0
        if b.get("sigma", 0) and b.get("price", 0): b["sigma"] = 0 # price superseeds sigma if both present
        if not len(errs): return b
        for e in errs: print(f'err: {e}')
        return 0

    def calc_all(self, b):
        h = self.all_set(b)
        if not h: return False
        if not h.get("sigma"): self.civ(h)
        if not h.get("sigma"): return False
        a = (h["flag"], h["F"], h["K"], h["t"], h["r"], h["sigma"])
        r = self.rounding
        h["price"] = round(oprice(*a),r)
        h["delta"] = round(delta(*a),r)
        h["gamma"] = round(gamma(*a)*100,r)
        h["vega"] = round(vega(*a),r)
        return h

    def civ(self, h):
        try:
            x = iv(h["price"], h["F"], h["K"], h["t"], h["r"], h["flag"])
        except Exception as e:
            self.warning(e)
        else:
            h["sigma"] = round(x,self.rounding)



# x = Option({"K":102}, {"F":100, "flag":"c", "price":2})
# x.calc_all()
# print(x.price, x.delta, x.gamma, x.vega)
# print(x.opt)
