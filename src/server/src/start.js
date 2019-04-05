var startTime=0;
var tNow = () => (new Date()).getTime()
var elapsed = (label) => console.log("==========", tNow() - startTime, label)
var thiscase = location.hash.replace(/^#/, "").toLowerCase()
console.log("thiscase", thiscase)
// var Case2 = Update
var Case = {case1: Case1, case2: Case2}
var updater = new Case[thiscase]()
window.addEventListener("load", function(event) {
  var ws = Ws('ws://'+location.host+"/ws")
})
$(window).on("configok", function(event) {
  console.log("starting.....................")
  Grid( $(".grid") ).all()
})

htuid1 = {
  "action": "newMsg",
  "istest": 1,
  "num": 201,
  "info": "tototo",
  "meta": {"pnl":111, "fines":222},
  "assets": {
    "IDX#PHX": {
      "status": {
        "name": "IDX#PHX",
        "alert": 1,
        "pos": -30,
        "avg": 99.88333384195964,
        "cash": -2989.199981689453,
        "mkt": 100.32,
        "pnl": -3002.2999664306635
      },
      "market": {
        "bids": [
          {
            "price": 100.31,
            "size": 1000
          }
        ],
        "asks": [
          {
            "price": 100.33,
            "size": 1500
          }
        ]
      },
      "orders": {
        "bids": [
          {
            "price": 100.31,
            "quantity": 5,
            "size": 5,
            "order_id": "01D73HECC9BMKTW2H82GBDW97N"
          }
        ],
        "asks": []
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
        "pos": -12,
        "avg": 5.919166803359985,
        "cash": -65.28998899459839,
        "mkt": 6.02,
        "pnl": -66.49998735427856,
        "delta": 0.6,
        "gamma": 0.03,
        "vega": 0.16,
        "sigma": 0.3
      },
      "market": {
        "bids": [
          {
            "price": 6.01,
            "size": 5
          },
          {
            "price": 6,
            "size": 5
          },
          {
            "price": 5.99,
            "size": 5
          },
          {
            "price": 5.98,
            "size": 5
          }
        ],
        "asks": [
          {
            "price": 6.03,
            "size": 2
          },
          {
            "price": 6.04,
            "size": 5
          },
          {
            "price": 6.05,
            "size": 5
          },
          {
            "price": 6.06,
            "size": 5
          },
          {
            "price": 6.07,
            "size": 5
          }
        ]
      },
      "orders": {
        "bids": [],
        "asks": [
          {
            "price": 6.03,
            "quantity": -5,
            "size": 5,
            "order_id": "01D73HECP3TSD0K66ZTT16ZJZV"
          }
        ]
      },
      "fills": {
        "bids": [
          {
            "price": 6.019999980926514,
            "size": 5,
            "quantity": 5
          }
        ],
        "asks": [
          {
            "price": 5.820000171661377,
            "size": 5,
            "quantity": -5
          }
        ]
      }
    },
    "C99PHX": {
      "status": {
        "name": "C99PHX",
        "alert": 1,
        "pos": -24,
        "avg": 4.932916800181071,
        "cash": -118.3900032043457,
        "mkt": 5.495,
        "pnl": -131.88,
        "delta": 0.57,
        "gamma": 0.03,
        "vega": 0.16,
        "sigma": 0.3
      },
      "market": {
        "bids": [
          {
            "price": 5.49,
            "size": 5
          },
          {
            "price": 5.47,
            "size": 3
          },
          {
            "price": 5.41,
            "size": 1
          },
          {
            "price": 5.23,
            "size": 8
          },
          {
            "price": 5.22,
            "size": 10
          }
        ],
        "asks": [
          {
            "price": 5.5,
            "size": 8
          },
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
            "price": 5.41,
            "quantity": 1,
            "size": 5,
            "order_id": "01D73HE1VRGH9VZW22HQBYH6KM"
          },
          {
            "price": 5.47,
            "quantity": 3,
            "size": 5,
            "order_id": "01D73HEB7RMYYC9609JH3YQ861"
          },
          {
            "price": 5.49,
            "quantity": 5,
            "size": 5,
            "order_id": "01D73HECCDS4DNWM5A4AW3FGZK"
          },
          {
            "price": 5.49,
            "quantity": 5,
            "size": 5,
            "order_id": "01D73HECP44AA5PXXJZJR874EE"
          }
        ],
        "asks": []
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
        "pos": -8,
        "avg": 4.558749675750736,
        "cash": -36.46999740600586,
        "mkt": 4.925,
        "pnl": -39.39999999999997,
        "delta": 0.53,
        "gamma": 0.03,
        "vega": 0.16,
        "sigma": 0.29
      },
      "market": {
        "bids": [
          {
            "price": 4.83,
            "size": 2
          },
          {
            "price": 4.82,
            "size": 10
          },
          {
            "price": 4.81,
            "size": 10
          }
        ],
        "asks": [
          {
            "price": 5.02,
            "size": 5
          },
          {
            "price": 5.03,
            "size": 10
          },
          {
            "price": 5.04,
            "size": 10
          }
        ]
      },
      "orders": {
        "bids": [],
        "asks": [
          {
            "price": 4.84,
            "quantity": -5,
            "size": 5,
            "order_id": "01D73HECP6SQPJQWG2R9X0Q6VC"
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
        "pos": 31,
        "avg": 4.639354490464732,
        "cash": 143.81998920440674,
        "mkt": 4.275,
        "pnl": 132.52500000000006,
        "delta": 0.5,
        "gamma": 0.03,
        "vega": 0.16,
        "sigma": 0.28
      },
      "market": {
        "bids": [
          {
            "price": 4.27,
            "size": 11
          },
          {
            "price": 4.26,
            "size": 15
          }
        ],
        "asks": [
          {
            "price": 4.28,
            "size": 10
          },
          {
            "price": 4.38,
            "size": 1
          },
          {
            "price": 4.39,
            "size": 5
          },
          {
            "price": 4.4,
            "size": 5
          }
        ]
      },
      "orders": {
        "bids": [
          {
            "price": 4.27,
            "quantity": 5,
            "size": 5,
            "order_id": "01D73HECP7KN7JKCAVBKWN2PF3"
          }
        ],
        "asks": [
          {
            "price": 4.28,
            "quantity": -5,
            "size": 5,
            "order_id": "01D73HEC2MJF9627ENCPQ9YJEM"
          },
          {
            "price": 4.28,
            "quantity": -5,
            "size": 5,
            "order_id": "01D73HECCG3XS4NX74C08JPXSV"
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
        "pos": -8,
        "avg": 3.256249040365219,
        "cash": -26.049992322921753,
        "mkt": 4.125,
        "pnl": -33,
        "delta": 0.47,
        "gamma": 0.03,
        "vega": 0.16,
        "sigma": 0.3
      },
      "market": {
        "bids": [
          {
            "price": 4.12,
            "size": 10
          },
          {
            "price": 4.1,
            "size": 3
          },
          {
            "price": 4.04,
            "size": 1
          },
          {
            "price": 3.84,
            "size": 15
          }
        ],
        "asks": [
          {
            "price": 4.13,
            "size": 1
          },
          {
            "price": 4.14,
            "size": 10
          },
          {
            "price": 4.15,
            "size": 10
          }
        ]
      },
      "orders": {
        "bids": [
          {
            "price": 4.04,
            "quantity": 1,
            "size": 5,
            "order_id": "01D73HE25NN8TR0SE94VXX9FS1"
          },
          {
            "price": 4.1,
            "quantity": 3,
            "size": 5,
            "order_id": "01D73HEAHN9BT8WX4RW7G4WQEV"
          },
          {
            "price": 4.12,
            "quantity": 5,
            "size": 5,
            "order_id": "01D73HEC2PPQ658ZTVZXG9W09Z"
          },
          {
            "price": 4.12,
            "quantity": 5,
            "size": 5,
            "order_id": "01D73HECCJA2V6DHJ5V85XMKGN"
          }
        ],
        "asks": [
          {
            "price": 4.13,
            "quantity": -5,
            "size": 5,
            "order_id": "01D73HECP9A3V482401H21V0H8"
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
        "pos": -52,
        "avg": 3.7648075177119327,
        "cash": -194.76999068260193,
        "mkt": 3.7649999999999997,
        "pnl": -194.77999976158142,
        "delta": -0.4,
        "gamma": 0.03,
        "vega": 0.16,
        "sigma": 0.3
      },
      "market": {
        "bids": [
          {
            "price": 3.76,
            "size": 18
          },
          {
            "price": 3.75,
            "size": 15
          }
        ],
        "asks": [
          {
            "price": 3.77,
            "size": 5
          },
          {
            "price": 3.8,
            "size": 1
          },
          {
            "price": 3.98,
            "size": 5
          },
          {
            "price": 3.99,
            "size": 10
          }
        ]
      },
      "orders": {
        "bids": [
          {
            "price": 3.76,
            "quantity": 5,
            "size": 5,
            "order_id": "01D73HEB7V49KYN3KQ2H3YX5G3"
          }
        ],
        "asks": [
          {
            "price": 3.8,
            "quantity": -1,
            "size": 5,
            "order_id": "01D73HE8ZQHJ18HJ3SPSJEKP2F"
          },
          {
            "price": 3.77,
            "quantity": -5,
            "size": 5,
            "order_id": "01D73HEC2RMFN2WN9BRXMRAJAD"
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
        "pos": 5,
        "avg": 4.39600019454956,
        "cash": 24.39000415802002,
        "mkt": 4.345,
        "pnl": 24.135003185272218,
        "delta": -0.43,
        "gamma": 0.03,
        "vega": 0.16,
        "sigma": 0.31
      },
      "market": {
        "bids": [
          {
            "price": 4.34,
            "size": 3
          },
          {
            "price": 4.33,
            "size": 10
          },
          {
            "price": 4.32,
            "size": 15
          }
        ],
        "asks": [
          {
            "price": 4.35,
            "size": 3
          },
          {
            "price": 4.41,
            "size": 2
          },
          {
            "price": 4.42,
            "size": 5
          },
          {
            "price": 4.43,
            "size": 5
          },
          {
            "price": 4.44,
            "size": 5
          }
        ]
      },
      "orders": {
        "bids": [
          {
            "price": 4.34,
            "quantity": 3,
            "size": 5,
            "order_id": "01D73HEC2TNGQJ5XFB83HXK8GY"
          },
          {
            "price": 4.34,
            "quantity": 5,
            "size": 5,
            "order_id": "01D73HECPASX3MD54SDNDM7M3H"
          }
        ],
        "asks": [
          {
            "price": 4.35,
            "quantity": -3,
            "size": 5,
            "order_id": "01D73HEB7WEJBGA6Y0CYSV89NZ"
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
        "pos": -28,
        "avg": 4.822857277733937,
        "cash": -132.69000482559204,
        "mkt": 4.765,
        "pnl": -131.0700010490418,
        "delta": -0.47,
        "gamma": 0.03,
        "vega": 0.16,
        "sigma": 0.3
      },
      "market": {
        "bids": [
          {
            "price": 4.76,
            "size": 13
          },
          {
            "price": 4.75,
            "size": 15
          }
        ],
        "asks": [
          {
            "price": 4.77,
            "size": 10
          },
          {
            "price": 4.8,
            "size": 1
          },
          {
            "price": 4.81,
            "size": 3
          },
          {
            "price": 4.91,
            "size": 4
          },
          {
            "price": 4.92,
            "size": 10
          }
        ]
      },
      "orders": {
        "bids": [],
        "asks": [
          {
            "price": 4.81,
            "quantity": -3,
            "size": 5,
            "order_id": "01D73HE6TJTMW98K736918D2GT"
          },
          {
            "price": 4.8,
            "quantity": -1,
            "size": 5,
            "order_id": "01D73HE8P1X3T5CJB8V5PF7SJN"
          },
          {
            "price": 4.77,
            "quantity": -5,
            "size": 5,
            "order_id": "01D73HEC2WAD2BVC71WP7MSQTK"
          },
          {
            "price": 4.77,
            "quantity": -5,
            "size": 5,
            "order_id": "01D73HECCMY05Z8HB8N4DE1K9C"
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
        "pos": 18,
        "avg": 5.7627775934007435,
        "cash": 103.72999668121338,
        "mkt": 5.365,
        "pnl": 96.57,
        "delta": -0.5,
        "gamma": 0.03,
        "vega": 0.16,
        "sigma": 0.31
      },
      "market": {
        "bids": [
          {
            "price": 5.36,
            "size": 8
          },
          {
            "price": 5.35,
            "size": 13
          }
        ],
        "asks": [
          {
            "price": 5.37,
            "size": 8
          },
          {
            "price": 5.39,
            "size": 2
          },
          {
            "price": 5.43,
            "size": 4
          },
          {
            "price": 5.44,
            "size": 10
          }
        ]
      },
      "orders": {
        "bids": [
          {
            "price": 5.36,
            "quantity": 3,
            "size": 5,
            "order_id": "01D73HEC2X24M45X0A1Z4MHKE8"
          },
          {
            "price": 5.36,
            "quantity": 5,
            "size": 5,
            "order_id": "01D73HECCP58KW5SVXW84602KF"
          }
        ],
        "asks": [
          {
            "price": 5.39,
            "quantity": -2,
            "size": 5,
            "order_id": "01D73HE4YTVTNW36YGTDEYW6K0"
          },
          {
            "price": 5.37,
            "quantity": -3,
            "size": 5,
            "order_id": "01D73HEAHVMXD88NBER28XR6Z1"
          },
          {
            "price": 5.37,
            "quantity": -5,
            "size": 5,
            "order_id": "01D73HEB7Z09AZZXS4RQ0M250Y"
          },
          {
            "price": 5.37,
            "quantity": -5,
            "size": 5,
            "order_id": "01D73HECPCMCFMH18WVPWMXMRR"
          }
        ]
      },
      "fills": {
        "bids": [
          {
            "price": 5.360000133514404,
            "size": 2,
            "quantity": 2
          }
        ],
        "asks": []
      }
    },
    "P102PHX": {
      "status": {
        "name": "P102PHX",
        "alert": 1,
        "pos": 71,
        "avg": 6.09943683382491,
        "cash": 433.0600152015686,
        "mkt": 5.92,
        "pnl": 420.32,
        "delta": -0.53,
        "gamma": 0.03,
        "vega": 0.16,
        "sigma": 0.31
      },
      "market": {
        "bids": [
          {
            "price": 5.9,
            "size": 13
          },
          {
            "price": 5.89,
            "size": 15
          }
        ],
        "asks": [
          {
            "price": 5.94,
            "size": 6
          },
          {
            "price": 5.95,
            "size": 5
          },
          {
            "price": 6.04,
            "size": 8
          },
          {
            "price": 6.05,
            "size": 10
          }
        ]
      },
      "orders": {
        "bids": [
          {
            "price": 5.93,
            "quantity": 5,
            "size": 5,
            "order_id": "01D73HECPDKS2Z9R31RJXPNFV3"
          }
        ],
        "asks": [
          {
            "price": 5.95,
            "quantity": -5,
            "size": 5,
            "order_id": "01D73HE8BQXPV7R5K5S8GA4XQW"
          },
          {
            "price": 5.94,
            "quantity": -1,
            "size": 5,
            "order_id": "01D73HE9A9N9N6T3D7QV2CYMD4"
          },
          {
            "price": 5.94,
            "quantity": -5,
            "size": 5,
            "order_id": "01D73HEC30FV8W6ET5F2HZCWGW"
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
      "elapsed": 0.2
    },
    {
      "name": "market",
      "elapsed": 1.3
    },
    {
      "name": "options",
      "elapsed": 5.7
    },
    {
      "name": "traded",
      "elapsed": 0.1
    }
  ]
}
