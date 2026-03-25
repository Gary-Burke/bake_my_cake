from django.shortcuts import render
from .models import Order, DeliveryDate
from .forms import OrderForm

# Create your views here.


def checkout(request):

    template = "checkout/checkout.html"

    if request.method == "POST":
        pass

    order_form = OrderForm()

    context = {
        "order_form": order_form,
    }

    return render(request, template, context)
