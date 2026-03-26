/* jshint esversion: 11, jquery: true */

// Wait for the DOM to load before executing functions
$(document).ready(function () {

    const dateInput = document.getElementById("delivery-date");
    const minDate = parseInt(dateInput.dataset.minDate, 10);
    const maxDate = parseInt(dateInput.dataset.maxDate, 10);
    const disabledDates = JSON.parse(dateInput.dataset.disabledDates);

    $("#delivery-date").flatpickr({
        minDate: new Date().fp_incr(minDate),
        maxDate: new Date().fp_incr(maxDate),
        disable: disabledDates,
        dateFormat: "Y-m-d",

        onChange: function (selectedDates, dateStr, instance) {
            $.get("/checkout/", {
                delivery_date: dateStr
            });
        }
    });

});