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
    });


    // Get the values for the params from the product html
    $("#product-details .form-select").change(function () {
        const form = $("#product-details");
        const slug = form.data("slug");
        const id = form.data("product-id");

        const params = {
            size: $("#size").val(),
            tiers: $("#tiers").val(),
            sponge: $("#sponge").val(),
            filling: $("#filling").val(),
            icing: $("#icing").val(),
            quantity: $("#quantity").val(),
        };

        // Pass the params values to the view in the get request as a query
        $.get(`/products/${slug}/${id}/`, params).done(function (data) {
            $("#product-total").text(data.total + "€");
        }).fail(function () {
            console.error("Price calculation failed");
        });
    });


    // Change description of size select options based on shape
    let shape = $("#product-details").data("shape").toLowerCase();

    if (shape === "cupcake") {
        $("select option[value='small']").text("12 Cupcakes");
        $("select option[value='medium']").text("24 Cupcakes");
        $("select option[value='large']").text("36 Cupcakes");
    } else if (shape === "square") {
        $("select option[value='small']").text("15cm x 15cm");
        $("select option[value='medium']").text("18cm x 18cm");
        $("select option[value='large']").text("25cm x 25cm");
    } else if (shape === "rectangle") {
        $("select option[value='small']").text("15cm x 20cm");
        $("select option[value='medium']").text("20cm x 25cm");
        $("select option[value='large']").text("30cm x 25cm");
    } else {
        $("select option[value='small']").text("15cm Ø");
        $("select option[value='medium']").text("18cm Ø");
        $("select option[value='large']").text("20cm Ø");
    };


});