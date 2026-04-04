import json
import stripe
from datetime import datetime
from decimal import Decimal

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.db import IntegrityError

from .models import Order, OrderLineItem, DeliveryDate
from products.models import Product
from profiles.models import UserProfile
from .forms import OrderForm

stripe.api_key = settings.STRIPE_SECRET_KEY
wh_secret = settings.STRIPE_WH_SECRET


def send_confirmation_email(order, contact_email):
    """
    Send a confirmation email to the customer with their order summary
    """
    customer_email = order.email
    order_number = (str(order.order_number))[:10]
    subject = render_to_string(
        'checkout/order_confirmation_emails/order_confirm_subject.txt',
        {'order': order, 'order_number': order_number})
    body = render_to_string(
        'checkout/order_confirmation_emails/order_confirm_body.txt',
        {'order': order, 'order_number': order_number,
         'contact_email': contact_email})

    send_mail(
        subject,
        body,
        contact_email,
        [customer_email]
    )


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, wh_secret
        )
    except ValueError:
        return HttpResponse(status=400)  # Invalid payload
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)  # Invalid signature

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        handle_checkout_complete(session)

    return HttpResponse(status=200)


def handle_checkout_complete(session):
    """
    Creates the Order, DeliveryDate and OrderLineItems from the
    Stripe session metadata. Called by the webhook handler.
    This runs independently of the Django session — all data
    comes from Stripe metadata.
    """
    if session.payment_status != "paid":
        return

    # Idempotency check — skip if order already created by checkout_complete
    if Order.objects.filter(stripe_pid=session.payment_intent).exists():
        return

    metadata = session.metadata
    username = metadata["username"]
    save_info = metadata["save_info"] == "True"

    # Reconstruct basket from individual item keys
    item_count = int(metadata["item_count"])
    basket = {}
    for i in range(1, item_count + 1):
        item_key = f"item_{i}"
        if item_key in metadata:
            basket[item_key] = json.loads(metadata[item_key])

    form_data = {
        "name_surname": metadata["name_surname"],
        "phone_number": metadata["phone_number"],
        "email": metadata["email"],
        "street_address1": metadata["street_address1"],
        "street_address2": metadata["street_address2"] if "street_address2" in metadata else "",  # noqa
        "town_or_city": metadata["town_or_city"],
        "state": metadata["state"],
        "postcode": metadata["postcode"],
        "country": metadata["country"],
    }

    order_form = OrderForm(form_data)

    if not order_form.is_valid():
        print(f"Webhook: OrderForm invalid — {order_form.errors}")
        return

    order = order_form.save(commit=False)
    order.stripe_pid = session.payment_intent
    order.grand_total = Decimal(session.amount_total) / 100
    order.original_basket = json.dumps(basket)

    # Link Order to user profile if authenticated
    try:
        user = User.objects.get(username=username)
        profile = UserProfile.objects.get(user=user)
        order.user_profile = profile
    except (User.DoesNotExist, UserProfile.DoesNotExist):
        order.user_profile = None

    # Create or get the delivery date
    date_obj = datetime.strptime(metadata["delivery_date"], "%Y-%m-%d").date()
    delivery_date, _ = DeliveryDate.objects.get_or_create(date=date_obj)
    order.delivery_date = delivery_date

    try:
        order.save()
    except IntegrityError:
        # checkout_complete created the order first — race condition, skip
        return

    # Create order line items from basket
    for item_key, item_data in basket.items():
        try:
            product = Product.objects.get(id=item_data["product_id"])
            OrderLineItem.objects.create(
                order=order,
                product=product,
                size=item_data["size"],
                tiers=item_data["tiers"],
                sponge=item_data["sponge"],
                filling=item_data["filling"],
                icing=item_data["icing"],
                main_colour=item_data["main_colour"],
                secondary_colour=item_data["secondary_colour"],
                cake_topper=item_data["cake_topper"],
                quantity=item_data["quantity"],
                total=item_data["total"],
            )
        except Product.DoesNotExist:
            print(f"Webhook: Product {item_data['product_id']} not found")
            order.delete()
            return

    # Update profile billing details if save_info was checked
    if save_info and order.user_profile:
        profile = order.user_profile
        profile.name_surname = metadata["name_surname"]
        profile.phone_number = metadata["phone_number"]
        profile.email = metadata["email"]
        profile.street_address1 = metadata["street_address1"]
        profile.street_address2 = metadata["street_address2"]
        profile.town_or_city = metadata["town_or_city"]
        profile.state = metadata["state"]
        profile.postcode = metadata["postcode"]
        profile.country = metadata["country"]
        profile.save()

    send_confirmation_email(order, settings.DEFAULT_FROM_EMAIL)
