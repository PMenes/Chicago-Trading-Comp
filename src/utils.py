import time
import os
import json
import asyncio
import socket
import requests
from types import SimpleNamespace as Namespace
from functools import partial
import importlib
import sys
import collections
import copy
import re

import src.logs as logs

def deep_update(d, other):
    iscm = lambda x: isinstance(x, collections.Mapping)
    for k, v in other.items():
        d_v = d.get(k)
        if iscm(v) and iscm(d_v):
            deep_update(d_v, v)
        else:
            d[k] = copy.deepcopy(v) # or d[k] = v if you know what you're doing

def get_config(no_args=False):
    global config
    from config import config
    cf = sys.argv[1] if len(sys.argv)>1 else "configs/default.py"
    if no_args or not os.path.exists(cf): return
    cf = re.sub(r"\/", ".", cf).replace(".py", "")
    upd = importlib.import_module(cf).upd
    deep_update(config, upd)
get_config()

# print(config["processes"]["market_maker.py"])

# sugar for arrays and dicts
def push(arr, elt):
    if elt: arr.append(elt)
    return elt
def set(h, k, v):
    if v: h[k] = v
    return v

def todict(keys, dft=0):
    h={}
    todef = lambda x: x if type(dft) != dict else update({}, x)
    for k in keys: h[k] = todef(dft)
    return h

def update(dct, *oth):
    for h in oth: dct.update(h or {})
    return dct

import os, errno

def delfile(filename):
    try:
        os.remove(filename)
    except OSError as e: # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT: raise # errno.ENOENT = no such file or directory; re-raise if not
    return filename

act = asyncio.create_task
async def concurrent_tasks(tsks, fnc=0):
    tsks = tsks if not fnc else [act( fnc(o) ) for o in tsks]
    for t in tsks: await t
    return [t.result() for t in tsks]

sign = lambda x: bool(x > 0) - bool(x < 0)
def between(min, x, max):
    if x < min: return min
    if x > max: return max
    return x

log=0
def setLogger(lgs=0):
    return logs.new_logger(lgs)

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
# def get_config(path="config.json"):
#     with open(path) as f:
#         data = json.load(f)
#     return data
# def get_params(f, path="config.json"):
#     c = get_config(path)
#     return c["processes"][f]
# config = get_config()

# handle known errors properly
def makerr(errClass, log, msg, *oth):
    log.error(0, msg, oth)
    if config["env"] == "dev": raise errClass(msg)

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
        if name == 0: return self.debug(f"============== perf =========== {el}")
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
def launch_server_async(cls, file=0):
    c=cls(file)
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
