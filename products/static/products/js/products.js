/* jshint esversion: 11, jquery: true */

// Wait for the DOM to load before executing functions
$(document).ready(function () {

    /**
     * On category selection change from user, get value from input
     * and write the parameter 'category' with retrieved input to url.
     * If no input 'reset' selected then remove parameter from url
     */
    $("#category-selector").change(function (e) {
        var selectedVal = $(this).val();
        var currentUrl = new URL(window.location);

        if (selectedVal != "reset") {
            var category = selectedVal;
            currentUrl.searchParams.set("category", category);
        } else {
            currentUrl.searchParams.delete("category");
        }

        currentUrl.searchParams.delete("page");
        window.location.replace(currentUrl);
    });

    /**
     * On sort selection change from user, get value from input
     * and write the parameters 'sort' and 'direction' with retrieved input to url.
     * If no input 'reset' selected then remove parameter from url.
     */
    $('#sort-selector').change(function () {
        var selectedVal = $(this).val();
        var currentUrl = new URL(window.location);

        if (selectedVal != "reset") {
            var sort = selectedVal.split("_")[0];
            var direction = selectedVal.split("_")[1];
            currentUrl.searchParams.set("sort", sort);
            currentUrl.searchParams.set("direction", direction);
        } else {
            currentUrl.searchParams.delete("sort");
            currentUrl.searchParams.delete("direction");
        }

        currentUrl.searchParams.delete("page");
        window.location.replace(currentUrl);
    });

    
    let mybutton = document.getElementById("scroll-top");

    $(mybutton).hover(function () {
        $(this).toggleClass("fa-beat");
    });

    
    // https://www.w3schools.com/howto/howto_js_scroll_to_top.asp
    window.onscroll = function () {
        scrollFunction()
    };
    
    function scrollFunction() {
        if (document.body.scrollTop > 30 || document.documentElement.scrollTop > 30) {
            mybutton.style.display = "block";
        } else {
            mybutton.style.display = "none";
        }
    }

    function topFunction() {
        document.body.scrollTop = 0; // For Safari
        document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
    }

    mybutton.addEventListener("click", () => {
        topFunction();
    })

    

});