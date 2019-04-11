config = {
  "env": "dev", # change to "prod" to prevent throwing
  "fast": 0, # todo
  "shared_key":"tototo", # todo
  "rtt": 0, # dev only, mock round-trip time, change to 0 on real competition or real server
  "exchange":{
    # "host": "ec2-18-188-121-233.us-east-2.compute.amazonaws.com",
    "host": "localhost",
    "port": "50052"
  },
  "limits": { # internal limits
    "delta": 5,
    "vega": 20,
    "one": 20
  },
  "limits-fined": { # real competition limits
    "delta": 25,
    "vega": 25,
    "one": 50
  },
  "groups": { # grouped launch, for "run" or "multi_starter.py"
    "case1": ["case1.par", "case_one_bot.par", "distributor.py"],
    "case2": ["case2.par", "case_two_bot.par", "distributor.py"]
    # "case2": ["distributor.py"]
  },
  "processes": {
    "case2.par": {
        "start": "cd exchange/server/continuous_exchange && ln -sf __n__.textproto exchangeconfig.textproto &&  cd ../.. && ln -sf __n__.json price_setter_config.json && python __n__ > /dev/null 2>&1 &"
    },
    "case_two_bot.par": {
        "start": "cd exchange && python __n__ > /dev/null 2>&1 &"
    },
    "case1.par": {
      "start": "cd exchange/server/continuous_exchange && ln -sf __n__.textproto exchangeconfig.textproto &&  cd ../.. && ln -sf __n__.json price_setter_config.json && python __n__ > /dev/null 2>&1 &"
    },
    "case_one_bot.par": {
        "start": "cd exchange && python __n__ > /dev/null 2>&1 &"
    },
    "distributor.py": { # distributes the processed fill for display on browser
        "port":"5046",
        "host": "0.0.0.0",
        "static_path": "src/server",
        "get_path": "",
        "start": "mkdir -p .logs && python __n__ > .logs/__n__.log 2>&1 &"
    },
    "market_maker.py": {
      "start": "python __n__ &",
      "strategy": "christian",
      "client_id": "baruch1",
      "client_pk": "mm",
      "connect_to": ["distributor.py"], # to see the startegy running on the browser
      "loggers":[
          {"typ": "console", "filters": "main|P102PHX|C98PHX", "level":"DEBUG"}
          ,{"typ": "file", "filename":".logs/market_maker.py.txt", "level":"DEBUG", "filters": "main|P102PHX|C98PHX"}
      ],
      "modify": "mock_modify_order", # real_ || mock_ : what modif function to use (can't get modify_order to work)
      "strategies": {
        "random": { "better": 0.01, "quantity": 1 }, # default strategy
        "paul": { "bound": 5 },
        "christian": { "quantity": 6 }
      }
    },
    "case1.py": {
      "start": "python __n__ &",
      "strategy": "christian",
      "client_id": "",
      "client_pk": "",
      "connect_to": ["distributor.py"],
      "strategies": {
        "random": { "better": 0.01, "quantity": 1 },
        "paul": { "bound": 5 },
        "christian": { "quantity": 10, "better":0 }
      }
    },
    "xcpt1.py": {
      "start": "python __n__ > .logs/__n__.log 2>&1 &",
      "strategy": "christian",
      "client_id": "cp1",
      "client_pk": "cp1",
      "connect_to": [],
      "strategies": {
        "random": { "better": 0.01, "quantity": 1 },
        "paul": { "bound": 5 },
        "christian": { "quantity": 15 }
      }
    },
    "xcpt2.py": {
      "start": "python __n__ > .logs/__n__.log 2>&1 &",
      "strategy": "random",
      "client_id": "cp2",
      "client_pk": "cp2",
      "connect_to": [],
      "strategies": {
        "random": { "better": 0.01, "quantity": 1 },
        "paul": { "bound": 5 },
        "christian": { "quantity": 15 }
      }
    }
  },
  "underlying":"IDX#PHX",
  "options": {
    "C98PHX" : {"flag":"c", "K":98},
    "C99PHX" : {"flag":"c", "K":99},
    "C100PHX" : {"flag":"c", "K":100},
    "C101PHX" : {"flag":"c", "K":101},
    "C102PHX" : {"flag":"c", "K":102},
    "P98PHX" : {"flag":"p", "K":98},
    "P99PHX" : {"flag":"p", "K":99},
    "P100PHX" : {"flag":"p", "K":100},
    "P101PHX" : {"flag":"p", "K":101},
    "P102PHX" : {"flag":"p", "K":102}
  },
  "case1": {
    "K" : {"flag":"May", "n":5},
    "M" : {"flag":"June", "n":6},
    "N" : {"flag":"July", "n":7},
    "Q" : {"flag":"August", "n":8},
    "U" : {"flag":"September", "n":9},
    "V" : {"flag":"October", "n":10}
  }
}
