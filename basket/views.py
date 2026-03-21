from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib import messages
from products.models import Product
from products.utils import calculate_total

# Create your views here.


def view_basket(request):
    """ A view to render the contents of the basket """

    return render(request, 'basket/basket.html')


def add_to_basket(request, product_id):
    """
    Stores products in session storage inside a dictionary named basket

    **Model**
    :model:`products.Product`
    """

    if request.method == "POST":
        product = get_object_or_404(Product, pk=product_id)
        redirect_url = request.POST.get('redirect_url')
        data = request.POST
        basket = request.session.get("basket", {})
        total = calculate_total(request, product)
        item_id = "item_" + str(len(basket) + 1)

        basket[item_id] = {}
        basket[item_id]["name"] = product.name
        basket[item_id]["product_id"] = product_id
        basket[item_id]["size"] = data.get("size")
        basket[item_id]["tiers"] = data.get("tiers")
        basket[item_id]["sponge"] = data.get("sponge")
        basket[item_id]["filling"] = data.get("filling")
        basket[item_id]["icing"] = data.get("icing")
        basket[item_id]["main_colour"] = data.get("main_colour")
        basket[item_id]["secondary_colour"] = data.get("secondary_colour")
        basket[item_id]["quantity"] = data.get("quantity", 1)
        basket[item_id]["cake_topper"] = data.get("cake_topper")
        basket[item_id]["total"] = str(total)

        request.session["basket"] = basket

        messages.add_message(
            request, messages.SUCCESS,
            f"{product.name} has been added to your basket!"
        )

        return redirect(redirect_url)


def delete_from_basket(request, item_id):
    """
    Removes an item from the basket dictionary stored in the session

    **Model**
    :model:`products.Product`
    """

    try:
        basket = request.session.get("basket", {})
        product = get_object_or_404(Product, pk=basket[item_id]["product_id"])
        basket.pop(item_id)
        request.session["basket"] = basket

        messages.add_message(
            request, messages.SUCCESS,
            f"{product.name} has been removed from your basket!"
        )

        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
