$(document).ready(function() {
  if (!(/Android|iPhone|iPad|iPod|BlackBerry|Windows Phone/i).test(navigator.userAgent || navigator.vendor || window.opera)) {
  	$.getScript("assets/plugins/skrollr/dist/skrollr.min.js", function(){
      var s = skrollr.init({
        edgeStrategy: "set",
        easing: {
          WTF: Math.random,
          inverted: function(p) {
            return 1-p;
          }
        }
      }); 
  	});
  }
});