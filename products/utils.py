from .constants import PRODUCT_COST, PRODUCT_COST_CUPCAKE
from decimal import Decimal


def calculate_total(request, product):
    """
    Business logic for calculating the cost of a product based on the user
    customization input. This function returns the total cost of a product
    including the quantity selected.
    """

    data = request.GET if request.method == "GET" else request.POST

    sponge = Decimal(PRODUCT_COST["sponge"].get(data.get("sponge"), 0))
    filling = Decimal(PRODUCT_COST["filling"].get(data.get("filling"), 0))
    icing = Decimal(PRODUCT_COST["icing"].get(data.get("icing"), 0))
    tiers = Decimal(PRODUCT_COST["tiers"].get(data.get("tiers"), 1))
    quantity = Decimal(PRODUCT_COST["quantity"].get(data.get("quantity"), 1))

    if product.shape == "cupcake":
        size = Decimal(PRODUCT_COST_CUPCAKE["size"].get(data.get("size"), 1))
    else:
        size = Decimal(PRODUCT_COST["size"].get(data.get("size"), 1))

    base_price = Decimal(product.base_price)

    total = (
        ((base_price + sponge + filling + icing) * size) * tiers) * quantity

    total = str(total.quantize(Decimal("0.01")))

    return total
