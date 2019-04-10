var Ws = function(url, cb) {
  var t = this
  if (!(t instanceof Ws)) return new Ws(url, cb)
  t.ws = new window.WebSocket('ws://'+location.host+"/ws")
  var num = 0
  t.ws.onopen =  () => {
      console.log('socket connection opened properly');
      t.ws.send("iam=client"); // send a message
      setTimeout(function() { t.ws.send("timed out, something is wrong...")}, 100)
      console.log('message sent');
  }
  t.ws.onmessage = evt =>  t.handle(evt.data, num++)
  t.ws.onclose =  () => console.log("Connection closed...")  // websocket is closed.
  if(cb)cb(t.ws)
}

Ws.prototype = {
  constructor: Ws,
  handle: function(msg, n) {
    var t = this
    elapsed("TOTAL"); startTime = tNow()
    try {
        m = JSON.parse(msg); if(n===0) console.log(m)
    } catch (e) {
      console.error("could not parse", msg); return
    }
    elapsed("parse")
    updater[m.action](m)
  }
}
