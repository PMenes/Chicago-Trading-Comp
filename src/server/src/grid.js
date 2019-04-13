var Grid = function(container) {
  var t = this; var i
  if (!(t instanceof Grid)) return new Grid(container)
  t.container = container
  t.arr = []
  t.cur = {r: 1, c:1, sr:1, sc:1, mr:1, mc:1}
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
    var c = t.cur.c = h.c + h.sc; t.cur.mc = c > t.cur.mc ? c : t.cur.mc
    var r = t.cur.r = h.r + h.sr; t.cur.mr = r > t.cur.mr ? r : t.cur.mr
    return r
  },
  line: function(n, h={}) {
    var t = this; nh = {r:h.r || t.cur.r, c:h.c || t.dft.c || 1, sr:h.sr || 1, sc:h.sc || 1};
    cols = h.cols || t.dft.cols;  nh.scs = h.scs || cols.map(x=>nh.sc); nc=nh.c
    nh.scs.map((v,i)=> t.box(`${n}-${cols[i]}`, {r: nh.r, c:nc, sr:nh.sr, sc:v, chart:h.chart}, nc+=v))
    return t.cur.r
  },
  build: function() {
    var t = this
    var ur = `${Math.round(($(document).height())/t.cur.mr)}px`
    var uc = `${Math.round(($(document).width())/t.cur.mc)}px`
    var css = []; var html = []
    css.push(`\n.wrapper {
  		display: grid;
      column-gap: 3px;
  		grid-template-columns: repeat(${t.cur.mc}, [col] ${uc} ) ;
  		grid-template-rows: repeat(${t.cur.mr}, [row] ${ur}  );
  	}`)
    $.each(t.arr, function(i, h) {css.push(h.css); html.push(h.html)})
    $("head").append(`<style>${css.join("\n")}\n</style>`)
    t.container.append(`<div class="wrapper">\n${html.join("\n")}\n</div>\n`)
    return t
  },
  generate: function() {
    var t = this; var kp={}; var u = updater; ul = u.lowercharts
    t.dft = {c:3, cols:updater.kcharts}
    // console.log(t.dft)
    kp.r1 = t.line("title", {sr:2})
    u.upperlines.map((v,i) => t.line(`${v}-num`) )
    kp.r2 = t.line("chart", {sr:20, chart:1})
    kp.r3 = u.lowerlines.map(v=> t.line(`${v}_pos-num`))

    r = 9; "cycles,trades,volume,pnl,fines".split(",").map((v,i)=>{
      t.line(`${v}`, {r:r+i, sr:1, c:1, cols:["label", "num"]})
    })
    r = 15; u.fines.map((n, x)=> {
      ;["name"].concat(u.fine_types).map((v, i) => t.box(`${n}-${v}-num-fines`, {r: r+i, c:1+x}))
    })

    t.dft = {c:1, cols:["label", "num-sum"]}
    u.upperlines.map((v,i) => t.line(`${v}-label`, {r: kp.r1+i, sc:2, cols:["label"]}) )
    u.lowerlines.map((v,i)=> t.line(`${v}_pos`, {r: kp.r2+i}))
    t.line(`hist`, {sr:6, chart:1, cols:ul.names, scs:ul.cols})
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
    updater.lowercharts.names.map(k=>{
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
    updater.newMsg(ht[thiscase])
    $("#pnl-label").html("Xch pnl:")
    $("#fines-label").html("Xch fines:")
    updater.fines.map((n, x)=> {
      $(`#${n}-name-num-fines`).html(`${n} fines`)
    })
    updater.afterGrid()
    return this
  }
}
