

def basket_contents(request):
    """
    The context of this function is made available across
    all templates by adding it to settings.py as a context_processor
    """

    basket = request.session.get("basket", {})
    basket_qty = 0
    if len(basket):
        for item in basket.values():
            basket_qty += int(item["quantity"])

    context = {
        "basket_qty": basket_qty,
    }

    return context
