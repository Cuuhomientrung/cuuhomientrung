import $ from 'jquery';

const waitWebpackAndStyleLoader = 1100;

// End preloader when webpack is ready
$(document).ready(() => {
  setTimeout(() => {
    $('#loader').slideUp("fast", () => {
        $('body').removeClass('cuuhomientrung__preloader');
        $('#loader').remove();
        $('#loader__wrapped').show();
    });
  }, Math.floor(Math.random() * waitWebpackAndStyleLoader));
});
