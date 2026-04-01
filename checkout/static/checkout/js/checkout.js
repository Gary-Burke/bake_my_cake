/* jshint esversion: 11, jquery: true */

$(document).ready(function () {

    // ── Flatpickr ────────────────────────────────────────────────────── //
    const dateInput = document.getElementById("id_delivery_date");
    const minDate = parseInt(dateInput.dataset.minDate, 10);
    const maxDate = parseInt(dateInput.dataset.maxDate, 10);
    const disabledDates = JSON.parse(dateInput.dataset.disabledDates || "[]");

    $("#id_delivery_date").flatpickr({
        minDate: new Date().fp_incr(minDate),
        maxDate: new Date().fp_incr(maxDate),
        disable: disabledDates,
        dateFormat: "Y-m-d",
        disableMobile: true,
        onChange: function (selectedDates, dateStr) {
            $.get("/checkout/", {
                delivery_date: dateStr
            });
        }
    });

    // https://docs.stripe.com/payments/quickstart-checkout-sessions ───── //

    // ── Stripe setup ─────────────────────────────────────────────────── //
    const stripePublicKey = JSON.parse(
        document.getElementById("stripe-public-key").textContent
    );
    const stripe = Stripe(stripePublicKey);

    let checkout;
    let actions;

    initialize();

    document
        .querySelector("#payment-form")
        .addEventListener("submit", handleSubmit);

    // ── Initialize Stripe Checkout Elements ──────────────────────────── //
    async function initialize() {
        const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

        const promise = fetch("/checkout/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken,
                },
            })
            .then((r) => r.json())
            .then((r) => r.clientSecret);

        const appearance = {
            theme: "stripe"
        };

        checkout = stripe.initCheckoutElementsSdk({
            clientSecret: promise,
            elementsOptions: {
                appearance
            },
        });

        const loadActionsResult = await checkout.loadActions();
        if (loadActionsResult.type === "success") {
            actions = loadActionsResult.actions;
            const session = actions.getSession();
            document.querySelector("#button-text").textContent =
                `Pay ${session.total.total.amount} now`;
        }

        const emailInput = document.getElementById("email");
        const emailErrors = document.getElementById("email-errors");

        if (emailInput) {
            emailInput.addEventListener("input", () => {
                emailErrors.textContent = "";
                emailInput.classList.remove("error");
            });

            emailInput.addEventListener("blur", async () => {
                const newEmail = emailInput.value;
                if (!newEmail) return;
                const {
                    isValid,
                    message
                } = await validateEmail(newEmail);
                if (!isValid) {
                    emailInput.classList.add("error");
                    emailErrors.textContent = message;
                }
            });
        }

        const paymentElement = checkout.createPaymentElement();
        paymentElement.mount("#payment-element");
    }

    // ── Validate email via Stripe ─────────────────────────────────────── //
    const validateEmail = async (email) => {
        const updateResult = await actions.updateEmail(email);
        const isValid = updateResult.type !== "error";
        return {
            isValid,
            message: !isValid ? updateResult.error.message : null,
        };
    };

    // ── Validate order form via Django ────────────────────────────────── //
    async function validateOrderForm() {
        const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
        const addr2El = document.getElementById("id_street_address2");

        const formData = {
            name_surname: document.getElementById("id_name_surname").value,
            phone_number: document.getElementById("id_phone_number").value,
            street_address1: document.getElementById("id_street_address1").value,
            street_address2: addr2El ? addr2El.value : "",
            town_or_city: document.getElementById("id_town_or_city").value,
            state: document.getElementById("id_state").value,
            postcode: document.getElementById("id_postcode").value,
            country: document.getElementById("id_country").value,
            delivery_date: document.getElementById("id_delivery_date").value,
            email: document.getElementById("email").value,
            save_info: document.getElementById("id_save_info")?.checked || false,
        };

        const response = await fetch("/checkout/validate/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken,
            },
            body: JSON.stringify(formData),
        });

        return response.json();
    }

    // ── Clear previous validation state ──────────────────────────────── //
    function clearValidationErrors() {
        document.querySelectorAll(".is-invalid").forEach((el) => {
            el.classList.remove("is-invalid");
        });
        document.querySelectorAll(".invalid-feedback").forEach((el) => {
            el.remove();
        });
    }

    // ── Handle form submission ────────────────────────────────────────── //
    async function handleSubmit(e) {
        e.preventDefault();
        setLoading(true);
        clearValidationErrors();

        // Step 1: validate order form server-side
        const validationResponse = await validateOrderForm();

        if (!validationResponse.valid) {
            Object.entries(validationResponse.errors).forEach(([field, errors]) => {
                const fieldId = field === "email" ? "email" : `id_${field}`;
                const input = document.getElementById(fieldId);
                if (input) {
                    input.classList.add("is-invalid");
                    let errorDiv = input.nextElementSibling;
                    if (!errorDiv || !errorDiv.classList.contains("invalid-feedback")) {
                        errorDiv = document.createElement("div");
                        errorDiv.classList.add("invalid-feedback");
                        input.after(errorDiv);
                    }
                    errorDiv.textContent = errors[0];
                }
            });
            showMessage("Please correct the errors above before paying.");
            setLoading(false);
            return;
        }

        // Step 2: update Stripe session metadata with validated order details
        const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
        const updateResponse = await fetch("/checkout/update-session/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken,
            },
        }).then((r) => r.json());

        if (updateResponse.error) {
            showMessage("Something went wrong. Please try again.");
            setLoading(false);
            return;
        }

        // Step 3: validate email with Stripe
        const emailInput = document.getElementById("email");
        const emailErrors = document.getElementById("email-errors");
        const {
            isValid,
            message
        } = await validateEmail(emailInput.value);

        if (!isValid) {
            emailInput.classList.add("is-invalid");
            emailErrors.textContent = message;
            showMessage(message);
            setLoading(false);
            return;
        }

        // Step 4: confirm payment with Stripe
        const {
            error
        } = await actions.confirm();
        if (error) {
            showMessage(error.message);
        }

        setLoading(false);
    }

    // ── UI helpers ───────────────────────────────────────────────────── //
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