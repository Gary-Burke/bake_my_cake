from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse

from products.models import Product
from .utils import check_basket
from products.utils import calculate_total
from products.constants import PRODUCT_COST, PRODUCT_COST_CUPCAKE

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
        basket = request.session.get("basket", {})
        total = calculate_total(request, product)
        check_basket(request, basket, product, total)

        messages.add_message(
            request, messages.SUCCESS,
            f"{product.name} has been added to your basket!"
        )

        return redirect("products")


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


def edit_basket(request, item_id):
    """
    Updates an instance of an item stored in the session basket

    **Model**
    :model:`products.Product`
    """
    basket = request.session.get("basket", {})
    product = get_object_or_404(Product, pk=basket[item_id]["product_id"])
    template = "basket/edit_basket.html"

    # Used to loop through in template input fields
    if product.shape == "cupcake":
        product_cost = PRODUCT_COST_CUPCAKE
    else:
        product_cost = PRODUCT_COST

    if request.GET.get("sponge"):
        try:
            total = calculate_total(request, product)

            # Return calculated total to JS to update field
            # wihtout having to reload whole query in template
            # str() needed to convert Decimal object for JSON handling
            return JsonResponse(
                {"total": str(total)}
            )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    total = calculate_total(request, product)

    if request.method == "POST":

        # Remove current item from basket to compare it with the updated
        # choices from user and existing basket to check for qty.
        del basket[item_id]
        check_basket(request, basket, product, total)

        messages.add_message(
            request, messages.SUCCESS,
            "Your basket has been updated!"
        )

        return redirect("view_basket")

    context = {
        "product": product,
        "product_cost": product_cost,
        "item_id": item_id,
    }

    return render(request, template, context)
