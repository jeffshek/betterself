$(document).ready(function() {
  // init Masonry
  var $grid = $('.grid').masonry({
    itemSelector: '.grid-item',
    percentPosition: true,
    columnWidth: '.grid-sizer',
    gutter: '.grid-gutter'
  });
  // layout Isotope after each image loads
  $grid.imagesLoaded().progress(function() {
    $grid.masonry();
  });
});