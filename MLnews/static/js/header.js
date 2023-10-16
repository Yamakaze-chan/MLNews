$(document).ready(function(){

    $('.menu-search').click(function(){
      $('.search-box').slideToggle(700)
    })
  
    $('.responsive-menu').click(function(){
      $('.responsive-sub-menu').toggleClass('responsive-active-sub-menu')
    })
  })