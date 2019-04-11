var round = (n, d=2, add=0) => (Math.round((n+add)*(10**d)))/(10**d)
var hdel = (h, k) => { x=h[k]; delete h[k]; return x }
var between = (min, x, max) => x > max ? max : x <min ? min : x

var Update = class {
  constructor() {
    this.i = 0
  }

  chgNum(sel, val) {
    var el =$(sel); var isn = typeof val == 'number'
    m = isn && sel.search("pri")>-1 ? 100 : 1
    el.html(isn ? Math.round(val*m)/m : val)
    isn && val >= 0 ? el.removeClass("minus") : el.addClass("minus")
  }

  init() { // when we receive the config
    var t = this; t.ok = 1
    t.fine_types = "val,max,seconds".split(",")
    $(window).trigger('configok')
  }

  newMsg(m) {
    var t = this
    while (!t.ok) return setTimeout(t.newMsg.bind(t,m), 10)
    // this.i++; console.log(m); if(this.i>15) return
    console.log(`================== ${m.cycles} ==============================`)
    startTime = tNow()
    "cycles,trades,volume,pnl,fines".split(",").map(x=>t.chgNum(`#${x}-num`, m.meta[x]))
    if(m.assets["IDX#PHX"]) m.assets["IDXPHX"] = hdel(m.assets, "IDX#PHX")

    var sums = m.gpos ||{}; var arr = t.lowercharts.names
    t.kcharts.map(k=>t.fillChart(k, m.assets[k], sums)) // update main charts
    t.lowerlines.map(x=> t.chgNum(`#${x}_pos-num-sum`, sums[x])) // write sums to screen

    Object.keys(m.fines).map(n => {
      "val,seconds,max".split(",").map(v => t.chgNum(`#${n}-${v}-num-fines`, m.fines[n][v]) )
    })

    if(charts["hist-pnl"]) charts["hist-pnl"].domain_add = (p) => p* 0.005 // special one
    t.updatelowercharts(m, t)
    t.afterallcharts(m)
    m=0; sums=0
    elapsed("all charts")
  }

  fillChart(k, asset, sums) {
    var t = this
    var h = Object.assign(t.assets[k], asset.status)
    h.name = k // remove the # which screws up everything

    // fill numbers
    t.upperlines.map(x=>t.chgNum(`#${x}-num-${k}`, h[x]*({pos:1,price:1,vpos:1}[x] || 100)))
    // t.lowerlines.map(x=> t.chgNum(`#${x}_pos-num-${k}`, h[x]*(x==="pnl" || x==="price" ? 1 : h.pos)) )
    t.lowerlines.map(x=> t.chgNum(`#${x}_pos-num-${k}`, h[x]*({pnl:1,price:1}[x] || h.pos )) )

    // draw charts
    var chart = charts[`chart-${h.name}`]; var mm = {min:1000, max:0}
    var data = {orders:[],market:[],fills:[]}; var orders = {}
    Object.keys(data).forEach(typ=>{
      "bids,asks".split(",").forEach(boa=>{
        asset[typ][boa].forEach(x=>{
          mm.min = Math.min(x.price, mm.min); mm.max = Math.max(x.price, mm.max)
          if(x.size>0) data[typ].push(Object.assign({K:h.K, flag:h.flag, source:typ, boa:boa}, x))
        })
      })
    })
    setTimeout(()=>{}, 0)
    t.beforeupperchart(k, data, sums, h)
    chart.remove(".datall").remove(".yaxis").yAxis({domain:[round(mm.min,2,-0.01), round(mm.max,2,0.01)]})
    var tt = d=>[`price=${round(d.price,2)}`,`size=${d.size}`,`strike=${d.K?round(d.K):''}`,`source=${d.source}`,`type=${d.boa}`].join("<br/>")
    chart.points(data.market.concat(data.orders).concat(data.fills), {}, tt)
    data=0; setTimeout(()=>{}, 0)
  }

  getmid(mkts) {
    var mm = {bids:0, asks:2000}
    mkts.map(h=> {
      if(h.boa === "bids") mm.bids = Math.max(mm.bids, h.price)
      if(h.boa === "asks") mm.asks = Math.min(mm.asks, h.price)
    })
    if(mm.asks===2000) console.error("no ask!!!!!!!!", mkts)
    if(mm.bids===0) console.error("no bid!!!!!!!!", mkts)
    var ret =  mm.asks===2000 || mm.bids===0 ? 0 :(mm.bids+mm.asks)/2
    return ret
  }
}
