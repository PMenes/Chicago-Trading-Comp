var Ws = function(url, cb) {
  var t = this; var i
  if (!(t instanceof Ws)) return new Ws(url, cb)
  t.nums = 0
  var WebSocket = window.WebSocket;
  t.ws = new WebSocket('ws://'+location.host+"/ws")
  var num = 0
  t.ws.onopen = function () {
      console.log('socket connection opened properly');
      t.ws.send("iam=client"); // send a message
      setTimeout(function() { t.ws.send("timed out, something is wrong...")}, 100)
      console.log('message sent');
  };

  t.ws.onmessage = function (evt) {
      // console.log("Message received = " + evt.data);
      t.handle(evt.data, num); num += 1
  };

  t.ws.onclose = function () {
      // websocket is closed.
      console.log("Connection closed...");
  };
  if(cb)cb(t.ws)
}

Ws.prototype = {
  constructor: Ws,
  handle: function(msg, n) {
    var t = this
    elapsed("TOTAL")
    startTime = tNow()
    // if(t.nums> 5) return
    console.log("received message", t.nums++)
    try {
        m = JSON.parse(msg)
        if(n===0) console.log(m)
    } catch (e) {
      console.error("could not parse", msg); return
    }
    // console.log("-----------------------------------------------")
    // console.log("-----------------------------------------------")
    // console.log("-----------------------------------------------")
    // console.log("-----------------------------------------------")
    // console.log(JSON.stringify(m,0,4))
    // upd(m)
    elapsed("parse")
    updater[m.action](m)
  }
}

var htuid = {
  "action": "newMsg",
  "num": 121,
  "assets": {
    "IDX#PHX": {
      "status": {
        "name": "IDX#PHX",
        "alert": 1,
        "pos": 5,
        "avg": 100.2900161743164,
        "cash": 501.5000915527344,
        "mkt": 99.985,
        "pnl": 499.97501068115236
      },
      "market": {
        "bids": [
          {
            "price": 99.98,
            "size": 835
          }
        ],
        "asks": [
          {
            "price": 99.99,
            "size": 500
          }
        ]
      },
      "orders": {
        "bids": [
          {
            "price": 99.73,
            "quantity": 0,
            "order_id": "01D732ZANRR6QQVANNJRJDF3P6"
          },
          {
            "price": 99.95,
            "quantity": 5,
            "order_id": "01D732ZWP9TR397VPYFKNH85JK"
          },
          {
            "price": 99.98,
            "quantity": 5,
            "order_id": "01D732ZZEYTCDEN6KMYCZ7K1P3"
          }
        ],
        "asks": [
          {
            "price": 99.74,
            "quantity": 0,
            "order_id": "01D732ZNJNMQ8RZKHCJWXFXWQM"
          },
          {
            "price": 99.78,
            "quantity": 0,
            "order_id": "01D732ZPT96843YB4FYDTWGCFQ"
          },
          {
            "price": 99.86,
            "quantity": 0,
            "order_id": "01D732ZQR9B7BBXJ7S6XEXBHTA"
          },
          {
            "price": 100.01,
            "quantity": 0,
            "order_id": "01D732ZTTRFBBK9W946RNHV078"
          }
        ]
      },
      "fills": {
        "bids": [],
        "asks": []
      }
    },
    "C98PHX": {
      "status": {
        "name": "C98PHX",
        "alert": 1,
        "pos": 21,
        "avg": 6.06619051524571,
        "cash": 128.3400011062622,
        "mkt": 5.8149999999999995,
        "pnl": 123.06500028610229,
        "delta": 0.59,
        "gamma": 0.03,
        "vega": 0.16,
        "sigma": 0.3
      },
      "market": {
        "bids": [
          {
            "price": 5.81,
            "size": 3
          },
          {
            "price": 5.79,
            "size": 3
          },
          {
            "price": 5.76,
            "size": 10
          },
          {
            "price": 5.75,
            "size": 15
          }
        ],
        "asks": [
          {
            "price": 5.82,
            "size": 5
          },
          {
            "price": 5.88,
            "size": 5
          },
          {
            "price": 5.89,
            "size": 5
          },
          {
            "price": 5.9,
            "size": 5
          }
        ]
      },
      "orders": {
        "bids": [
          {
            "price": 5.88,
            "quantity": 0,
            "order_id": "01D732Z9DJFB1HV0AW82A6C2QY"
          },
          {
            "price": 5.88,
            "quantity": 0,
            "order_id": "01D732ZD51Y85V03Y5RK0PM5WZ"
          },
          {
            "price": 5.88,
            "quantity": 0,
            "order_id": "01D732ZDESV0KRD3YA7RXW1MTG"
          },
          {
            "price": 5.81,
            "quantity": 0,
            "order_id": "01D732ZFMPQBCD91T190RCPCNF"
          },
          {
            "price": 5.81,
            "quantity": 0,
            "order_id": "01D732ZHT2JZ65R7E6SJGJ0Y8H"
          },
          {
            "price": 5.8,
            "quantity": 0,
            "order_id": "01D732ZJ430CT2AEH6JQ1HVM3V"
          },
          {
            "price": 6.01,
            "quantity": 0,
            "order_id": "01D732ZQRDXW3CYC38SQ80839R"
          },
          {
            "price": 5.76,
            "quantity": 5,
            "order_id": "01D732ZRZSEPYDCBF0CF6FBKS7"
          },
          {
            "price": 5.79,
            "quantity": 3,
            "order_id": "01D732ZSKFPCZDPHVD6JM1CSAG"
          },
          {
            "price": 5.81,
            "quantity": 3,
            "order_id": "01D732ZTTT7NXEW1SJNP66QT05"
          }
        ],
        "asks": [
          {
            "price": 5.96,
            "quantity": 0,
            "order_id": "01D732Z3J134BTNHSH7T1XGTW8"
          },
          {
            "price": 5.89,
            "quantity": 0,
            "order_id": "01D732Z9Q9994N9WYCDNWZR21E"
          },
          {
            "price": 5.82,
            "quantity": 0,
            "order_id": "01D732ZFABB9KZYTW0AY4DRYG9"
          },
          {
            "price": 5.77,
            "quantity": 0,
            "order_id": "01D732ZRC7DWBQRNRTKM7S7DQV"
          },
          {
            "price": 5.82,
            "quantity": 0,
            "order_id": "01D732ZXXNN4RJWAZ1JVQEBFDM"
          },
          {
            "price": 5.82,
            "quantity": -5,
            "order_id": "01D732ZYVC1Y9Q24Z19VWCF1PY"
          },
          {
            "price": 5.82,
            "quantity": -5,
            "order_id": "01D732ZZF05V7JY09HTSYA6DKN"
          }
        ]
      },
      "fills": {
        "bids": [],
        "asks": []
      }
    },
    "C99PHX": {
      "status": {
        "name": "C99PHX",
        "alert": 1,
        "pos": 15,
        "avg": 5.3833333651224775,
        "cash": 80.25000095367432,
        "mkt": 5.41,
        "pnl": 80.65000047683715,
        "delta": 0.56,
        "gamma": 0.03,
        "vega": 0.16,
        "sigma": 0.3
      },
      "market": {
        "bids": [
          {
            "price": 5.31,
            "size": 10
          },
          {
            "price": 5.3,
            "size": 10
          }
        ],
        "asks": [
          {
            "price": 5.51,
            "size": 10
          },
          {
            "price": 5.52,
            "size": 10
          }
        ]
      },
      "orders": {
        "bids": [
          {
            "price": 5.32,
            "quantity": 0,
            "order_id": "01D732ZCTX2VYAYE00TDG2H693"
          },
          {
            "price": 5.32,
            "quantity": 0,
            "order_id": "01D732ZEPBQHTVVJHJSFSB1FRM"
          },
          {
            "price": 5.49,
            "quantity": 0,
            "order_id": "01D732ZXXP5ZT68PKD53YGHT73"
          },
          {
            "price": 5.5,
            "quantity": 5,
            "order_id": "01D732ZZ57Q3N2ZMQ161PZCQ08"
          }
        ],
        "asks": [
          {
            "price": 5.36,
            "quantity": 0,
            "order_id": "01D732Z94M9Y6VEH43GBREAQTZ"
          },
          {
            "price": 5.3,
            "quantity": 0,
            "order_id": "01D732ZFMRYHV8D94S2GYMPZK3"
          },
          {
            "price": 5.26,
            "quantity": 0,
            "order_id": "01D732ZMM4NYGBE0G77FENDR34"
          },
          {
            "price": 5.33,
            "quantity": 0,
            "order_id": "01D732ZQRFE8EW6QS7KTS3YNSH"
          }
        ]
      },
      "fills": {
        "bids": [],
        "asks": []
      }
    },
    "C100PHX": {
      "status": {
        "name": "C100PHX",
        "alert": 1,
        "pos": -16,
        "avg": 4.6362499594688416,
        "cash": -73.77999496459961,
        "mkt": 4.859999999999999,
        "pnl": -77.35999561309814,
        "delta": 0.52,
        "gamma": 0.03,
        "vega": 0.16,
        "sigma": 0.3
      },
      "market": {
        "bids": [
          {
            "price": 4.85,
            "size": 5
          },
          {
            "price": 4.81,
            "size": 1
          },
          {
            "price": 4.8,
            "size": 10
          },
          {
            "price": 4.79,
            "size": 10
          }
        ],
        "asks": [
          {
            "price": 4.87,
            "size": 10
          },
          {
            "price": 4.88,
            "size": 10
          }
        ]
      },
      "orders": {
        "bids": [
          {
            "price": 4.98,
            "quantity": 0,
            "order_id": "01D732YWWMCWPZN5XMAMCF84F3"
          },
          {
            "price": 4.8,
            "quantity": 0,
            "order_id": "01D732ZJ48FQDHMRBXC7CBY23D"
          },
          {
            "price": 4.75,
            "quantity": 0,
            "order_id": "01D732ZMA7NGPJQ22G7E5FH385"
          },
          {
            "price": 4.84,
            "quantity": 0,
            "order_id": "01D732ZQRJQY66R9DGC99X7597"
          },
          {
            "price": 4.85,
            "quantity": 5,
            "order_id": "01D732ZYVHFY2NWRFHRQK9A5BM"
          },
          {
            "price": 4.86,
            "quantity": 5,
            "order_id": "01D732ZZF1HZPMH7368R2MGJ92"
          }
        ],
        "asks": [
          {
            "price": 4.85,
            "quantity": 0,
            "order_id": "01D732ZAC3KK5NBE1NT50HB0PZ"
          },
          {
            "price": 4.85,
            "quantity": 0,
            "order_id": "01D732ZD54NVN096ARWQ9XZ1W6"
          },
          {
            "price": 4.81,
            "quantity": 0,
            "order_id": "01D732ZF0EWX0CA68X5GFAEN26"
          },
          {
            "price": 4.76,
            "quantity": 0,
            "order_id": "01D732ZKP79WT59GZTPWZG2555"
          },
          {
            "price": 4.76,
            "quantity": 0,
            "order_id": "01D732ZPG7ERYJC33YAGJ9HK11"
          },
          {
            "price": 4.82,
            "quantity": 0,
            "order_id": "01D732ZWPDZ0R000AVF5AGZRRY"
          },
          {
            "price": 4.82,
            "quantity": 0,
            "order_id": "01D732ZXXRJV4E556J4SMV27AB"
          },
          {
            "price": 4.82,
            "quantity": -5,
            "order_id": "01D732ZZ59ZJRG572KBASDJ9G4"
          }
        ]
      },
      "fills": {
        "bids": [],
        "asks": []
      }
    },
    "C101PHX": {
      "status": {
        "name": "C101PHX",
        "alert": 1,
        "pos": 37,
        "avg": 4.559189100523252,
        "cash": 169.739999294281,
        "mkt": 4.445,
        "pnl": 165.5150025749207,
        "delta": 0.49,
        "gamma": 0.03,
        "vega": 0.16,
        "sigma": 0.3
      },
      "market": {
        "bids": [
          {
            "price": 4.44,
            "size": 5
          },
          {
            "price": 4.41,
            "size": 3
          },
          {
            "price": 4.37,
            "size": 3
          },
          {
            "price": 4.31,
            "size": 6
          },
          {
            "price": 4.3,
            "size": 15
          }
        ],
        "asks": [
          {
            "price": 4.45,
            "size": 8
          },
          {
            "price": 4.46,
            "size": 5
          },
          {
            "price": 4.47,
            "size": 5
          },
          {
            "price": 4.48,
            "size": 5
          }
        ]
      },
      "orders": {
        "bids": [
          {
            "price": 4.54,
            "quantity": 0,
            "order_id": "01D732Z8T3Z78PVHT9SHM2T7XY"
          },
          {
            "price": 4.54,
            "quantity": 0,
            "order_id": "01D732ZANVWYPQQSK8DEN4KAY0"
          },
          {
            "price": 4.41,
            "quantity": 0,
            "order_id": "01D732ZD57ZS2DX1Q0KWJHTFDR"
          },
          {
            "price": 4.37,
            "quantity": 3,
            "order_id": "01D732ZRZWN456GKQGS9BNH49Z"
          },
          {
            "price": 4.41,
            "quantity": 3,
            "order_id": "01D732ZWPE8097EZH1Z8PAQBWP"
          },
          {
            "price": 4.44,
            "quantity": 5,
            "order_id": "01D732ZXXSMQAEJGP7VSV0AP3D"
          },
          {
            "price": 4.44,
            "quantity": 5,
            "order_id": "01D732ZZ5A0SCD98S51XJ76094"
          }
        ],
        "asks": [
          {
            "price": 4.55,
            "quantity": -4,
            "order_id": "01D732Z86M52PDSBBCY9246BC1"
          },
          {
            "price": 4.32,
            "quantity": 0,
            "order_id": "01D732ZJ4BG7JCHY069MAMVCEY"
          },
          {
            "price": 4.32,
            "quantity": 0,
            "order_id": "01D732ZMA910910XAF1SXGEQRX"
          },
          {
            "price": 4.45,
            "quantity": -5,
            "order_id": "01D732ZYVK6YZ7QQF1PDGHHN9K"
          }
        ]
      },
      "fills": {
        "bids": [],
        "asks": []
      }
    },
    "C102PHX": {
      "status": {
        "name": "C102PHX",
        "alert": 1,
        "pos": 12,
        "avg": 4.179166754086812,
        "cash": 50.250000953674316,
        "mkt": 3.8899999999999997,
        "pnl": 46.77999990463257,
        "delta": 0.46,
        "gamma": 0.03,
        "vega": 0.16,
        "sigma": 0.29
      },
      "market": {
        "bids": [
          {
            "price": 3.8,
            "size": 15
          },
          {
            "price": 3.79,
            "size": 15
          }
        ],
        "asks": [
          {
            "price": 3.98,
            "size": 8
          },
          {
            "price": 3.99,
            "size": 10
          },
          {
            "price": 4,
            "size": 10
          }
        ]
      },
      "orders": {
        "bids": [
          {
            "price": 3.96,
            "quantity": 0,
            "order_id": "01D732ZC79A4X8KYF6XMQM5Y3F"
          },
          {
            "price": 3.8,
            "quantity": 5,
            "order_id": "01D732ZHT653AS4661XHWFAN6V"
          },
          {
            "price": 3.82,
            "quantity": 0,
            "order_id": "01D732ZKPAB4A6MTH7FA9PSR24"
          },
          {
            "price": 3.82,
            "quantity": 0,
            "order_id": "01D732ZPG88AZ4B8MKVHF4YNQ2"
          }
        ],
        "asks": [
          {
            "price": 3.86,
            "quantity": 0,
            "order_id": "01D732ZFAFZDCMNXKYNY9868C6"
          },
          {
            "price": 3.82,
            "quantity": 0,
            "order_id": "01D732ZHG94KTJEQJ8S6V2D4RK"
          },
          {
            "price": 3.83,
            "quantity": 0,
            "order_id": "01D732ZMM8ZJ8EV3EZDFGW0898"
          },
          {
            "price": 3.83,
            "quantity": 0,
            "order_id": "01D732ZNJRVM4YVR5BVN9M0ZFM"
          },
          {
            "price": 3.81,
            "quantity": -5,
            "order_id": "01D732ZZ5CW35SS3Y5AWW4GTP0"
          },
          {
            "price": 3.81,
            "quantity": -5,
            "order_id": "01D732ZZF22HDC9QAVNXYTNX8H"
          }
        ]
      },
      "fills": {
        "bids": [],
        "asks": []
      }
    },
    "P98PHX": {
      "status": {
        "name": "P98PHX",
        "alert": 1,
        "pos": -59,
        "avg": 3.936440799195888,
        "cash": -232.25000715255737,
        "mkt": 3.885,
        "pnl": -229.21499999999997,
        "delta": -0.41,
        "gamma": 0.03,
        "vega": 0.16,
        "sigma": 0.3
      },
      "market": {
        "bids": [
          {
            "price": 3.88,
            "size": 16
          },
          {
            "price": 3.87,
            "size": 15
          }
        ],
        "asks": [
          {
            "price": 3.89,
            "size": 3
          },
          {
            "price": 3.98,
            "size": 5
          },
          {
            "price": 3.99,
            "size": 5
          },
          {
            "price": 4,
            "size": 8
          }
        ]
      },
      "orders": {
        "bids": [
          {
            "price": 3.94,
            "quantity": 0,
            "order_id": "01D732Z1J8ED20S4CSVF1PYBA3"
          },
          {
            "price": 4.02,
            "quantity": 0,
            "order_id": "01D732Z9QEKEG1GN8WE7BY8QCP"
          },
          {
            "price": 4.1,
            "quantity": 0,
            "order_id": "01D732ZJ4DV87EBZPY5AKZFHMJ"
          },
          {
            "price": 3.88,
            "quantity": 5,
            "order_id": "01D732ZYVPS02ZMHPCE2EJY5A9"
          },
          {
            "price": 3.88,
            "quantity": 5,
            "order_id": "01D732ZZ5ESCWV2TCQSAV0M5S3"
          },
          {
            "price": 3.88,
            "quantity": 5,
            "order_id": "01D732ZZF494RWNWJCB79C9A3A"
          }
        ],
        "asks": [
          {
            "price": 4.03,
            "quantity": 0,
            "order_id": "01D732ZEPCKJF1YB2NXC2B02Z5"
          },
          {
            "price": 4.03,
            "quantity": 0,
            "order_id": "01D732ZFMY2WE3HHQ3T9N8E7B1"
          },
          {
            "price": 4.01,
            "quantity": -5,
            "order_id": "01D732ZPGAFJY1NGK8MBHHGSJS"
          },
          {
            "price": 4,
            "quantity": -3,
            "order_id": "01D732ZQRNSQZ2PC36PM41561Z"
          },
          {
            "price": 4,
            "quantity": -5,
            "order_id": "01D732ZR2229EEQGEGMFD136M1"
          },
          {
            "price": 3.99,
            "quantity": -5,
            "order_id": "01D732ZRCFX0V7P5FGTJ1FW272"
          },
          {
            "price": 3.98,
            "quantity": -5,
            "order_id": "01D732ZRZYYYHCR19WG8ZKS6F7"
          },
          {
            "price": 3.89,
            "quantity": -3,
            "order_id": "01D732ZXXVNRVWG5F0FKYDSJG9"
          }
        ]
      },
      "fills": {
        "bids": [],
        "asks": []
      }
    },
    "P99PHX": {
      "status": {
        "name": "P99PHX",
        "alert": 1,
        "pos": 11,
        "avg": 4.596363457766446,
        "cash": 53.71999931335449,
        "mkt": 4.605,
        "pnl": 53.815001277923585,
        "delta": -0.44,
        "gamma": 0.03,
        "vega": 0.16,
        "sigma": 0.31
      },
      "market": {
        "bids": [
          {
            "price": 4.6,
            "size": 5
          },
          {
            "price": 4.49,
            "size": 1
          },
          {
            "price": 4.48,
            "size": 10
          },
          {
            "price": 4.47,
            "size": 10
          }
        ],
        "asks": [
          {
            "price": 4.61,
            "size": 8
          },
          {
            "price": 4.62,
            "size": 15
          }
        ]
      },
      "orders": {
        "bids": [
          {
            "price": 4.6,
            "quantity": 0,
            "order_id": "01D732ZHTADA4887KE03M4Z76P"
          },
          {
            "price": 4.6,
            "quantity": 0,
            "order_id": "01D732ZRCJG0ZTQXY3E4JZGPQ0"
          },
          {
            "price": 4.6,
            "quantity": 0,
            "order_id": "01D732ZVRHA95YY5AV69Y37C5E"
          },
          {
            "price": 4.6,
            "quantity": 5,
            "order_id": "01D732ZXXWP8BSKKDP8295EB2J"
          }
        ],
        "asks": [
          {
            "price": 4.54,
            "quantity": 0,
            "order_id": "01D732ZD590S1A6WZCSFTSDNYB"
          },
          {
            "price": 4.54,
            "quantity": 0,
            "order_id": "01D732ZDEX8K8HECAWZNACTGEN"
          },
          {
            "price": 4.61,
            "quantity": -3,
            "order_id": "01D732ZJ4E6YV2FKEDSZTYXE06"
          },
          {
            "price": 4.61,
            "quantity": -5,
            "order_id": "01D732ZWPG882JZZQ3M259GHZ9"
          }
        ]
      },
      "fills": {
        "bids": [],
        "asks": []
      }
    },
    "P100PHX": {
      "status": {
        "name": "P100PHX",
        "alert": 1,
        "pos": 5,
        "avg": 4.869999885559082,
        "cash": 31.750010013580322,
        "mkt": 4.835,
        "pnl": 31.575010585784913,
        "delta": -0.48,
        "gamma": 0.03,
        "vega": 0.16,
        "sigma": 0.3
      },
      "market": {
        "bids": [
          {
            "price": 4.83,
            "size": 16
          },
          {
            "price": 4.82,
            "size": 15
          }
        ],
        "asks": [
          {
            "price": 4.84,
            "size": 10
          },
          {
            "price": 4.89,
            "size": 8
          },
          {
            "price": 4.9,
            "size": 10
          }
        ]
      },
      "orders": {
        "bids": [
          {
            "price": 4.88,
            "quantity": 0,
            "order_id": "01D732ZDEYRF5E4QQMA4EXFCKR"
          },
          {
            "price": 5.05,
            "quantity": 0,
            "order_id": "01D732ZKPGS11NMEH1ZW0EWRQ0"
          },
          {
            "price": 5.06,
            "quantity": 0,
            "order_id": "01D732ZMAEM43VDNWH0VWK4FGF"
          },
          {
            "price": 5.06,
            "quantity": 0,
            "order_id": "01D732ZMMASAAQQ3PCRFPJ8ETY"
          },
          {
            "price": 5.07,
            "quantity": 0,
            "order_id": "01D732ZPTTK9MMDPYTJV9BC8HS"
          },
          {
            "price": 4.87,
            "quantity": 0,
            "order_id": "01D732ZS0A97QAQKYXTP7N5EPQ"
          },
          {
            "price": 4.83,
            "quantity": 5,
            "order_id": "01D732ZT782WQWCFRV0S88D8XG"
          }
        ],
        "asks": [
          {
            "price": 4.89,
            "quantity": 0,
            "order_id": "01D732Z9QG9HP2MHNAYA99DQD7"
          },
          {
            "price": 4.89,
            "quantity": 0,
            "order_id": "01D732ZCV0E5ZKW6H0F4Q5HWJE"
          },
          {
            "price": 4.89,
            "quantity": 0,
            "order_id": "01D732ZEPFWYYGMWZQEXPPV2TV"
          },
          {
            "price": 4.89,
            "quantity": 0,
            "order_id": "01D732ZFAKNGE995SW2XQMKJ1S"
          },
          {
            "price": 4.89,
            "quantity": 0,
            "order_id": "01D732ZHTC11JG3NV2DKVH1HNB"
          },
          {
            "price": 5.08,
            "quantity": -5,
            "order_id": "01D732ZRP74QR0GXA257ZTD21W"
          },
          {
            "price": 4.84,
            "quantity": -5,
            "order_id": "01D732ZXXZQ4EZ71HQ3B40TRZC"
          },
          {
            "price": 4.84,
            "quantity": -5,
            "order_id": "01D732ZYVSJR0NPY4XQF4VEW5J"
          }
        ]
      },
      "fills": {
        "bids": [],
        "asks": []
      }
    },
    "P101PHX": {
      "status": {
        "name": "P101PHX",
        "alert": 1,
        "pos": -25,
        "avg": 5.420000076293944,
        "cash": -135.50000190734863,
        "mkt": 5.585,
        "pnl": -139.62500000000003,
        "delta": -0.51,
        "gamma": 0.03,
        "vega": 0.16,
        "sigma": 0.31
      },
      "market": {
        "bids": [
          {
            "price": 5.58,
            "size": 5
          },
          {
            "price": 5.4,
            "size": 11
          },
          {
            "price": 5.39,
            "size": 15
          }
        ],
        "asks": [
          {
            "price": 5.59,
            "size": 9
          },
          {
            "price": 5.6,
            "size": 10
          },
          {
            "price": 5.61,
            "size": 10
          }
        ]
      },
      "orders": {
        "bids": [
          {
            "price": 5.5,
            "quantity": 0,
            "order_id": "01D732Z9QJ9MV9RMBGJENE24RM"
          },
          {
            "price": 5.51,
            "quantity": 0,
            "order_id": "01D732ZB05ZEJYKZJ12NP7SN7V"
          },
          {
            "price": 5.52,
            "quantity": 0,
            "order_id": "01D732ZHGD7FBFB0C5RJ6NZBKC"
          },
          {
            "price": 5.42,
            "quantity": 0,
            "order_id": "01D732ZRCSHNZF4211J49WNST0"
          },
          {
            "price": 5.42,
            "quantity": 0,
            "order_id": "01D732ZTTYX5ZHDXMEQ4RZFSPX"
          },
          {
            "price": 5.57,
            "quantity": 0,
            "order_id": "01D732ZWPHVGH0DP22ESF6ZQ8J"
          },
          {
            "price": 5.58,
            "quantity": 5,
            "order_id": "01D732ZYVW656N7VE4E7SQ0DD2"
          }
        ],
        "asks": [
          {
            "price": 5.43,
            "quantity": 0,
            "order_id": "01D732Z94R2K90T0Y8PEB8VHKM"
          },
          {
            "price": 5.53,
            "quantity": 0,
            "order_id": "01D732ZDF0HH0CXZKDVGPBFW20"
          },
          {
            "price": 5.43,
            "quantity": 0,
            "order_id": "01D732ZS0CQ1CDJ5QTHPFQFS7V"
          },
          {
            "price": 5.43,
            "quantity": 0,
            "order_id": "01D732ZT7AS4N6B5BC2ES2W6N7"
          }
        ]
      },
      "fills": {
        "bids": [],
        "asks": []
      }
    },
    "P102PHX": {
      "status": {
        "name": "P102PHX",
        "alert": 1,
        "pos": 22,
        "avg": 6.286817854101008,
        "cash": 139.25999307632446,
        "mkt": 6.1850000000000005,
        "pnl": 137.0200002861023,
        "delta": -0.54,
        "gamma": 0.03,
        "vega": 0.16,
        "sigma": 0.31
      },
      "market": {
        "bids": [
          {
            "price": 6.18,
            "size": 3
          },
          {
            "price": 6.1,
            "size": 1
          },
          {
            "price": 6.09,
            "size": 5
          },
          {
            "price": 6.08,
            "size": 5
          },
          {
            "price": 6.07,
            "size": 5
          },
          {
            "price": 6.06,
            "size": 5
          }
        ],
        "asks": [
          {
            "price": 6.19,
            "size": 10
          },
          {
            "price": 6.26,
            "size": 14
          }
        ]
      },
      "orders": {
        "bids": [
          {
            "price": 6.14,
            "quantity": 0,
            "order_id": "01D732Z9DNF36PFH4ECH6M71R3"
          },
          {
            "price": 6.24,
            "quantity": 0,
            "order_id": "01D732ZF182ECJGZ3FGVK8HDDV"
          },
          {
            "price": 6.18,
            "quantity": 0,
            "order_id": "01D732ZSKNN70AKY83D9SQ0K4W"
          },
          {
            "price": 6.18,
            "quantity": 3,
            "order_id": "01D732ZXY1N36D80831B5MWKHB"
          }
        ],
        "asks": [
          {
            "price": 6.01,
            "quantity": 0,
            "order_id": "01D732Z9QMSA1A88C9SMZWBHA6"
          },
          {
            "price": 6.26,
            "quantity": -5,
            "order_id": "01D732ZHTF5CVNM7HZGNVPHYVV"
          },
          {
            "price": 6.19,
            "quantity": 0,
            "order_id": "01D732ZKPMR0R8HW835E3HM1SM"
          },
          {
            "price": 6.19,
            "quantity": 0,
            "order_id": "01D732ZNJV50PA8KGV416D4MCZ"
          },
          {
            "price": 6.16,
            "quantity": 0,
            "order_id": "01D732ZRCXVZ77BS6Q38XNQVC2"
          },
          {
            "price": 6.19,
            "quantity": -5,
            "order_id": "01D732ZVRM86AH57EBRJ27P5B9"
          },
          {
            "price": 6.19,
            "quantity": -5,
            "order_id": "01D732ZYVYY0TD928VSQ5ZDAR2"
          },
          {
            "price": 6.19,
            "quantity": -5,
            "order_id": "01D732ZZ5H74R1PFEVJE17ZTEA"
          },
          {
            "price": 6.19,
            "quantity": -5,
            "order_id": "01D732ZZF52ZAJ4CD8WYMSRCFX"
          }
        ]
      },
      "fills": {
        "bids": [],
        "asks": []
      }
    }
  },
  "perf": [
    {
      "name": "fills",
      "elapsed": 0.1
    },
    {
      "name": "market",
      "elapsed": 0.5
    },
    {
      "name": "options",
      "elapsed": 2.5
    },
    {
      "name": "traded",
      "elapsed": 13.5
    }
  ]
}
