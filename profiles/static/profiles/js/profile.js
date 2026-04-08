/* jshint esversion: 11, jquery: true */

// Wait for the DOM to load before executing functions
$(document).ready(function () {

    /**
     * On the profile page load data in template based on user selection.
     */
    $("#profile-tabs a").click(function (e) {
        const path = $(this).data("path");

        if (path !== "profile") {
            e.preventDefault();
            window.location.href = `/profile/orders/?path=${path}`;
        }
    });

});