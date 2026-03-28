import json
import stripe
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.conf import settings
from .models import Order, DeliveryDate
from profiles.models import UserProfile
from .forms import OrderForm
from basket.contexts import basket_contents
from .utils import get_dates
from decimal import Decimal, ROUND_HALF_UP

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.


def checkout(request):
    """
    TODO: Add comment when done TODO:
    """

    basket = request.session.get("basket", {})
    if not basket:
        messages.error(request, "Your basket is currently empty")
        return redirect("products")

    # Stripe metadata values have a 500 character limit
    basket_trimmed = {
        item_key: {
            "product_id": item_data["product_id"],
            "size": item_data["size"],
            "tiers": item_data["tiers"],
            "quantity":   item_data["quantity"],
        }
        for item_key, item_data in basket.items()
    }

    if request.method == "POST" and request.content_type == "application/json":
        current_basket = basket_contents(request)
        grand_total = Decimal(current_basket["grand_total"])
        stripe_total = int(grand_total.quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP) * 100)

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
                "basket": json.dumps(basket_trimmed),
                "username": str(request.user) if request.user.is_authenticated else "guest",
            },
        )
        return JsonResponse({"clientSecret": session.client_secret})

    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
            order_form = OrderForm(initial={
                "name_surname":   profile.name_surname,
                "phone_number":   profile.phone_number,
                "street_address1": profile.street_address1,
                "street_address2": profile.street_address2,
                "town_or_city":   profile.town_or_city,
                "state":          profile.state,
                "postcode":       profile.postcode,
                "country":        profile.country,
            })
        except UserProfile.DoesNotExist:
            order_form = OrderForm()
    else:
        order_form = OrderForm()

    # Get values from utils for date check and pass to html as data attributes
    # jQuery uses these values to update flatpickr accordingly
    date_context = get_dates()
    order_form.fields["delivery_date"].widget.attrs.update({
        "data-min-date": date_context["min_date"],
        "data-max-date": date_context["max_date"],
        "data-disabled-dates": date_context["dates_not_allowed"],
    })

    template = "checkout/checkout.html"
    context = {
        "order_form": order_form,
        "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
    }

    return render(request, template, context)


def checkout_complete(request):
    """
    Stripe redirects here after payment with ?session_id=...
    Retrieve the session and create the Order record.
    """
    session_id = request.GET.get("session_id")
    if not session_id:
        messages.error(request, "No session ID found.")
        return redirect("checkout")

    session = stripe.checkout.Session.retrieve(session_id)

    if session.payment_status == "paid":
        # Only create the order if it doesn't already exist (idempotency)
        if not Order.objects.filter(stripe_pid=session.payment_intent).exists():
            basket = json.loads(session.metadata.get("basket", "{}"))

            # TODO: build and save Order + OrderLineItems + DeliveryDate here TODO:
            #       using session.customer_details and basket contents

        return render(request, "checkout/complete.html", {"session": session})

    messages.error(request, "Payment was not completed.")
    return redirect("checkout")


def session_status(request):
    """
    Called by complete.js to poll the session status via AJAX.
    """
    session_id = request.GET.get("session_id")
    if not session_id:
        return JsonResponse({"error": "No session_id provided"}, status=400)

    session = stripe.checkout.Session.retrieve(
        session_id,
        expand=["payment_intent"],  # so we can read payment_intent.status
    )

    return JsonResponse({
        "status":                session.status,
        "payment_status":        session.payment_status,
        "payment_intent_id":     session.payment_intent.id if session.payment_intent else None,
        "payment_intent_status": session.payment_intent.status if session.payment_intent else None,
    })
