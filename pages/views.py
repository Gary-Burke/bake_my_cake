from django.shortcuts import render
from django.contrib import messages
from .forms import CustomOrderForm

# Create your views here.


def index(request):
    return render(request, "pages/index.html")


def about(request):
    return render(request, "pages/about.html")


def custom_order(request):
    custom_order_form = CustomOrderForm()

    if request.method == "POST":
        custom_order_form = CustomOrderForm(
            data=request.POST, files=request.FILES)
        if custom_order_form.is_valid():
            custom_order_form.save()
            messages.add_message(
                request, messages.SUCCESS,
                "Custom order submitted successfully!"
            )
            custom_order_form = CustomOrderForm()

    template = "pages/custom_order.html"

    context = {
        "custom_order_form": custom_order_form,
    }

    return render(request, template, context)
