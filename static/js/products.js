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


    $('#sort-selector').change(function () {
        var selector = $(this);
        var currentUrl = new URL(window.location);
        var selectedVal = selector.val();

        if (selectedVal != "reset") {
            var sort = selectedVal.split("_")[0];
            var direction = selectedVal.split("_")[1];

            currentUrl.searchParams.set("sort", sort);
            currentUrl.searchParams.set("direction", direction);
            window.location.replace(currentUrl);
        } else {
            currentUrl.searchParams.delete("sort");
            currentUrl.searchParams.delete("direction");
            window.location.replace(currentUrl);
        }
    });

});