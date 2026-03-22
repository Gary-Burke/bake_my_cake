from decimal import Decimal
from django.shortcuts import get_object_or_404
from products.models import Product


def basket_contents(request):
    """
    The context of this function is made available across
    all templates by adding it to settings.py as a context_processor
    """

    basket = request.session.get("basket", {})
    basket_qty = int(0)
    grand_total = Decimal("0")

    if len(basket):
        for item in basket.values():
            basket_qty += int(item["quantity"])
            grand_total += Decimal(item["total"])

    basket_items = []
    for item_id, item_data in basket.items():
        product = get_object_or_404(Product, pk=item_data["product_id"])
        basket_items.append({
            "item_id": item_id,
            "product": product,
            "size": item_data["size"],
            "tiers": item_data["tiers"],
            "sponge": item_data["sponge"],
            "filling": item_data["filling"],
            "icing": item_data["icing"],
            "main_colour": item_data["main_colour"],
            "secondary_colour": item_data["secondary_colour"],
            "quantity": item_data["quantity"],
            "cake_topper": item_data["cake_topper"],
            "total": item_data["total"],
        })

    context = {
        "basket_items": basket_items,
        "basket_qty": basket_qty,
        "grand_total": grand_total.quantize(Decimal("0.01")),
    }

    return context
