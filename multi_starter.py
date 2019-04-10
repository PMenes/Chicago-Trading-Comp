import argparse
import subprocess
import re
import os
import time
import src.utils as utils
from config import config

class Processor():
    def __init__(self, args):
        self.config = c = config; self.a = vars(args);
        l = c["groups"].get(self.a["process"][0]) or self.a["process"]
        self.asc = []; self.desc=[]
        for k in l: self.asc.append(k); self.desc.insert(0, k)

    def go(self):
        (self.start if self.a["isStart"] else self.stop)()

    def _bstart(self, p):
        x = self.config["processes"].get(p, "err")# check that file is in config.processes
        if x == "err": raise ValueError('file not in config: ' + p)
        return x["start"].replace("__n__", p)

    def _start(self, p):
        s = self._bstart(p)
        l = subprocess.call(["bash", "-c", s])
        if l!=0: raise ValueError('process failed ' + s) # process failed ?
        time.sleep(0.3)
        if len(self._running(p))<1: raise ValueError('process crashed ' + s) # process crashed ?
        print(f"started {p}")

    def _running(self, p):
        s = subprocess.check_output(["bash", "-c", f'ps ax | grep "python {p}"'])
        a = list(filter(lambda x: x != "" and x.find("running")<0 and x.find("grep")<0, re.split("\n", s.decode("utf-8"))))
        return list(map(lambda x: re.split("\s+", x.strip())[0], a))

    def _kill(self, pids, pn):
        for p in pids:
            l = subprocess.call(["kill", "-9", p])
            if l!=0: raise ValueError('could not kill pid ' + str(p) + " (code=" + str(l) +")") # process failed ?
        if len(pids): print(f"killed {pn}, pids: {pids}")

    def start(self):
        self.stop()
        print("starting", self.asc)
        for p in self.asc: self._start(p)

    def stop(self):
        a = [i for i in self.config["processes"].keys()]; a.reverse()
        # print(a)
        print("stopping all:", ",".join(a))
        for p in a: self._kill( self._running(p), p)
        # print("stopping", self.desc)
        # for p in self.desc: self._kill( self._running(p), p)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run any UC trading process')
    parser.add_argument('process', metavar='process', type=str, nargs="+",  help='file(s) to run | "all" (REQUIRED)')
    parser.add_argument('-stop', dest='isStart', action='store_false')
    parser.add_argument('-start', dest='isStart', action='store_true')
    parser.set_defaults(isStart=True)
    Processor(parser.parse_args()).go()
