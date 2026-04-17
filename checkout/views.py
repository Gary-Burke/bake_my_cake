import json
import stripe
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.conf import settings
from django.db import IntegrityError
from datetime import date, timedelta, datetime

from .models import Order, DeliveryDate, OrderLineItem
from products.models import Product
from profiles.models import UserProfile
from .forms import OrderForm

from basket.contexts import basket_contents
from .utils import get_dates
from decimal import Decimal, ROUND_HALF_UP
from .webhooks import send_confirmation_email

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.


def validate_order_form(request):
    """
    **Context**
    ``order_form``
     An instance of :form:`checkout.OrderForm`

    Returns an instance of a form for :form:`checkout.OrderForm`

    It validates the order_form separately since Stripe initializes
    the POST request via JS with json data and so normal form validation
    gets bypassed in Django. When the form is valid the data from the form
    gets stored in the request session as "pending_order"
    """
    if request.method == "POST":
        # Checkout form data via JS as JSON
        data = json.loads(request.body)
        # Call function for flatpickr date logic parameters from utils.py
        date_context = get_dates()

        today = date.today()
        min_date_val = today + timedelta(days=date_context["min_date"])
        max_date_val = today + timedelta(days=date_context["max_date"])

        delivery_date_str = data.get("delivery_date", "")
        # Convert JSON string to Python List for dates_not_allowed check
        dates_not_allowed = json.loads(date_context["dates_not_allowed"])

        # Test for empty input from user
        if not delivery_date_str:
            return JsonResponse({
                "valid": False,
                "errors": {"delivery_date": ["Please select a delivery date."]}
            })

        # Convert string to date object to test for date input format
        try:
            delivery_date = datetime.strptime(
                delivery_date_str, "%Y-%m-%d").date()
        except ValueError:
            return JsonResponse({
                "valid": False,
                "errors": {
                    "delivery_date": ["Please enter a valid date format."]}
            })

        # Test for html form hack for dates_not_allowed
        if delivery_date_str in dates_not_allowed:
            return JsonResponse({
                "valid": False,
                "errors": {
                    "delivery_date": ["Please select a valid delivery date."]}
            })

        # Test for min/max date range
        if delivery_date < min_date_val or delivery_date > max_date_val:
            return JsonResponse({
                "valid": False,
                "errors": {
                    "delivery_date": ["Please select a valid delivery date."]}
            })

        # Remaining code comes from claude.ai
        # Remove delivery_date from data before passing to OrderForm
        # since OrderForm expects a DeliveryDate FK instance, not a string
        form_data = {k: v for k, v in data.items() if k != "delivery_date"}
        order_form = OrderForm(form_data)

        if order_form.is_valid():
            # save full data including date
            request.session["pending_order"] = data

            return JsonResponse({"valid": True})
        else:
            errors = {
                field: [str(e) for e in error_list]
                for field, error_list in order_form.errors.items()
            }
            return JsonResponse({"valid": False, "errors": errors})


def checkout(request):
    """
    Create stripe checkout session and pass metadata from basket to stripe

    **context**
    ``order_form``
    An instance of :form:`checkout.OrderForm`

    ``date_context``
    Dates and data passed to jQuery to handle Flatpickr calendar
    in the template. Logic stored in .utils.py

    ``stripe_public_key``
    Global variable stored in settings.py

    **Template**
    :template:`checkout/checkout.html`
    """

    basket = request.session.get("basket", {})
    if not basket:
        messages.error(request, "Your basket is currently empty")
        return redirect("products")

    # Checks POST from JS - the initialize() function in checkout.js - Stripe
    if request.method == "POST" and request.content_type == "application/json":
        current_basket = basket_contents(request)
        grand_total = Decimal(current_basket["grand_total"])
        stripe_total = int(grand_total.quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP) * 100)

        # Stripe metadata values have a 500 character limit for each key.
        # Webhooks need a full basket to rebuild the Order and OrderLineItems.
        # Solution: Store each basket item in its own metadata key
        item_metadata = {}
        for item_key, item_data in basket.items():
            item_metadata[item_key] = json.dumps({
                "product_id": item_data["product_id"],
                "size": item_data["size"],
                "tiers": item_data["tiers"],
                "sponge": item_data["sponge"],
                "filling": item_data["filling"],
                "icing": item_data["icing"],
                "main_colour": item_data["main_colour"],
                "secondary_colour": item_data["secondary_colour"],
                "cake_topper": item_data["cake_topper"],
                "quantity": item_data["quantity"],
                "total": item_data["total"],
            })

        # https://docs.stripe.com/payments/quickstart-checkout-sessions
        session = stripe.checkout.Session.create(
            ui_mode="elements",
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": settings.STRIPE_CURRENCY,
                    "product_data": {"name": "Your Order"},
                    "unit_amount": stripe_total,
                },
                "quantity": 1,
            }],
            mode="payment",
            # {CHECKOUT_SESSION_ID} is filled in by Stripe automatically
            return_url=(
                request.build_absolute_uri("/checkout/complete/")
                + "?session_id={CHECKOUT_SESSION_ID}"
            ),
            metadata={
                # One key per basket item e.g. "item_1": "{}", "item_2": "{}"
                **item_metadata,
                "item_count": str(len(basket)),
                "username": str(request.user) if request.user.is_authenticated else "guest",  # noqa
                # Order details left empty - avoid timing problem
                # filled in by update_session_metadata
                "save_info": "",
                "name_surname": "",
                "phone_number": "",
                "email": "",
                "street_address1": "",
                "street_address2": "",
                "town_or_city": "",
                "state": "",
                "postcode": "",
                "country": "",
                "delivery_date": "",
            },
        )

        # Store session ID in Django session so update endpoint can access it
        request.session["stripe_session_id"] = session.id

        return JsonResponse({"clientSecret": session.client_secret})

    # Prepopulate form with user profile data if user is logged in
    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
            if not profile.email:
                email = request.user.email
            else:
                email = profile.email
            order_form = OrderForm(initial={
                "name_surname": profile.name_surname,
                "email": email,
                "phone_number": profile.phone_number,
                "street_address1": profile.street_address1,
                "street_address2": profile.street_address2,
                "town_or_city": profile.town_or_city,
                "state": profile.state,
                "postcode": profile.postcode,
                "country": profile.country,
            })
        except UserProfile.DoesNotExist:
            order_form = OrderForm()
    else:
        order_form = OrderForm()

    # Get values from utils.py for date check and pass to template
    # as data attributes. jQuery uses these values to update flatpickr.
    date_context = get_dates()

    template = "checkout/checkout.html"
    context = {
        "order_form": order_form,
        "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
        "date_context": date_context,
    }

    return render(request, template, context)


def update_session_metadata(request):
    """
    Called by JS after form validation succeeds.
    Updates the Stripe session metadata with order details.
    """
    if request.method == "POST":
        stripe_session_id = request.session.get("stripe_session_id")
        if not stripe_session_id:
            return JsonResponse({"error": "No session found"}, status=400)

        pending_order = request.session.get("pending_order", {})
        if not pending_order:
            return JsonResponse(
                {"error": "No pending order found"}, status=400
            )

        stripe.checkout.Session.modify(
            stripe_session_id,
            metadata={
                "save_info":       str(pending_order.get("save_info", False)),
                "name_surname":    pending_order.get("name_surname", ""),
                "phone_number":    pending_order.get("phone_number", ""),
                "email":           pending_order.get("email", ""),
                "street_address1": pending_order.get("street_address1", ""),
                "street_address2": pending_order.get("street_address2", ""),
                "town_or_city":    pending_order.get("town_or_city", ""),
                "state":           pending_order.get("state", ""),
                "postcode":        pending_order.get("postcode", ""),
                "country":         pending_order.get("country", ""),
                "delivery_date":   pending_order.get("delivery_date", ""),
            }
        )
        return JsonResponse({"success": True})


def checkout_complete(request):
    """
    Upon successfull checkout it creates an instance of:
        :model:`checkout.Order`
        :model:`checkout.DeliveryDate`
        :model:`checkout.OrderLineItem`
        :model:`checkout.UserProfile`

    Sends confirmation email to customer

    **context**
    ``order``
    Creates an instance of :model:`checkout.Order` and also creates an instance
    for the relationships between this model and the following:
        :model:`checkout.DeliveryDate`
        :model:`checkout.OrderLineItem`
        :model:`checkout.UserProfile` - only if the user is logged in and has
                                        opted to save their billing info

    **Template**
    :template:`checkout/complete.html`
    """

    session_id = request.GET.get("session_id")
    if not session_id:
        messages.error(request, "No session ID found.")
        return redirect("checkout")

    # https://docs.stripe.com/payments/quickstart-checkout-sessions
    session = stripe.checkout.Session.retrieve(session_id)

    if session.payment_status == "paid":
        try:
            if not Order.objects.filter(
                    stripe_pid=session.payment_intent).exists():

                # Retrieve the form data saved during form validation in
                # def validate_order_form()
                pending_order = request.session.get("pending_order")
                if not pending_order:
                    messages.error(request, "Order data not found.")
                    return redirect("checkout")

                # Rebuild the form from the session data
                basket = request.session.get("basket", {})

                form_data = {
                    "name_surname": pending_order["name_surname"],
                    "phone_number": pending_order["phone_number"],
                    "email": pending_order["email"],
                    "street_address1": pending_order["street_address1"],
                    "street_address2": pending_order["street_address2"],
                    "town_or_city": pending_order["town_or_city"],
                    "state": pending_order["state"],
                    "postcode": pending_order["postcode"],
                    "country": pending_order["country"],
                }

                order_form = OrderForm(form_data)
                save_info = pending_order["save_info"]

                if order_form.is_valid():
                    order = order_form.save(commit=False)

                    # Build Order with info not present in order_form
                    order.stripe_pid = session.payment_intent
                    order.grand_total = Decimal(session.amount_total) / 100
                    order.original_basket = json.dumps(basket)

                    # Link Order to UserProfile
                    if request.user.is_authenticated:
                        try:
                            order.user_profile = UserProfile.objects.get(
                                user=request.user)
                        except UserProfile.DoesNotExist:
                            order.user_profile = ""

                    # Parse "delivery_date" string into datetime object
                    # and extract the date
                    date_obj = datetime.strptime(
                        pending_order["delivery_date"], "%Y-%m-%d").date()

                    # Search if date_obj exists as an instance in DeliveryDate
                    # and returns it or creates it if not found.
                    delivery_date, _ = DeliveryDate.objects.get_or_create(
                        date=date_obj)

                    # Set ForeignKey relation between Order and Delivery Date
                    order.delivery_date = delivery_date
                    order.save()

                    # Save an instance of OrderLineItem for every item stored
                    # in the session basket
                    for item in basket:
                        try:
                            product_id = basket[item]["product_id"]
                            product = Product.objects.get(id=product_id)
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                size=basket[item]["size"],
                                tiers=basket[item]["tiers"],
                                sponge=basket[item]["sponge"],
                                filling=basket[item]["filling"],
                                icing=basket[item]["icing"],
                                main_colour=basket[item]["main_colour"],
                                secondary_colour=basket[item][
                                    "secondary_colour"],
                                quantity=basket[item]["quantity"],
                                cake_topper=basket[item]["cake_topper"],
                                total=basket[item]["total"],
                            )
                            order_line_item.save()

                        except Product.DoesNotExist:
                            messages.error(
                                request, (
                                    "One of the prodcuts in your basket has "
                                    "been removed from our database. Please "
                                    "contact us for assistance"
                                ))

                            order.delete()
                            return redirect("view_basket")

                    # Update UserProfile if save_info was checked
                    # No try block needed due to signals used in profile models
                    if save_info and request.user.is_authenticated:
                        profile = UserProfile.objects.get(user=request.user)
                        profile.name_surname = pending_order["name_surname"]
                        profile.phone_number = pending_order["phone_number"]
                        profile.email = pending_order["email"]
                        profile.street_address1 = pending_order[
                            "street_address1"]
                        profile.street_address2 = pending_order[
                            "street_address2"]
                        profile.town_or_city = pending_order["town_or_city"]
                        profile.state = pending_order["state"]
                        profile.postcode = pending_order["postcode"]
                        profile.country = pending_order["country"]
                        profile.save()

                    send_confirmation_email(order, settings.DEFAULT_FROM_EMAIL)

                    # Clear session data after saving
                    del request.session["pending_order"]

                else:
                    messages.error(
                        request,
                        "There was an error with your form. "
                        "Please double check your information."
                    )

        except IntegrityError:
            # Webhook created the order first
            # Race condition handled gracefully
            pass

        # Clear basket from session after checkout
        if 'basket' in request.session:
            del request.session['basket']

        order = Order.objects.get(stripe_pid=session.payment_intent)

        template = "checkout/complete.html"
        context = {
            "order": order,
        }

        return render(request, template, context)

    messages.error(request, "Payment was not completed.")
    return redirect("checkout")
