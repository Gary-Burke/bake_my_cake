/* jshint esversion: 11, jquery: true */

// Wait for the DOM to load before executing functions
$(document).ready(function () {

    $("#delivery-date").flatpickr({
        minDate: new Date().fp_incr(7),
        dateFormat: "Y-m-d",
        disableMobile: true,
    });

});