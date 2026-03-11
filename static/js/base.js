/* jshint esversion: 11 */

document.addEventListener("DOMContentLoaded", function () {

    // Trigger Bootstrap Toast element
    document.querySelectorAll('.toast').forEach(toast => {
        new bootstrap.Toast(toast).show();
    });

    // Scroll to top button function
    let mybutton = document.getElementById("scroll-top");

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

});