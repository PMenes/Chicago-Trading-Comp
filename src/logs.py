import logging, coloredlogs
import logging.config
import re
from functools import partial
import src.utils as u

def new_logger(lgs=0):
    lgs = lgs or [{"typ":"console"},{"typ":"file"}]
    l = logging.getLogger()

    prefix = [""];
    l.setPrefix = lambda x: prefix.remove(prefix[0]) or prefix.append(x)

    class MyRecord(logging.LogRecord):
        def __init__(self, name, level, pathname, lineno, msg, args, exc_info, func=None, sinfo=None, **kwargs):
            # h = {"hasErr": None}
            # chk = lambda x: (h.update({"hasErr": True}) if isinstance(x, BaseException) else 0) or str(x)
            nmsg = f'{prefix[0]} {" ".join(map(str, args))}'
            # print("hasErr", h["hasErr"], args[0], isinstance(args[0], BaseException))
            logging.LogRecord.__init__(self, name, level, pathname, lineno, nmsg, None, exc_info, func, sinfo, **kwargs)
            self.filterwith = msg

    class MyFilter(logging.Filter):
        def __init__(self, ison=False):
            self.ison = ison; self.isgood = []; self.re = re.compile('|'.join(self.isgood))
        def filter(self, record):
            return True if not self.ison else record.filterwith == 0 or re.search(self.re, record.filterwith)
        def accept(self, s):
            if not s: return self
            self.isgood.append(f'{s}'); self.re = re.compile('|'.join(self.isgood)); return self
        def ok(self, s):
            return re.search(self.re, s)

    def setPartials(obj, name=0):
        name = name or getattr(obj, "logname")
        obj.debug = partial(l.debug, name)
        obj.info = partial(l.info, name)
        obj.warning = partial(l.warning, name)
        obj.error = partial(l.error, name)
        obj.fatal = obj.critical = partial(l.critical, name)
        obj.logger = l; obj.logname = name
        return l

    for o in lgs:
        typ=o.get("typ")
        if not typ or typ not in ["console", "file"]:
            return print(f"type not valid {o.get('typ')}", o)
        if typ == "file":
            x = logging.handlers.RotatingFileHandler(o.get("filename", "log.log"))
            x.setLevel(o.get("level",'ERROR'))
            # 'format_for_file': {'format': "%(asctime)s :: %(levelname)s :: %(funcName)s in %(filename)s (l:%(lineno)d) :: %(message)s", 'datefmt': '%Y-%m-%d %H:%M:%S'},
            f = logging.Formatter("%(asctime)s :: %(levelname)s :: %(filename)s %(lineno)d :: %(message)s",datefmt='%Y-%m-%d %H:%M:%S')
            x.setFormatter(o.get("formatter", f))
            x.maxBytes = o.get("maxBytes", 10240000)
            x.backupCount = o.get("backupCount", 3)
        elif typ == "console":
            x = logging.StreamHandler()
            x.setLevel(o.get("level",'DEBUG'))
            f = coloredlogs.ColoredFormatter("%(levelname)s %(filename)s %(lineno)d: %(message)s")
            x.setFormatter(o.get("formatter", f))
        else:
            return print(f"type {typ} is not handled")

        sfilters = o.get("filters")
        x.addFilter(MyFilter(1 if sfilters else 0).accept(sfilters or 0))
        l.addHandler(x)

    def ok(s):
        rec = u.make_object('{"filterwith": "'+f'{s}'+'"}')
        for h in l.handlers:
            if h.filter(rec): return 1

    logging.setLogRecordFactory(MyRecord)
    l.thisClassLogger = l.classFilter = setPartials
    l.ok = ok
    l.setLevel("DEBUG")
    return l

# l=new_logger([
#     {"typ": "console", "level": "DEBUG", "filters": "x"},
#     {"typ": "file","level": "DEBUG", "filters": "x", "path":"tst.log"}
# ])
# l.error("xxx", "toto")
