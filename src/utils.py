import time
import json
import asyncio
import signal
import socket
import requests
from types import SimpleNamespace as Namespace
from functools import partial

import src.trader.Logs as logs

def new_logger(name=0,file=0): return logs.new_logger(name, file)

def make_object(h):
    def get(o, s):
        try:
            return getattr(o, s)
        except Exception as e:
            return None

    def set(o, k, v): setattr(o, k, v)
    x = json.loads(h, object_hook=lambda d: Namespace(**d))
    x.get = partial(get, x); x.set = partial(set, x)
    return x

# config stuff
def get_config(path="config.json"):
    with open(path) as f:
        data = json.load(f)
    return data
def get_params(f, path="config.json"):
    c = get_config(path)
    return c["processes"][f]
config = get_config()

# handle known errors properly
def makerr(errClass, log, msg, *oth):
    log.error(0, msg, oth)
    if config["env"] == "dev": raise errClass(msg)

# sugar for arrays and dicts
def push(arr, elt):
    if elt: arr.append(elt)
    return elt
def set(h, k, v):
    if v: h[k] = v
    return v

def update(dct, *oth):
    for h in oth: dct.update(h or {})
    return dct

sign = lambda x: bool(x > 0) - bool(x < 0)
def between(min, x, max):
    if x < min: return min
    if x > max: return max
    return x

# network addresses
class MyAddr():
    def local(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("www.example.com",80))
        a = (s.getsockname()[0])
        s.close(); return a
    def real(self):
        r = requests.get('https://api.ipify.org?format=json')
        return r.json()['ip']

# time and measure performance
def curtime():
    return round(time.time() * 1000,1)

class Perf():
    def __init__(self, num, lg):
        lg.thisClassLogger(self, "perf")
        self.time = 0
        self.reset(num)

    def reset(self, num=0):
        if self.time: self.step(f'NEW {num}')
        self.time = curtime()
        self.reft = self.time
        self.steps = []
        self.snd = {"num":num, "started": self.time, "data": self.steps}

    def step(self, name=0, ref=0):
        t = curtime(); el = round(t - (ref or self.time), 2); self.time = t
        if name == 0: return print(f"============== perf =========== {el}")
        self.steps.append({"name":name, "elapsed": el})
        self.debug(f"{el}   ========= {name}")

# launch processes: sync
def launch_server(cls):
    c=cls()
    try:
        c.start()
    except KeyboardInterrupt:
        c.stop()

# launch processes: async
def launch_server_async(cls):
    c=cls()
    try:
        loop = asyncio.get_event_loop()
        tasks = c.start()
        for t in tasks:
            exe = t.pop(0)
            loop.create_task(exe(*t))
        loop.run_forever()

    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(c.stop())
        pending = asyncio.Task.all_tasks()
        for task in pending: task.cancel()
        loop.run_until_complete(asyncio.gather(*pending, loop=loop, return_exceptions=True))
        # # for task in pending:
        # #     print("task---------:", task)
        # #     if task.cancelled():
        # #         print("ok---------:", task)
        # #         continue
        # #     else:
        # #         print("err---------:", task)
