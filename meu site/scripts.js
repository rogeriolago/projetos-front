var $carousel = $('.imgList'),currentSlide, nextSlide;

$(".wrapper .left").on('click', function() {

  var length = $('.imgList lu').length;

  currentSlide = $carousel.attr('data-slide');
  nextSlide = +currentSlide === (length - 1) ? 0 : +currentSlide + 1;
  $carousel.attr('data-slide', nextSlide);
  //console.log(nextSlide); 

  $('.wrapper .imgList lu').css({
    'position': 'relative',
    'transition': 'all 1s ease',
    'right': 'calc(' + nextSlide + ' * 700px)', 
  });

});

$(".wrapper .right").on('click', function() {
  var length = $('.wrapper .imgList li').length;
  currentSlide = $carousel.attr('data-slide');
  nextSlide = +currentSlide === 0 ? (length - 1) : +currentSlide - 1;
  $carousel.attr('data-slide', nextSlide);
  //console.log(nextSlide);
  $('.wrapper .imgList li').css({
    'position': 'relative',
    'transition': 'all 1s ease',
    'right': 'calc(' + nextSlide + ' * 700px)'
  });
});