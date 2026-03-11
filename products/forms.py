from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    """
    Form to add products to database for superuser
    """
    class Meta:
        """
        :model:`products.Product`
        """
        model = Product
        fields = (
            "name",
            "shape",
            "category",
            "base_price",
            "image_url",
        )
