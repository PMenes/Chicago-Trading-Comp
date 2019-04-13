var Case1 = class extends Update {
  constructor() {
    super()
  }

  init(m) { // receive the config
    var t = this; var c = m.data
    t.kcharts = Object.keys(c["case1-ma"])
    // t.assets = t.kcharts
    t.assets = {}
    t.kcharts.map(k=> {t.assets[k] = c["case1-ma"][k]})
    // t.koptions.map(k=> {t.assets[k] = c.options[k]})
    t.upperlines = "price,price_avg,pri_dma,tgt,pos".split(",")
    t.lowerlines = "pnl".split(",")
    t.lowercharts={}
    t.lowercharts.names = []
    t.lowercharts.cols = t.lowercharts.names.map(x=>1)
    t.fines = ["asset", "val"]
    t.fine_types = "K,M,N,Q,U,V,Total".split(",")
    super.init()
  }
  initcharts() {
    Object.keys(charts).map(x => charts[x].dft.radius = (d,i) => between(3, d.size/(d.source === "fills" ? 1 : 2), 20))
  }
  afterGrid() {
    var t = this
    console.log("afterGrid")
    t.fine_types.map(x=>$(`#asset-${x}-num-fines`).html(x))
    updater.fines.map((n, x)=> $(`#${n}-name-num-fines`).html(`${n}`))
  }
  updatelowercharts(m, t) {
  }
  beforeupperchart(k, data, m) {
  }
  afterallcharts(m) {
    var t = this; var tot = 0
    t.fine_types.map(x=>{
      var v = m.limits[x] || 0; tot += v
      t.chgNum(`#val-${x}-num-fines`, v)
      // $(`#val-${x}-num-fines`).html(v)
    })
    $(`#val-Total-num-fines`).html(tot)
  }
  fillChart(k, asset, sums) {
    var t = this
    var h = Object.assign(t.assets[k], asset.status)
    h = asset.status
    Object.assign(h, {price:h.cur, price_avg:h.avg, pri_dma:h.dma, tgt:h.tgt, name: k})

    // fill numbers
    t.upperlines.map(x=>t.chgNum(`#${x}-num-${k}`, h[x]))
    t.lowerlines.map(x=> t.chgNum(`#${x}_pos-num-${k}`, h[x]*({pnl:1,price:1}[x] || h.pos )) )

    // draw charts
    var chart = charts[`chart-${h.name}`]; var mm = {min:asset.status.avg-0.4, max:asset.status.avg+0.4}
    var data = {orders:[],market:[],fills:[]}; var orders = {}

    data.market.push({source:"market", boa:"asks", price:h.avg, size:10})
    if (h.pos < 0) data.orders.push({source:"fills", boa:"asks", price:h.cur, size:Math.abs(h.pos)})
    if (h.pos >= 0) data.orders.push({source:"fills", boa:"bids", price:h.cur, size:Math.abs(h.pos)})
    setTimeout(()=>{}, 0)
    t.beforeupperchart(k, data, sums, h)
    if(!chart.doneAxis) {chart.remove(".yaxis").yAxis({domain:[round(mm.min,2,-0.01), round(mm.max,2,0.01)]}), chart.doneAxis=1}
    chart.remove(".datall") //.remove(".yaxis").yAxis({domain:[round(mm.min,2,-0.01), round(mm.max,2,0.01)]})
    var tt = d=>[`price=${round(d.price,2)}`,`size=${d.size}`,`strike=${d.K?round(d.K):''}`,`source=${d.source}`,`type=${d.boa}`].join("<br/>")
    chart.points(data.market.concat(data.orders).concat(data.fills), {}, tt)
    data=0; setTimeout(()=>{}, 0)
  }

}

var Case11 = class extends Update {
  constructor() {
    super()
  }

  init(m) { // receive the config
    var t = this; var c = m.data
    t.kcharts = Object.entries(c.case1).sort((a, b) => a[1].n - b[1].n).map(i=>i[0])
    t.assets = {}
    t.kcharts.map(k=> {t.assets[k] = c.case1[k]})
    // t.koptions.map(k=> {t.assets[k] = c.options[k]})
    t.upperlines = []
    t.lowerlines = "price,one,pnl".split(",")
    t.lowercharts={}
    t.lowercharts.names = "pnl,one,K,M,N,Q,U,V".split(",")
    t.lowercharts.cols = t.lowercharts.names.map(x=>1)
    t.fines = ["one"]
    super.init()
  }
  initcharts() {
    "K,M,N,Q,U,V".split(",").map(x => charts[`hist-${x}`].domain_add = () => 0.1)
  }
  updatelowercharts(m, t) {
    "K,M,N,Q,U,V".split(",").map(x => charts[`hist-${x}`].update(m.assets[x].status.price) )
    "pnl,one".split(",").map(x => charts[`hist-${x}`].update(m.gpos[x]))
  }
  beforeupperchart(k, data, m) {
  }
  afterallcharts(m) {
  }
}

var Case2 = class extends Update {
  constructor() {
    super()
  }

  init(m) { // receive the config
    var t = this; var c = m.data
    t.koptions = Object.entries(c.options).sort((a, b) => a[1].K - b[1].K).map(i=>i[0])
    t.kcharts = ["IDXPHX"].concat(t.koptions)
    t.assets = {"IDXPHX":{strike:1}}
    t.koptions.map(k=> {t.assets[k] = c.options[k]})
    t.upperlines = "price,delta,vega,sigma,pos,vpos,pri".split(",")
    t.lowerlines = "delta,vega,pnl,gamma".split(",")
    t.lowercharts = {}
    t.lowercharts.names = ["IDXPHX", "delta","vega","pnl"]
    t.lowercharts.cols = [3,3,3,4]
    t.fines = ["delta", "vega"]
    super.init()
  }
  initcharts() {
    charts["hist-IDXPHX"].domain_add = () => 0.05 // special one
  }
  beforeupperchart(k, data, sums, h) {
    if(k==="IDXPHX") sums.IDXPHX = h.price || h.mkt
  }
  updatelowercharts(m) {
    this.lowercharts.names.map(x => charts[`hist-${x}`].update(m.gpos[x]))
  }
  afterallcharts(m) {
    this.placeUnd(this.assets.IDXPHX.price)
  }
  placeUnd(ret) {
    // place the underlying price
    var a1 = [97.5,  98,  98.5,  99,   99.5,  100,  100.5,  101,  101.5,  102]
    var a2 = ["C98","P98","C99","P99","C100","P100","C101","P101","C102","P102"]
    var place = {}
    for (var i = 0; i < a1.length; i++) {
      if(ret-a1[i]<0.5) {place.x=(ret-a1[i])*2; place.chart=a2[i]; break}
    }
    charts[`chart-${place.chart}PHX`].line([0,100], {getx:d => place.x, gety:d => d, "stroke-width":5})
    return ret
  }
}
