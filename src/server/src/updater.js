var round = (n, d=2, add=0) => (Math.round(n*(10**d))+add)/(10**d)
var hdel = (h, k) => { x=h[k]; delete h[k]; return x }
var between = (min, x, max) => x > max ? max : x <min ? min : x

var Update = class {
  constructor() {
    this.i = 0
  }

  chgNum(sel, val) {
    var el =$(sel); var isn = typeof val == 'number'
    el.html(isn ? Math.round(val) : val)
    isn && val > 0 ? el.removeClass("minus") : el.addClass("minus")
  }

  newMsg(m) {
    var t = this
    while (!t.ok) return setTimeout(t.newMsg.bind(t,m), 10)
    // this.i++; if(this.i>15) return
    // console.log(m);
    // return
    console.log(`================== ${m.cycles} ==============================`)
    startTime = tNow()
    "cycles,info,pnl,fines".split(",").map(x=>t.chgNum(`#${x}-num`, m[x] || m.meta[x] || ""))
    m.assets["IDXPHX"] = hdel(m.assets, "IDX#PHX")

    var sums = {}; var arr = t.lowercharts
    arr.map(x=> {sums[`${x}_pos-num-sum`] = 0.0 } ) // init sums
    t.kcharts.map(k=>t.fillChart(k, m.assets[k], sums)) // update main charts
    arr.map(x=> {
      t.chgNum(`#${x}_pos-num-sum`, sums[`${x}_pos-num-sum`]) // write sums to screen
      m.istest // update history graphs
        ? t.testlower(x, 2)
        : charts[`hist-${x}`].update(sums[`${x}_pos-num-sum`])
    })
    t.afterallcharts(sums)
    t.chgNum(`#trades-num`, t.trades)
    m=0; sums=0
    elapsed("all charts")
  }

  fillChart(k, asset, sums) {
    var t = this
    // console.log(t.assets)
    var h = Object.assign(t.assets[k], asset.status)
    h.name = k // remove the # which screws up everything

    // console.log(h)

    // fill numbers
    t.upperlines.map(x=>t.chgNum(`#${x}-num-${k}`, h[x]*(x==="pos"?1:100)))
    t.lowerlines.map(x=> {
      var n = x !=="pnl" ? (h[x]||(x==="delta"?1:0))* h.pos : h.pnl
       t.chgNum(`#${x}_pos-num-${k}`, n); sums[`${x}_pos-num-sum`] += n
    })

    // draw charts
    var chart = charts[`chart-${h.name}`]; var mm = {min:1000, max:0}
    var data = {orders:[],market:[],fills:[]}; var orders = {}
    Object.keys(data).forEach(typ=>{
      "bids,asks".split(",").forEach(boa=>{
        asset[typ][boa].forEach(x=>{
          mm.min = Math.min(x.price, mm.min); mm.max = Math.max(x.price, mm.max)
          // if(typ==="orders") orders[`${boa}${x.price}`] = x.size
          // if(typ==="market") x.size -= orders[`${boa}${x.price}`] || 0
          if(x.size>0) data[typ].push(Object.assign({K:h.K, flag:h.flag, source:typ, boa:boa}, x))
        })
      })
    })
    setTimeout(()=>{}, 0)
    t.beforeupperchart(k, data, sums)
    chart.remove(".datall").remove(".yaxis").yAxis({domain:[round(mm.min,2,-1), round(mm.max,2,1)]})
    var tt = d=>[`price=${round(d.price,2)}`,`size=${d.size}`,`strike=${d.K?round(d.K):''}`,`source=${d.source}`,`type=${d.boa}`].join("<br/>")
    chart.points(data.market.concat(data.orders).concat(data.fills), {}, tt)
    t.trades += data.fills.length
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
  testlower(name, n) {
    var chart = charts[`hist-${name}`]; var mm = {bids:0, asks:2000}
    var arr = Array.from({length: 50}, () => {
      x=Math.random(); var res = n * (1 + (x>0.5?1:-1)*x/300 )
      mm.bids = Math.max(mm.bids, res); mm.asks = Math.min(mm.asks, res)
      return round(res,2)
    });
    chart.remove(".datall").remove(".yaxis").yAxis({domain:[round(mm.bids,2,-1), round(mm.asks,2,1)]})
    chart.line(arr)
  }
}
