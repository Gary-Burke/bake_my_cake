from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import Order, DeliveryDate
from profiles.models import UserProfile
from profiles.forms import UserProfileForm
from .forms import OrderForm
from basket.contexts import basket_contents
from .utils import get_dates

# Create your views here.


def checkout(request):
    """
    TODO: Add comment when done TODO:
    """

    basket = request.session.get("basket", {})
    if not basket:
        messages.error(request, "Your basket is currently empty")
        return redirect("products")

    if request.method == "POST":
        pass
    else:
        if request.user.is_authenticated:
            # Prepopulate fields with stored user profile
            try:
                profile = UserProfile.objects.get(user=request.user)
                order_form = OrderForm(initial={
                    "name_surname": profile.name_surname,
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
    }

    return render(request, template, context)
