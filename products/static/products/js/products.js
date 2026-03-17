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

        if (selectedVal != "all_categories") {
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
        // Return the calculated total from view and update html with total
        $.get(`/products/${slug}/${id}/`, params).done(function (data) {
            $("#product-total").text(data.total + "€");
        }).fail(function () {
            console.error("Price calculation failed");
        });
    });


    // Change description of size select options based on shape
    let shape = $("#product-details").data("shape");

    if (shape === "cupcake") {
        $("select option[value='small']").text("12 Cupcakes");
        $("select option[value='medium']").text("24 Cupcakes");
        $("select option[value='large']").text("36 Cupcakes");
    } else if (shape === "square") {
        $("select option[value='small']").text("15cm x 15cm");
        $("select option[value='medium']").text("20cm x 20cm");
        $("select option[value='large']").text("25cm x 25cm");
    } else if (shape === "rectangle") {
        $("select option[value='small']").text("15cm x 20cm");
        $("select option[value='medium']").text("20cm x 30cm");
        $("select option[value='large']").text("30cm x 40cm");
    } else {
        $("select option[value='small']").text("15cm Ø");
        $("select option[value='medium']").text("20cm Ø");
        $("select option[value='large']").text("25cm Ø");
    };

    // Add animation to edit/delete icons when hovered
    $(".admin-icons i").hover(function () {
        $(this).toggleClass("fa-beat");
    });

    /**
     * Gets productId from clicked product edit icon to build dynamic URL.
     * Set href attributes for clicked product to open product edit form.
     */
    $(".button-edit").click(function () {
        let productId = $(this).closest('.product-card-admin').attr("data-product-id");
        $(this).attr("href", `/products/edit/${productId}`);

    });

    /**
     * Triggers bootstrap delete modal confirmation.
     * Gets productId from clicked product delete icon to build dynamic URL.
     * If delete confirm clicked then set URL dynamically to delete product.         
     */
    const deleteModal = new bootstrap.Modal($("#deleteModal"));

    $(".button-delete").on("click", function () {
        let productId = $(this).closest('.product-card-admin').attr("data-product-id");
        $("#delete-confirm").attr("href", `/products/delete/${productId}`);
        deleteModal.show();
    });

    /**
     * Get the search parameters from the URL passed through with name "q"
     * Take that string to prepopulate search field after submission 
     */
    const params = new URLSearchParams(window.location.search);
    if (params.has("q")) {
        $("#form-search input[name='q']").val(params.get("q"));
    }

});