from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from products.models import Product
from decimal import Decimal
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
        redirect_url = request.POST.get('redirect_url')
        data = request.POST
        basket = request.session.get("basket", {})
        total = calculate_total(request, product)

        # Make a copy of POST data and prepare the data
        # to compare with basket line items
        qty_check = {"check": dict(data.copy())}
        qty_check["check"].pop("csrfmiddlewaretoken")
        qty_check["check"].pop("redirect_url")
        qty_check["check"].pop("quantity")

        # Some products don't have tiers as options, so set default to 1
        qty_check["check"]["tiers"] = int(data.get("tiers", 1))

        # from POST dictionary turn values from list to string
        for key, value in qty_check["check"].items():
            if isinstance(value, list):
                qty_check["check"][key] = value[0]

        qty_check["check"].update(
            {"name": product.name, "product_id": product_id})
        qty_change = False

        # compare POST data with basket items to find duplicates and update
        # quantity and total for items in basket accordingly.
        # Remove quantity and total for dictionary comparison as these should
        # be diffent values while the dictionaries still match.
        for item in basket:
            quantity_item = int(basket[item].pop("quantity"))
            total_item = basket[item].pop("total")
            if basket[item] == qty_check["check"]:
                basket[item]["quantity"] = quantity_item + \
                    int(data.get("quantity"))
                basket[item]["total"] = str(
                    Decimal(total_item) + Decimal(total))
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
            basket[item_id]["total"] = total

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
        data = request.POST
        basket[item_id]["size"] = data.get("size")
        basket[item_id]["tiers"] = int(data.get("tiers", 1))
        basket[item_id]["sponge"] = data.get("sponge")
        basket[item_id]["filling"] = data.get("filling")
        basket[item_id]["icing"] = data.get("icing")
        basket[item_id]["main_colour"] = data.get("main_colour")
        basket[item_id]["secondary_colour"] = data.get("secondary_colour")
        basket[item_id]["quantity"] = int(data.get("quantity", 1))
        basket[item_id]["cake_topper"] = data.get("cake_topper")
        basket[item_id]["total"] = total

        request.session["basket"] = basket

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
