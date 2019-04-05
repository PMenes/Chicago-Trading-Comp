var Case1 = class extends Update {
  constructor() {
    super()
  }

  init(m) { // receive the config
    var t = this; var c = m.data
    t.kcharts = Object.entries(c.case1).sort((a, b) => a[1].n - b[1].n).map(i=>i[0])
    console.log("t.kcharts", t.kcharts)
    t.assets = {}
    t.kcharts.map(k=> {t.assets[k] = t.kcharts[k]})
    t.upperlines = []
    t.lowerlines = "one,pnl".split(",")
    t.lowercharts = t.lowerlines
    t.ok = 1
    t.trades = 0
    $(window).trigger('configok')
  }
  initcharts() {
    // charts["hist-IDXPHX"].domain_add = () => 0.1 // special one
  }
  beforeupperchart(k, data, sums) {
    // if(k==="IDXPHX") {var mid = this.getmid(data.market); if (mid) sums[`IDXPHX_pos-num-sum`] = mid }
  }
  afterallcharts(sums) {
    // this.placeUnd( sums[`IDXPHX_pos-num-sum`])
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
    // t.allcols = ["label","sum"].concat(t.kcharts)
    t.assets = {"IDXPHX":{strike:1}}
    t.koptions.map(k=> {t.assets[k] = c.options[k]})
    t.upperlines = "price,delta,vega,sigma,pos".split(",")
    t.lowerlines = "delta,vega,pnl".split(",")
    t.lowercharts = ["IDXPHX", "delta","vega","pnl"]
    t.ok = 1
    t.trades = 0
    $(window).trigger('configok')
  }
  initcharts() {
    charts["hist-IDXPHX"].domain_add = () => 0.1 // special one
  }
  beforeupperchart(k, data, sums) {
    if(k==="IDXPHX") {var mid = this.getmid(data.market); if (mid) sums[`IDXPHX_pos-num-sum`] = mid }
  }
  afterallcharts(sums) {
    this.placeUnd( sums[`IDXPHX_pos-num-sum`])
  }
  placeUnd(ret) {
    // place the underlying price
    var a1 = [97.5,  98,  98.5,  99,   99.5,  100,  100.5,  101,  101.5,  102]
    var a2 = ["C98","P98","C99","P99","C100","P100","C101","P101","C102","P102"]
    var place = {}
    for (var i = 0; i < a1.length; i++) {
      if(ret-a1[i]<0.5) {place.x=(ret-a1[i])*2; place.chart=a2[i]; break}
    }
    // console.log("--------------ret", ret, place)
    charts[`chart-${place.chart}PHX`].line([0,100], {getx:d => place.x, gety:d => d, "stroke-width":5})
    return ret
  }
}
