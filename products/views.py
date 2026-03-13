from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.http import JsonResponse
from django.db.models.functions import Lower
from .models import Product
from .constants import PRODUCT_COST, PRODUCT_COST_CUPCAKE
from decimal import Decimal
from .forms import ProductForm, EditProductForm

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
    is_admin_view = False

    def get_queryset(self):

        queryset = Product.objects.all()
        sort = "name"

        # Filter by user category selection
        if "category" in self.request.GET:
            category = self.request.GET.get("category")
            allowed_categories = [
                "all-cakes", "kids-cakes", "birthday-cakes",
                "event-cakes", "cupcakes"
            ]

            if category in allowed_categories:
                if category == "all-cakes":
                    queryset = queryset.exclude(category__name="cupcakes")
                else:
                    queryset = queryset.filter(category__name=category)

        # Sort by user selection
        if "sort" in self.request.GET:
            sort_key = self.request.GET.get("sort")
            allowed_keys = ["price", "name"]

            if sort_key not in allowed_keys:
                sort_key = "name"

            sort_direction = self.request.GET.get("direction")
            allowed_direction = ["asc", "desc"]

            if sort_direction not in allowed_direction:
                sort_direction = "asc"

            # Django sorts capital and lowercase letters differently.
            # Converting all to lowercase ensures correct sorting
            if sort_key == 'name':
                sort_key = 'lower_name'
                queryset = queryset.annotate(lower_name=Lower('name'))

            if sort_key == "price":
                sort_key = "base_price"

            if sort_direction == "asc":
                sort = sort_key
            else:
                sort = f"-{sort_key}"

        return queryset.order_by(sort)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["current_category"] = self.request.GET.get("category")

        sort = self.request.GET.get("sort")
        direction = self.request.GET.get("direction")
        context["current_sorting"] = f"{sort}_{direction}"

        query_params = self.request.GET.copy()
        query_params.pop("page", None)
        context["query_string"] = query_params.urlencode()

        context["is_admin_view"] = self.is_admin_view

        return context


class ProductListAdmin(LoginRequiredMixin, ProductList):
    is_admin_view = True


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
        product_form = ProductForm(data=request.POST, files=request.FILES)
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


@login_required
def edit_product(request, product_id):
    """
    Display an instance to edit of :model:`products.Product`

    **Context**
    ``edit_product_form``
     An instance of :form:`products.EditProductForm`

    **Template**
    :template:`products/edit_product.html`
    """
    if not request.user.is_superuser:
        messages.add_message(
            request, messages.ERROR,
            "Access to the database is only permitted for Admins!"
        )
        return redirect(reverse('index'))

    product = get_object_or_404(Product, pk=product_id)

    if request.method == "POST":

        edit_product_form = EditProductForm(
            data=request.POST, instance=product, files=request.FILES)

        if edit_product_form.is_valid():
            product = edit_product_form.save()
            messages.add_message(request, messages.SUCCESS,
                                 f"{product.name} successfully updated!")
            return redirect(reverse('products_admin'))
        else:
            messages.add_message(
                request, messages.ERROR, f"Unable to update {product.name} "
                "at this moment. Please try again later."
            )

    else:
        edit_product_form = EditProductForm(instance=product)

    template = "products/edit_product.html"
    context = {
        "product": product,
        "edit_product_form": edit_product_form,
    }

    return render(request, template, context)
