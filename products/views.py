from django.shortcuts import render
from django.views.generic import ListView
from .models import Product, Category

# Create your views here.


class ProductList(ListView):
    """
    Returns all products in :model:`products.Product`

    **Context**

    ``queryset``
    All instances of products in :model:`products.Product` based on:
     - filter by category

    **Template**
    :template:`products/products.html`
    """

    template_name = "products/products.html"
    context_object_name = "products_list"

    def get_queryset(self):
        print(self.request.GET)  # TODO: Delete print
        print(self.request.path)  # TODO: Delete print
        queryset = Product.objects.all()

        category = self.request.GET.get("category")
        print(category)  # TODO: Delete print

        allowed_categories = [
            "all-cakes", "kids-cakes", "birthday-cakes",
            "event-cakes", "cupcakes"
        ]

        if category not in allowed_categories:
            return queryset
        elif category == "all-cakes":
            queryset = queryset.exclude(category__name="cupcakes")
        else:
            queryset = queryset.filter(category__name=category)

        return queryset.order_by("name")
