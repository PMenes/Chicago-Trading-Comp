import logging, coloredlogs
import logging.config
import re
from functools import partial

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
            'colored_console': {'()': 'coloredlogs.ColoredFormatter', 'format': "%(filename)s %(lineno)d: %(message)s"},
            'format_for_file': {'format': "%(asctime)s :: %(levelname)s :: %(funcName)s in %(filename)s (l:%(lineno)d) :: %(message)s", 'datefmt': '%Y-%m-%d %H:%M:%S'},
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'colored_console',
                'stream': 'ext://sys.stdout'
            },
            'file': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'format_for_file',
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

    prefix = [""]
    l.setPrefix = lambda x: prefix.remove(prefix[0]) or prefix.append(x)

    a = []; r = [1]
    l.compile = lambda x: r.remove(r[0]) or r.append(re.compile('|'.join(x)))
    l.accept = lambda s: l.compile(a.append(re.escape(s)) or a)
    l.reject = lambda s: l.compile(a.remove(re.escape(s)) or a)
    # l.reject = lambda s: l.compile(a.remove(re.escape(s)) or (not len(a) and a.append(0)) or a)

    l.olog = l._log
    # ok = lambda v, n: 1 if v > 39 or n==0 else len(a) and re.search(r[0], f'{n}')
    def ok(v,n):
        # print("r=", r)
        return 1 if v > 39 or n==0 else len(a) and re.search(r[0], f'{n}')
    l.ok = lambda s: ok(5, s)
    def nlog(level, msg, args, exc_info=None, extra=None, stack_info=False):
        if not ok(level, msg): return
        nmsg = f'{prefix[0]} {" ".join(map(str, args))}'
        l.olog(level, nmsg, None, exc_info, extra, stack_info)
    l._log = nlog

    def setPartials(obj, name=0):
        name = name or obj.logname
        obj.debug = partial(l.debug, name)
        obj.info = partial(l.info, name)
        obj.warning = partial(l.warning, name)
        obj.error = partial(l.error, name)
        obj.fatal = partial(l.fatal, name)
        obj.logger = l
        return l
    l.thisClassLogger = setPartials
    return l
