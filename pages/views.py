from django.shortcuts import render
from django.contrib import messages
from .forms import CustomOrderForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


# Create your views here.


def index(request):
    return render(request, "pages/index.html")


def about(request):
    return render(request, "pages/about.html")


def custom_order(request):
    custom_order_form = CustomOrderForm()

    def _send_confirmation_email(custom_order):
        """Send the user a confirmation email"""
        subject = render_to_string(
            'pages/custom_order_emails/custom_order_subject.txt',
            {'custom_order': custom_order})
        body = render_to_string(
            'pages/custom_order_emails/custom_order_body.txt',
            {'custom_order': custom_order,
             'contact_email': settings.DEFAULT_FROM_EMAIL})

        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [settings.DEFAULT_FROM_EMAIL]
        )

    if request.method == "POST":
        custom_order_form = CustomOrderForm(
            data=request.POST, files=request.FILES)
        if custom_order_form.is_valid():
            custom_order = custom_order_form.save()
            messages.add_message(
                request, messages.SUCCESS,
                "Custom order submitted successfully!"
            )
            _send_confirmation_email(custom_order)
            custom_order_form = CustomOrderForm()

    template = "pages/custom_order.html"

    context = {
        "custom_order_form": custom_order_form,
    }

    return render(request, template, context)
