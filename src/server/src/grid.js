var Grid = function(container) {
  var t = this; var i
  if (!(t instanceof Grid)) return new Grid(container)
  t.container = container
  t.arr = []
  t.cur = {r: 1, c:1, sr:1, sc:1, mr:1, mc:1}
  t.cols = updater.kcharts
  return t
}

Grid.prototype = {
  constructor: Grid,
  all() { this.generate().build().fill().startCharts().formatGrid() },
  box: function(n, nh) {
    var t = this
    var h = {r: nh.r || t.cur.r, c:nh.c || t.cur.c, sr:nh.sr || 1, sc:nh.sc || 1, n:n}
    // var fill = nh.chart ? `<svg id="c-${h.n}"></svg>` : h.n
    h.html = `<div id="${h.n}" class="bb box ${nh.chart ? "chart" : ''} ${h.n.split("-").join(" ")}">${h.n}</div>`
    h.css = `\n#${h.n} {
        grid-column: ${h.c} / span ${h.sc};
        grid-row: ${h.r} / span ${h.sr};
      }`
    t.arr.push(h)
    var c = h.c + h.sc; t.cur.mc = c > t.cur.mc ? c : t.cur.mc
    var r = h.r + h.sr; t.cur.mr = r > t.cur.mr ? r : t.cur.mr
  },
  line: function(n, h={}) {
    var t = this; nh = {r:h.r || t.cur.mr, c:h.c || 3, sr:h.sr || 1, sc:h.sc || 1};
    var i; cols = h.cols || t.cols; nh.c -= nh.sc
    for(i=0; i<cols.length; i++) t.box(`${n}-${cols[i]}`, {r: nh.r, c:(nh.c+=nh.sc), sr:nh.sr, sc:nh.sc, chart:h.chart})
  },
  build: function() {
    var t = this
    var ur = `${Math.round(($(document).height()-t.cur.mr)/t.cur.mr*100)/100}px`
    var uc = `${Math.round(($(document).width()-t.cur.mc)/t.cur.mc*100)/100}px`
    var css = []; var html = []
    css.push(`\n.wrapper {
  		display: grid;
      grid-gap: 0px;
  		grid-template-columns: repeat(${t.cur.mc}, [col] ${uc} ) ;
  		grid-template-rows: repeat(${t.cur.mr}, [row] ${ur}  );
  	}`)
    $.each(t.arr, function(i, h) {css.push(h.css); html.push(h.html)})
    $("head").append(`<style>${css.join("\n")}\n</style>`)
    t.container.append(`<div class="wrapper">\n${html.join("\n")}\n</div>\n`)
    return t
  },
  generate: function() {
    var t = this; var r
    t.line("title", {sr:2})
    $.each(updater.upperlines, (i, v) => t.line(`${v}-num`))
    r = t.cur.mr
    t.line("chart", {r:r, sr:20, sc:1, chart:1})
    r = t.cur.mr
    updater.lowerlines.map(v=> t.line(`${v}_pos-num`))
    r = t.cur.mr
    // t.box("hist-IDXPHX", {r:r, c:1, sr:8, sc:3, chart:1})
    t.line("hist", {r:r, c:1, sr:6, sc:3, chart:1, cols:updater.lowercharts })

    updater.lowerlines.map((v,i) => { t.box(`${v}-label`, {r: i+3, c:1, sc:2}) })
    // "price,delta,vega,sigma,pos".split(",").map((v,i) => { t.box(`${v}-label`, {r: i+3, c:1, sc:2}) })
    updater.lowerlines.map((v,i)=> t.line(`${v}_pos`, {r: 28+i, c:1, cols:["label", "num-sum"]}))
    r = 9
    "cycles,trades,info,pnl,fines".split(",").map((v,i)=>{
      t.line(`${v}`, {r:r+i*2, sr:2, c:1, cols:["label", "num"]})
    })
    // t.box("cycles", {r: 1, c:1, sc:2, sr:2})
    // t.box("info", {r: 9, c:1, sc:2, sr:2})
    // t.box("pnl", {r: 11, c:1, sc:2, sr:2})
    // t.box("fines", {r: 13, c:1, sc:2, sr:2})

    return t
  },
  fill: function() {
    x = $('.title')
    x.css('text-align', 'center');
    x.each(function(i, el) {
      $(el).html(el.id.split("-")[1])
    })
    return this
  },
  startCharts: function() {
    var t = this; var x
    updater.kcharts.map(k=> {
      Charts[`chart-${k}`] = class extends Charts.Big {}
    })
    updater.lowercharts.map(k=>{
      Charts[`hist-${k}`] = class extends Charts.Lower {}
    })

    t.container.find(".chart").each((i,c) => {
      if (Charts[c.id]) {
        x = charts[c.id] = new Charts[c.id](`#${c.id}`)
        x.start()
      }
    })
    updater.initcharts()
    return this
  },
  formatGrid: function() {
    var t = this; var x
    $(".label").each((i,el)=>$(el).html(el.id.split("-")[0]+":"))
    updater.newMsg(htuid)
    return this
  }
}
