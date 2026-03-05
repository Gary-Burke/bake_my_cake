/* jshint esversion: 11 */

// Wait for the DOM to load before executing functions
$(document).ready(function () {

    $("#category-selector").change(function (e) {
        var selectedVal = $(this).val();
        var currentUrl = new URL(window.location);
        
        console.log(`selectedVal: ${selectedVal}`)
        console.log(`currentUrl: ${currentUrl}`)

        if (selectedVal != "reset") {
            var category = selectedVal;

            currentUrl.searchParams.set("category", category);            
            window.location.replace(currentUrl);
        } else {
            currentUrl.searchParams.delete("category");
            window.location.replace(currentUrl);
        }

        
    });


    $('#sort-selector').change(function () {
        var selector = $(this);
        var currentUrl = new URL(window.location);
        var selectedVal = selector.val();

        console.log(`selectedVal: ${selectedVal}`)
        console.log(`currentUrl: ${currentUrl}`)

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