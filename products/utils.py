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

    # Prevent HTML form hacking by checking values with predefined values
    # If values are not valid then assign default values for total calculation
    # No need to add cupcake check since they have the same values

    sponge = 0 if data.get("sponge") not in PRODUCT_COST["sponge"] else sponge
    filling = 0 if data.get(
        "filling") not in PRODUCT_COST["filling"] else filling
    icing = 0 if data.get("icing") not in PRODUCT_COST["icing"] else icing
    tiers = 1 if data.get("tiers") not in PRODUCT_COST["tiers"] else tiers
    quantity = 1 if data.get(
        "quantity") not in PRODUCT_COST["quantity"] else quantity
    size = 1 if data.get("size") not in PRODUCT_COST["size"] else size

    base_price = Decimal(product.base_price)

    total = (
        ((base_price + sponge + filling + icing) * size) * tiers) * quantity

    total = str(total.quantize(Decimal("0.01")))

    return total
