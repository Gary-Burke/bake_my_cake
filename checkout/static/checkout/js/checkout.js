/* jshint esversion: 11, jquery: true */

// Wait for the DOM to load before executing functions
$(document).ready(function () {

    // ── Flatpickr ────────────────────────────────────────────────────── //
    const dateInput     = document.getElementById("delivery-date");
    const minDate       = parseInt(dateInput.dataset.minDate, 10);
    const maxDate       = parseInt(dateInput.dataset.maxDate, 10);
    const disabledDates = JSON.parse(dateInput.dataset.disabledDates);

    $("#delivery-date").flatpickr({
        minDate:    new Date().fp_incr(minDate),
        maxDate:    new Date().fp_incr(maxDate),
        disable:    disabledDates,
        dateFormat: "Y-m-d",
        onChange: function (selectedDates, dateStr) {
            $.get("/checkout/", { delivery_date: dateStr });
        }
    });

    // ── Stripe ───────────────────────────────────────────────────────── //
    // Read the public key Django injected via json_script — no hardcoding
    const stripePublicKey = JSON.parse(
        document.getElementById("stripe-public-key").textContent
    );
    const stripe = Stripe(stripePublicKey);

    let checkout;
    let actions;

    document
        .querySelector("#payment-form")
        .addEventListener("submit", handleSubmit);

    initialize();

    async function initialize() {
        const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

        const promise = fetch("/checkout/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken":  csrfToken,
            },
        })
        .then((r) => r.json())
        .then((r) => r.clientSecret);

        const appearance = { theme: "stripe" };

        checkout = stripe.initCheckoutElementsSdk({
            clientSecret:    promise,
            elementsOptions: { appearance },
        });

        checkout.on("change", (session) => {
            document.getElementById("submit").disabled = !session.canConfirm;
        });

        const loadActionsResult = await checkout.loadActions();
        if (loadActionsResult.type === "success") {
            actions = loadActionsResult.actions;
            const session = actions.getSession();
            document.querySelector("#button-text").textContent =
                `Pay ${session.total.total.amount} now`;
        }

        // Email field — id manually set to "email" in OrderForm
        const emailInput  = document.getElementById("email");
        const emailErrors = document.getElementById("email-errors");

        if (emailInput) {
            emailInput.addEventListener("input", () => {
                emailErrors.textContent = "";
                emailInput.classList.remove("error");
            });

            emailInput.addEventListener("blur", async () => {
                const newEmail = emailInput.value;
                if (!newEmail) return;
                const { isValid, message } = await validateEmail(newEmail);
                if (!isValid) {
                    emailInput.classList.add("error");
                    emailErrors.textContent = message;
                }
            });
        }

        // Mount the Stripe payment element
        const paymentElement = checkout.createPaymentElement();
        paymentElement.mount("#payment-element");
    }

    // ── Helpers ──────────────────────────────────────────────────────── //

    const validateEmail = async (email) => {
        const updateResult = await actions.updateEmail(email);
        const isValid = updateResult.type !== "error";
        return {
            isValid,
            message: !isValid ? updateResult.error.message : null,
        };
    };

    async function handleSubmit(e) {
        e.preventDefault();
        setLoading(true);

        const emailInput = document.getElementById("email");
        const emailErrors = document.getElementById("email-errors");
        const email = emailInput.value;

        const { isValid, message } = await validateEmail(email);
        if (!isValid) {
            emailInput.classList.add("error");
            emailErrors.textContent = message;
            showMessage(message);
            setLoading(false);
            return;
        }

        const { error } = await actions.confirm();
        if (error) {
            showMessage(error.message);
        }

        setLoading(false);
    }

    function showMessage(messageText) {
        const el = document.querySelector("#payment-message");
        el.classList.remove("hidden");
        el.textContent = messageText;
        setTimeout(() => {
            el.classList.add("hidden");
            el.textContent = "";
        }, 4000);
    }

    function setLoading(isLoading) {
        document.querySelector("#submit").disabled = isLoading;
        document.querySelector("#spinner").classList.toggle("hidden", !isLoading);
        document.querySelector("#button-text").classList.toggle("hidden", isLoading);
    }

});