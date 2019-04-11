var Case1 = class extends Update {
  constructor() {
    super()
  }

  init(m) { // receive the config
    var t = this; var c = m.data
    t.kcharts = Object.entries(c.case1).sort((a, b) => a[1].n - b[1].n).map(i=>i[0])
    console.log("t.kcharts", t.kcharts)
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
