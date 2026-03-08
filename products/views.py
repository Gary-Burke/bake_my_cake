from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.http import JsonResponse
from .models import Product
from .contexts import product_cost
from decimal import Decimal

# Create your views here.


class ProductList(ListView):
    """
    Returns all products in :model:`products.Product`

    **Context**

    ``queryset``
    All instances of products in :model:`products.Product` based on:
     - filter by category input
     - sort by user input
     - pagination by 24

    **Template**
    :template:`products/products.html`
    """

    template_name = "products/products.html"
    context_object_name = "products_list"
    paginate_by = 24

    def get_queryset(self):

        queryset = Product.objects.all()

        if "category" in self.request.GET:
            category = self.request.GET.get("category")
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

        if "sort" in self.request.GET:
            sort_key = self.request.GET.get("sort")
            sort_direction = self.request.GET.get("direction")

            if sort_key == "price":
                sort_key = "base_price"

            if sort_direction == "asc":
                sort = sort_key
            else:
                sort = f"-{sort_key}"

            return queryset.order_by(sort)

        return queryset.order_by("name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["current_category"] = self.request.GET.get("category")

        sort = self.request.GET.get("sort")
        direction = self.request.GET.get("direction")
        context["current_sorting"] = f"{sort}_{direction}"

        query_params = self.request.GET.copy()
        query_params.pop("page", None)
        context["query_string"] = query_params.urlencode()

        return context


def product_details(request, slug, product_id):
    """
    """
    product = get_object_or_404(Product, pk=product_id)
    current_cost = product_cost(request)
    template = "products/product_details.html"

    if request.GET.get("sponge"):
        try:
            sponge_cost = Decimal(
                str(current_cost["sponge"].get(request.GET.get("sponge"), 0)))
            filling_cost = Decimal(
                str(current_cost["filling"].get(request.GET.get("filling"), 0))
            )
            icing_cost = Decimal(
                str(current_cost["icing"].get(request.GET.get("icing"), 0)))
            size_cost = Decimal(
                str(current_cost["size"].get(request.GET.get("size"), 1)))
            tiers_cost = Decimal(
                str(current_cost["tiers"].get(request.GET.get("tiers"), 1)))

            total = ((product.base_price + sponge_cost + filling_cost
                      + icing_cost) * size_cost) * tiers_cost

            return JsonResponse(
                {"total": str(total.quantize(Decimal("0.01")))}
            )

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    context = {
        "product": product,
    }

    return render(request, template, context)
