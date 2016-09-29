$(document).ready(function(){ 
  $(".sliding-panel__btn").on("click", function(event) {
    event.preventDefault();//the default action of the event will not be triggered
                
    if($(".sliding-panel-ini").hasClass("sliding-panel-ini-open")) {
      $(".sliding-panel-ini").removeClass("sliding-panel-ini-open");
    } else {
      $(".sliding-panel-ini").addClass("sliding-panel-ini-open");      
    }
  });
  $(".sliding-panel__close").on("click", function(event) {
  	$(".sliding-panel-ini").removeClass("sliding-panel-ini-open");
  });
  $(window).scroll(function() {
    $(".sliding-panel-ini").removeClass("sliding-panel-ini-open");
  });
})