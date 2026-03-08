
def product_cost(request):
    size = {
        "small": 1,
        "medium": 1.4,
        "large": 1.8,
    }

    tiers = {
        "one": 1,
        "two": 1.5,
        "three": 2,
    }

    sponge = {
        "vanilla": 0,
        "chocolate": 0,
        "coffee": 3,
        "carrot": 5,
        "lemon": 2,
    }

    filling = {
        "vanilla": 0,
        "chocolate": 0,
        "caramel_treat": 6,
        "strawberry_jam": 2,
        "butter_cream": 4,
    }

    icing = {
        "royal_icing": 0,
        "buttercream": 2,
        "ganache": 8,
        "fondant": 6,
        "cream_cheese": 4,
    }

    context = {
        "size": size,
        "tiers": tiers,
        "sponge": sponge,
        "filling": filling,
        "icing": icing,
    }

    return context
