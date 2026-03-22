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

        # Make copy of POST data and prepare to compare with
        # basket line item
        qty_check = {"check": dict(data.copy())}
        qty_check["check"].pop("csrfmiddlewaretoken")
        qty_check["check"].pop("redirect_url")
        qty_check["check"].pop("quantity")
        if "tiers" not in qty_check["check"]:
            qty_check["check"]["tiers"] = 1

        # from POST dictionary turn values from list to string
        for key, value in qty_check["check"].items():
            if isinstance(value, list):
                qty_check["check"][key] = value[0]

        # turn values to integer for calculations
        for key, value in qty_check["check"].items():
            if key == "tiers":
                qty_check["check"][key] = int(value)

        qty_check["check"].update(
            {"name": product.name, "product_id": product_id})
        qty_change = False

        # compare POST data with basket items to find duplicates and update
        # quantity and total for items in basket accordingly.
        # Remove quantity and total for dictionary comparison as these should
        # be diffent values while the dictionaries still match.

        for item in basket:
            quantity_item = int(basket[item].pop("quantity"))
            total_item = float(basket[item].pop("total"))
            if basket[item] == qty_check["check"]:
                basket[item]["quantity"] = quantity_item + \
                    int(data.get("quantity"))
                basket[item]["total"] = total_item + float(total)
                qty_change = True
            else:
                basket[item]["quantity"] = quantity_item
                basket[item]["total"] = total_item

        if not qty_change:
            item_id = "item_" + str(len(basket) + 1)
            basket[item_id] = {}
            basket[item_id]["name"] = product.name
            basket[item_id]["product_id"] = product_id
            basket[item_id]["size"] = data.get("size")
            basket[item_id]["tiers"] = int(data.get("tiers", 1))
            basket[item_id]["sponge"] = data.get("sponge")
            basket[item_id]["filling"] = data.get("filling")
            basket[item_id]["icing"] = data.get("icing")
            basket[item_id]["main_colour"] = data.get("main_colour")
            basket[item_id]["secondary_colour"] = data.get("secondary_colour")
            basket[item_id]["quantity"] = int(data.get("quantity", 1))
            basket[item_id]["cake_topper"] = data.get("cake_topper")
            basket[item_id]["total"] = float(total)

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
