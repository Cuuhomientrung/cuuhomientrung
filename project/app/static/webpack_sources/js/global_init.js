import $ from 'jquery';
import LazyLoad from './plugins/lazyload.amd';
const waitWebpackAndStyleLoader = 1100;


function preloaderInit() {
  $('#loader').slideUp("fast", () => {
      $('body').removeClass('cuuhomientrung__preloader');
      $('#loader').remove();
      $('#loader__wrapped').show();
  });
}

function lazyloadInit() {
  var lazyLoadInstance = new LazyLoad({});
}

// End preloader when webpack is ready
$(document).ready(() => {
  // Preloader
  setTimeout(() => {
    preloaderInit();
    lazyloadInit();
  }, Math.floor(Math.random() * waitWebpackAndStyleLoader));
});
