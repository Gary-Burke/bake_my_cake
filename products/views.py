from django.shortcuts import render
from django.views.generic import ListView
from .models import Product

# Create your views here.


class CakeList(ListView):
    """
    """
    template_name = "products/cakes.html"
    context_object_name = "cakes_list"

    def get_queryset(self):
        queryset = Product.objects.all()

        return queryset.order_by("name")
