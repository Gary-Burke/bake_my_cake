from django.shortcuts import render

# Create your views here.


def checkout(request):

    template = "checkout/checkout.html"
    context = {

    }

    return render(request, template, context)
