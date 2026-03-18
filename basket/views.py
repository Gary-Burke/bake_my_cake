from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages
from products.models import Product
from products.utils import calculate_total

# Create your views here.


def view_basket(request):
    """ A view to render the contents of the basket """

    return render(request, 'basket/basket.html')


def add_to_basket(request, product_id):

    if request.method == "POST":
        product = get_object_or_404(Product, pk=product_id)
        redirect_url = request.POST.get('redirect_url')

        print(f"request.POST : {request.POST}")
        print(f"redirect_url : {redirect_url}")
        print(f"product : {product}")

        total = calculate_total(request, product)

        print(f"total : {total}")

        return redirect(redirect_url)
