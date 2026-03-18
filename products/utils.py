from .constants import PRODUCT_COST, PRODUCT_COST_CUPCAKE
from decimal import Decimal


def calculate_total(request, product):

    sponge = Decimal(
        str(PRODUCT_COST["sponge"].get(request.GET.get("sponge"), 0)))
    filling = Decimal(
        str(PRODUCT_COST["filling"].get(request.GET.get(
            "filling"), 0))
    )
    icing = Decimal(
        str(PRODUCT_COST["icing"].get(request.GET.get("icing"), 0)))

    if product.shape == "cupcake":
        size = Decimal(
            str(PRODUCT_COST_CUPCAKE["size"].get(request.GET.get(
                "size"), 1))
        )
    else:
        size = Decimal(
            str(PRODUCT_COST["size"].get(request.GET.get("size"), 1)))
    tiers = Decimal(
        str(PRODUCT_COST["tiers"].get(request.GET.get("tiers"), 1)))
    quantity = Decimal(
        str(PRODUCT_COST["quantity"].get(request.GET.get(
            "quantity"), 1))
    )

    total = (((product.base_price + sponge + filling + icing)
              * size) * tiers) * quantity

    return total
