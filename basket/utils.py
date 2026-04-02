from products.constants import PRODUCT_COST
from decimal import Decimal


def check_basket(request, basket, product, total):
    """
    This functions checks newly added item and edit items
    to check if they match any of the items in the basket.
    If all details match, then the qty and amount of the item in
    the basket is increased. If not, then a new item is added.
    """

    data = request.POST.copy()

    # Prevent HTML form hacking by checking values with predefined values
    # If values are not valid then assign default values for item creation
    # No need to add cupcake check since they have the same values

    if data.get("sponge") not in PRODUCT_COST["sponge"]:
        data["sponge"] = "vanilla"

    if data.get("filling") not in PRODUCT_COST["filling"]:
        data["filling"] = "vanilla"

    if data.get("icing") not in PRODUCT_COST["icing"]:
        data["icing"] = "royal_icing"

    if data.get("tiers") not in PRODUCT_COST["tiers"]:
        data["tiers"] = 1

    if data.get("quantity") not in PRODUCT_COST["quantity"]:
        data["quantity"] = 1

    if data.get("size") not in PRODUCT_COST["size"]:
        data["size"] = "small"

    # Make a copy of POST data and prepare the data
    # to compare with basket line items
    qty_check = {"check": dict(data.copy())}
    qty_check["check"].pop("csrfmiddlewaretoken")
    qty_check["check"].pop("quantity")

    # Some products don't have tiers as options, so set default to 1
    qty_check["check"]["tiers"] = int(data.get("tiers", 1))

    # from POST dictionary turn values from list to string
    for key, value in qty_check["check"].items():
        if isinstance(value, list):
            qty_check["check"][key] = value[0]

    qty_check["check"].update(
        {"name": product.name, "product_id": product.id})

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

    # If items don't match then add a new item to the basket
    # Ensure item_id is unique or it will overwrite items in basket

    if not qty_change:
        current_items = [x for x in basket]
        counter = 1
        item_id = "item_" + str(len(basket) + counter)

        while item_id in current_items:
            counter += 1
            item_id = "item_" + str(len(basket) + counter)

        basket[item_id] = {}
        basket[item_id]["name"] = product.name
        basket[item_id]["product_id"] = product.id
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
