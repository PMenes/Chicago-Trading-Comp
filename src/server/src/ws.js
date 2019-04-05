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
    // console.log("received message", t.nums++)
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
