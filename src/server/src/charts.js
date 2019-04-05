var Charts = {}; var charts = {}

Charts.Big = class extends Chart {
  start(opt={}) {
    var t = this
    var o = {
      domains:{x:[0,1], y:[100,100.3]}
      , margin: {top: 0, right: 1, bottom: 0, left: 1}
      // , tickValues: {x:[0.65]}
    }
    super.start(o)
    // t.tickSize = {x: -t.height}
    t.dft = Object.assign(t.dft, {
        radius: (d,i) => between(3, d.size/(d.source === "fills" ? 2 : 2), 20)
      , getx: (d,i) => ({market:0.1, orders:0.5, fills:0.9}[d.source])
      , gety: (d,i) => d.price
      , fill: (d,i) => d.boa === "bids"?(d.source==="fills"?"blue":"DarkCyan"):(d.source==="fills"?"red":"IndianRed")
      , pointType: (d) => ("symbol" + ({market:"Circle", fills:"Diamond", orders:"Square"}[d.source]))
    })
    t.xAxis().yAxis()
    return t
  }
}

Charts.Lower = class extends Chart {
  start(opt={}) {
    var t = this
    var o = {
      domains:{x:[0,50], y:[-25, 25]}
      , margin: {top: 0, right: 1, bottom: 0, left: 1}
      // , tickValues: {x:[0.65]}
    }
    // for updating
    t.hist = []; t.always = {getx:(d, i) => i, gety:(d, i) => d};
    t.domain_add = (p) => p * 0.1

    super.start(o)
    // t.tickSize = {x: -t.height}
    var ot={height:20, color:"yellow", title:t.selector.replace(/^.*-/, "")} // write the title
    t.title(ot).xAxis().yAxis({nbTicks:4})
    t.cycles = 0
    return t
  }
  update(p) {
    var t = this; var changed = 0; t.cycles++
    var redo = ()=>{
      t.bids = 100000000; t.asks = -100000000
      t.hist.map(i => { t.bids = i < t.bids ? i : t.bids; t.asks = i > t.asks ? i : t.asks })
      changed = 1; var add = t.domain_add(p); t.bids = round(t.bids,2,-add); t.asks = round(t.asks,2,add)
    }
    if(!t.hist.length) { t.bids=t.asks=p; redo()}
    if(p<t.bids || p>t.asks) redo()
    if(!changed && t.cycles % 10 === 0) redo()
    t.hist.push(p);
    if(t.hist.length>50) t.hist.shift()
    if (changed) t.remove(".yaxis").yAxis({domain:[t.bids, t.asks], nbTicks:4})
    t.remove(".datall").line(t.hist, t.always)
  }
}
