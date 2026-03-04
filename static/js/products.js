/* jshint esversion: 11 */

// Wait for the DOM to load before executing functions
$(document).ready(function () {

    $("#categories > a").on("click", function (e) {
        var currentUrl = window.location.href;
        var selectedUrl = this.href;

        if (selectedUrl === currentUrl) {
            e.preventDefault();
        }
    });

});