import src.utils as u
import asyncio

class BaseCycle():
    def __init__(self, master):
        t = self; m = master
        t.master = master;
        t.every = 1
        t.logger = m.logger.classFilter(self, "cycle")
        t.trade = getattr(t, m.p.get("strategy", "random"))
        t.prepare()

    async def process(self, num, upd):
        t = self; t.upd = upd; t.num = num
        await t.start()
        await t.execute_trades()
        await t.finish()
        t.master.live.pop(0)

    def prepare(self):
        t = self; m = t.master
        a = t.assets = m.assets
        t.perf = m.perf
        t.alerts = []; t.fills = {}; t.watch = []; t.meta = {}
        t.fines = u.update({}, m.fines)
        t.prep = {"trades": []}
        t.pos = u.update({}, m.pos_model)
        t.pos_updated = m.pos_updated
        t.save_pu = u.update({}, t.pos_updated) # to calculate fines later
        for k,v in a.items(): t.fills[k] = {"bids":[], "asks":[]} # prepare the fills dict
        t.fills_to_clean = []
        t.trades_to_execute = []

    async def start(self):
        t = self; m = t.master
        m.num = t.num; t.perf.reset(t.num) # keep track of time and performance.
        t.logger.setPrefix(format(t.num, "05d")) # logger prefix = new num
        self.debug(f"================== {t.num} =====================")

        await t.init_cycle() # all reset, user specific init

        m.trades += len(t.upd.fills); h = t.meta = {}; x = t.upd.competitor_metadata
        h["pnl"] = x.pnl; h["fines"] = x.fines; h["cycles"] = t.num; h["trades"] = m.trades

        t.pos_dirty = t.pos_updated
        for f in t.upd.fills: # first handle any fills
            ast = f.order.asset_code; a = t.assets[ast]; s = a.status
            o, f = await a.add_fill(f) # add the fill
            m.volume += f.filled_quantity
            t.fills[ast][o["typ"]].append(o)
            u.push(t.fills_to_clean, None if o["ok"] else f)
            for p in t.pos_dirty.keys(): t.pos_dirty[p] += s[p] * m.mult(s, p) # recalc dirty pos
            await t.onFilled(a, o) # trigger onFilled
        t.meta["volume"] = m.volume
        t.perf.step("fills")

        # here we could immediately check if position
        #   has gone our way (or not!) after the fills: not done
        await t.maybe_chock()
        t.perf.step("chock 1")

        for x in t.upd.market_updates: # then markets, we need it to get underlying
            a = t.assets[x.asset.asset_code] # update bids and asks
            a.mbids.update(x.bids); a.masks.update(x.asks)
            a.set_mid(x.mid_market_price) # set mid price
            await t.onMarketChange(a) # trigger onMarketChange
        t.perf.step("market")

        und = t.assets.get("IDX#PHX")
        if und and not und.mid.get("price") > 80: return # if no underlying price, wait

        # here we check if chock BEFORE RECALCULATING OPTIONS (which is 5 ms)
        await t.maybe_chock(market="updated")
        t.perf.step("chock 2")

        # self.error("starting pos", t.pos)
        for k,v in t.assets.items(): # update options, recalc iv and greeks
            v.update_status()
            for p in t.pos.keys(): t.pos[p] += v.status[p] * m.mult(v.status, p)
        # self.error("ending pos", t.pos)
        m.pos_updated = t.pos
        t.perf.step("options")

        await t.trade() # trade !!
        t.perf.step("prepared")

    # normally, don't touch it
    async def distribute(self):
        t = self; m = t.master
        if not len(m.p["connect_to"]) or not t.num % int(t.every) == 0: return

        snd = {"action": "newMsg", "gpos": t.pos, "assets":{}, "perf": t.perf.steps}
        for k in "fines,meta".split(","): snd[k] = getattr(self, k)
        # t.warning(t.fills)
        for k,a in t.assets.items(): # send all assets
            snd["assets"][k] = {
                "status": a.status,
                "market": { "bids": a.mbids.lst, "asks": a.masks.lst},
                "orders": { "bids": a.obids.lsth(), "asks": a.oasks.lsth()},
                "fills": t.fills[k]
            }

        try:
            dist = m.p["connect_to"][0]
            await m.connections[dist]["ws"].send_json(snd, False)
            snd=0
        except Exception as e:
            self.error("Error sending", e)

    async def finish(self):
        t = self; m = t.master
        for k in t.fines: # calcultate fines
            if abs(t.save_pu[k]) > m.c["limits-fined"][k]:
                h = t.fines[k]
                secs = 0.5 # assume 2 cycles every second
                h["val"] -= 0.01 * (abs(t.save_pu[k]) - m.c["limits-fined"][k])**2 * secs
                h["seconds"] += secs
                h["max"] = abs(t.save_pu[k]) if abs(t.save_pu[k]) > h["max"] else h["max"]

        for k,v in t.assets.items(): v.clean_cancelled(t.num) # cleaning cancelled orders

        t.perf.step("clean")

        await t.distribute() # send status to distributor (for web)
        t.perf.step("send")
        t.perf.step("ALL", t.perf.reft)
        t.upd=0

    # =====================================================================
    # =====================================================================
    # ======= these are the 4 functions specific to each trader ===========
    # =================== you should define your own ======================
    # =====================================================================
    # =====================================================================

    async def random(self, q=0): # this is stupid random trades.
        t=self; m = t.master
        q = q or m.sp["quantity"]
        if random.random() < 0.5: # only trade 25% (0.5*0.5) of the time
            for k,a in t.assets.items(): # place new orders
                if random.random() < 0.5: continue # cancel half the time
                await m.best_order(a, u.sign(random.random()-0.49) * (abs(q) or 1), "L")

    async def init_cycle(self): # all reset, user specific init
        return

    async def maybe_chock(self, greeks="old", market="old"): # "updated" or "old"(=greeks or market from previous update)
        return

    async def onFilled(self, asset, fill):
        return

    async def onMarketChange(self, asset):
        return

    async def execute_trades(self):
        t = self; m = t.master
        tasks = []; i=0
        await asyncio.sleep(m.rtt/2)
        async def wtsk(x, i):
            # await asyncio.sleep(0.001 * i)
            await x.pop(0)(*x)
        for x in t.trades_to_execute:
            tasks.append(asyncio.create_task(wtsk(x, i))); i += 1
        for tsk in tasks:
            await tsk
        t.perf.step("traded")
