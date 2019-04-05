var nanoid = function (size, url='Uint8ArdomValuesObj012345679BCDEFGHIJKLMNPQRSTWXYZ_cfghkpqvwxyz-') {
  size = size || 21
  var crypto = self.crypto || self.msCrypto
  var id = ''
  var bytes = crypto.getRandomValues(new Uint8Array(size))
  while (0 < size--) {
    id += url[bytes[size] & 63]
  }
  return id
}

var Chart = class {
  constructor(sel) {
    var t = this
    t.name = sel.replace(/#+|\.+/, "")
    t.selector = sel
    t.obj = $(sel); t.obj.html("")
    t.container = d3.select(sel)
    t.nums = { line:0, circle:0 }
    t.titleHeight = 0
    t.dft = {
        getx:(d, i) => d.x
      , gety:(d, i) => d.y
      , radius:(d, i) => 5
      , pointType: (d,i) => "symbolCircle"
    }
    t.notattrs = {getx:1,gety:1,radius:1,pointType:1}
    t.r = () => t // sugar
  }

  start(opt={}) {
    var t = this
    var deft = {
      name:`c${nanoid(9)}`
      // , dWidth: t.container.attr("width")
      // , dHeight: t.container.attr("height")
      , dWidth: t.obj.width() || t.container.attr("width")
      , dHeight: -t.titleHeight + t.obj.height() || t.container.attr("height")
      , margin: {top: 0, right: 1, bottom: 20, left: 1}
    }
    opt = Object.assign(deft, opt)
    Object.entries(opt).forEach(e => t[e[0]] = e[1])
    t.width = t.dWidth - t.margin.left - t.margin.right // Use the window's width
    t.height = t.dHeight - t.margin.top - t.margin.bottom // Use the window's height

    // Define the div for the tooltip
    t.div = d3.select("body").select("div.tooltip")
    // t.div = d3.select("body").append("div")
    //     .attr("class", "tooltip")
    //     .style("opacity", 0);

    t.svg = t.container.append("svg")
        .attr("width", t.width + t.margin.left + t.margin.right)
        .attr("height", t.height + t.margin.top + t.margin.bottom)
        .attr("class", t.name)
        .append("g")
        .attr("transform", "translate(" + t.margin.left + "," + t.margin.top + ")");
    return t
  }

  title(opt={}){
    var t = this; t.titleHeight = opt.height
    var s = `<div height=${opt.height} style="width:100%;text-align:center;background-color:${opt.color}">${opt.title}</div>`
    t.obj.prepend(s); return t
  }

  xAxis(opt={}) {
    var t = this
    t.xScale = d3.scaleLinear()
        .domain(opt.domain || t.domains.x) // input
        .range([0, t.width]); // output

    var x = d3.axisBottom(t.xScale)
    if(t.tickValues && t.tickValues.x) x.tickValues(t.tickValues.x)
    if(t.tickSize && t.tickSize.x) x.tickSize(t.tickSize.x)
    if(opt.nbTicks) x.ticks(opt.nbTicks)

    if(opt.hide) return t

    t.svg.append("g")
        .attr("class", `${t.name} axes xaxis`)
        .attr("stroke-dasharray", "8, 0")
        .attr("transform", "translate(0," + t.height + ")")
        // .call(d3.axisBottom(t.xScale)); // Create an axis component with d3.axisBottom
        .call(x); // Create an axis component with d3.axisBottom
    return t
  }

  yAxis(opt={}) {
    var t = this
    t.yScale = d3.scaleLinear()
        .domain(opt.domain || t.domains.y) // input
        .range([t.height, 0]) // output

    var x = d3.axisRight(t.yScale).tickSize(t.width)
    if(opt.nbTicks) x.ticks(opt.nbTicks)

    t.svg.append("g")
      .attr("class", `${t.name} axes yaxis`)
      .attr("stroke", "#777").attr("stroke-dasharray", "1,5")
      .call(x) // Create an axis component with d3.axisLeft
      .selectAll(".tick text").attr("x", 4).attr("dy", -4)
    return t
  }

  upd(dataset) {}

  optDefault(opt, prms, typ) {
    var t = this; opt.attrs = {}
    var cls = `${typ}${t.nums[typ]}`; t.nums[typ]++
    Object.keys(prms).concat(Object.keys(t.dft)).map((k, h) => {
       h = t.notattrs[k] ? opt : opt.attrs; h[k] = prms[k] || t.dft[k]
    })
    // console.log("opt=",opt)
    opt.attrs.class = `${t.name} datall ${typ} ${cls} ${prms.class || ''}`.trim()
    return cls
  }

  line(dataset, prms={}) {
    var t = this; var opt={}
    var cls = t.optDefault(opt, prms, "line")

    var line = d3.line()
        // .x((d,i) => { var g = t.xScale(opt.getx(d, i)); console.log("x",g, opt.getx(d, i)); return g})
        // .y((d,i) => { var g = t.yScale(opt.gety(d, i)); console.log("y",g, opt.gety(d, i)); return g})
        .x((d, i) => t.xScale(opt.getx(d, i))) // set the x values for the line generator
        .y((d, i) => t.yScale(opt.gety(d, i))) // set the y values for the line generator
        .curve(d3.curveMonotoneX) // apply smoothing to the line

    var x = t.svg.append("path")
        .datum(dataset) // 10. Binds data to the line
        .attr("fill", "none")
        .attr("stroke", "black")

    Object.entries(opt.attrs).forEach(e => x.attr(e[0], e[1]))
    x.attr("d", line); // 11. Calls the line generator
    return t
  }

  points(dataset, prms={}, tooltip) {
    if(!dataset.length) return
    var t = this; var opt={}
    var cls = t.optDefault(opt, prms, "circle")

    var f = 3
    if(f===0) { // old way ...
      var x = t.svg.selectAll(`.${cls}`)
          .data(dataset)
          .enter().append("circle") // Uses the enter().append() method
          // .attr("cx", (d,i) => { var g = t.xScale(opt.getx(d, i)); console.log("cx",g, opt.getx(d, i)); return g})
          // .attr("cy", (d,i) => { var g = t.yScale(opt.gety(d, i)); console.log("cy",g, opt.gety(d, i)); return g})
          // .attr("r", (d,i) => { var g = opt.radius(d,i); console.log("r",g, opt.radius(d,i)); return g})
          .attr("cx", (d,i) => t.xScale(opt.getx(d,i)))
          .attr("cy", (d,i) => t.yScale(opt.gety(d,i)))
          .attr("r", (d,i) => opt.radius(d,i))
    }
    if(f===3) { // new way, need transform, for some reason cannot integrate symbols with the other way
      var symbol = d3.symbol().size(500)
      var x = t.svg.selectAll(".path")
        .data(dataset)
        .enter().append("path") // Uses the enter().append() method
        .attr('transform', d => `translate(${[t.xScale(opt.getx(d)), t.yScale(opt.gety(d))]})`)
        .attr("r", (d,i) => opt.radius(d,i))
        .attr("d", (d, i) => symbol.type(d3[opt.pointType(d)]).size((opt.radius(d,i)*2)**2)())
    }
    if( tooltip ) {
      x.on("mouseover", function(d, b, c) {
        t.div.transition().duration(200).style("opacity", .9);
        t.div.html(tooltip(d))
            .style("left", (d3.event.pageX) + "px")
            .style("top", (d3.event.pageY - 28) + "px");
      })
      .on("mouseout", function(d) {
          t.div.transition().duration(500).style("opacity", 0);
      });
    }
    Object.entries(opt.attrs).forEach(e => x.attr(e[0], e[1]))
    return t
  }

  remove(sel) {
    this.svg.selectAll(sel).remove()
    return this
  }

}
