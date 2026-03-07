from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404

from products.models import Product

# Create your views here.


def view_basket(request):
    """ A view to render the contents of the basket """

    return render(request, 'basket/basket.html')


def add_to_basket(request, product_id):

    return render(request, 'basket/basket.html')
