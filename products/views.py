from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.http import JsonResponse
from .models import Product
from .constants import PRODUCT_COST, PRODUCT_COST_CUPCAKE
from decimal import Decimal
from .forms import ProductForm

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
    Returns a detailed view of a product :model:`products.Product`

    **Context**
    Imported values from constants.py used for template field generations
    and for price calculation.

    **Template**
    :template:`products/product_detail.html`
    """
    product = get_object_or_404(Product, pk=product_id)
    template = "products/product_details.html"

    # Used to loop through in template input fields
    if product.shape == "cupcake":
        product_cost = PRODUCT_COST_CUPCAKE
    else:
        product_cost = PRODUCT_COST

    if request.GET.get("sponge"):
        try:
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

            return JsonResponse(
                {"total": str(total.quantize(Decimal("0.01")))}
            )

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    context = {
        "product": product,
        "product_cost": product_cost,
    }

    return render(request, template, context)


@login_required
def add_product(request):
    """
    Creates an instance of :model:`products.Product`

    **Context**
    ``product_form``
     An instance of :form:`products.ProductForm`

    **Template**
    :template:`products/add_product.html`
    """
    if not request.user.is_superuser:
        messages.add_message(
            request, messages.ERROR,
            "Products can only be added by an Admin!"
        )
        return redirect(reverse('index'))

    if request.method == "POST":
        product_form = ProductForm(data=request.POST)
        if product_form.is_valid():
            product = product_form.save(commit=False)
            product.slug = product.name.replace(" ", "-").lower()
            product.save()
            messages.add_message(
                request, messages.SUCCESS,
                f"{product.name} was successfully added to the database!"
            )
        else:
            messages.add_message(
                request, messages.ERROR,
                "Unable to add product. Please try again later"
            )

    product_form = ProductForm()
    template = "products/add_product.html"
    context = {
        "product_form": product_form,
    }

    return render(request, template, context)
