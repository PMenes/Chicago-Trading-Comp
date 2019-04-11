var startTime=0;
var tNow = () => (new Date()).getTime()
var elapsed = (label) => console.log("==========", tNow() - startTime, label)
var thiscase = location.hash.replace(/^#/, "").toLowerCase()
console.log("thiscase", thiscase)
var Case = {case1: Case1, case2: Case2}
var updater = new Case[thiscase]()
window.addEventListener("load", function(event) {
  var ws = Ws('ws://'+location.host+"/ws")
})
$(window).on("configok", function(event) {
  console.log("starting.....................")
  Grid( $(".grid") ).all()
})
