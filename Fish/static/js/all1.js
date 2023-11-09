$(document).ready(function () {
   $('.showmenu').on('click',  function(e){
      e.preventDefault();
      $('body').toggleClass('menu-show');
  });

  $('.top').click(function(e){
   e.preventDefault(); 
    $('html,body').stop().animate({scrollTop:0},1000);
  });

});