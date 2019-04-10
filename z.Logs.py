import logging, coloredlogs
import logging.config
import re
from functools import partial
# import src.utils as u

def set_config(log_file):
    return {
        'version': 1,
        'disable_existing_loggers': False,   # set True to suppress existing loggers from other modules
        'loggers': {
            '': {
               'level': 'DEBUG',
               'handlers': ['console', 'file'],
            },
        },
        'formatters': {
            'colored_console': {'()': 'coloredlogs.ColoredFormatter', 'format': "%(levelname)s %(filename)s %(lineno)d: %(message)s"},
            # 'format_for_file': {'format': "%(asctime)s :: %(levelname)s :: %(funcName)s in %(filename)s (l:%(lineno)d) :: %(message)s", 'datefmt': '%Y-%m-%d %H:%M:%S'},
            'format_for_file': {'format': "%(asctime)s :: %(levelname)s :: %(filename)s %(lineno)d :: %(message)s", 'datefmt': '%Y-%m-%d %H:%M:%S'},
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'colored_console',
                # 'filters': ['consolefilter'],
                'stream': 'ext://sys.stdout',
            },
            'file': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'format_for_file',
                # 'filters': ['filefilter'],
                'filename': log_file,
                'maxBytes': 10240000,
                'backupCount': 3
            }
        },
    }

def new_logger(name=0, file=0):
    name = name or 'log'
    file = file or f'{name}.log'
    logging.config.dictConfig(set_config(file))
    l = logging.getLogger()
    class MyFilter(logging.Filter):
        def __init__(self, ison=False):
            self.ison = ison; self.name=name
        def filter(self, record):
            key = record.msg[:1]
            return True if not self.ison else key == " "
    def setFilter(console=0, to_file=0, f=0):
        f=l.handlers[0]; f.filters = []; f.addFilter(MyFilter(console)) # console handler
        f=l.handlers[1]; f.filters = []; f.addFilter(MyFilter(to_file)) # console handler
        return l
    def setLevel(x, y=0):
        l.handlers[0].setLevel(x) # console handler
        if y: l.handlers[1].setLevel(y) # file handler
        return l

    l.setLevel = lambda x,y=0: setLevel(x,y)
    l.setFilter = lambda x,y=0: setFilter(x,y)
    l.setLevel("DEBUG", "DEBUG") # default levels
    l.setFilter(1, 0) # by default the file handler has no filter (=logs everything)


    prefix = [""]; a = []; r = [1]
    l.setPrefix = lambda x: prefix.remove(prefix[0]) or prefix.append(x)
    l.compile = lambda x: r.remove(r[0]) or r.append(re.compile('|'.join(x)))
    l.accept = lambda s: l.compile(a.append(re.escape(s)) or a)
    l.reject = lambda s: l.compile(a.remove(re.escape(s)) or a)
    l.reject = lambda s: l.compile(a.remove(re.escape(s)) or (not len(a) and a.append(0)) or a)
    l.ok = lambda n,v=40: " " if n==0 or (len(a) and re.search(r[0], f'{n}')) else "1"

    l.olog = l._log
    def nlog(level, msg, args, exc_info=None, extra=None, stack_info=False):
        hasErr=0
        def chk(x):
            if isinstance(x, BaseException): hasErr=1
            return str(x)
        nmsg = f'{l.ok(msg,level)}{prefix[0]} {" ".join(map(chk, args))}'
        if hasErr: exc_info=True
        l.olog(level, nmsg, None, exc_info, extra, stack_info)
    l._log = nlog

    def setPartials(obj, name=0):
        name = name or obj.logname
        obj.debug = partial(l.debug, name)
        obj.info = partial(l.info, name)
        obj.warning = partial(l.warning, name)
        obj.error = partial(l.error, name)
        obj.fatal = obj.critical = partial(l.critical, name)
        obj.logger = l
        return l
    l.thisClassLogger = l.classFilter = setPartials
    return l


# x=new_logger(file=u.delfile("tst.log"))
# x.setLevel('DEBUG')
# x.setFilter(1,1)
# x.accept("x")
# x.setPrefix('000')
# x.debug("xxx", "toto take")
# print(" ")
# x.debug("yyy", "toto not take")
