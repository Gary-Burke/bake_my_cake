from django import forms
from cloudinary.forms import CloudinaryFileField
from .models import Product


class ProductForm(forms.ModelForm):
    """
    Form to add products to database for superuser
    """
    image_url = CloudinaryFileField(
        options={'folder': 'products'},
        required=False
    )

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


class EditProductForm(forms.ModelForm):
    """
    Form to edit products from the database for superuser
    """
    image_url = CloudinaryFileField(
        options={'folder': 'products'},
        required=False
    )

    class Meta:
        """
        :model:`products.Product`
        """
        model = Product
        fields = (
            "name",
            "tags",
            "shape",
            "category",
            "base_price",
            "image_url",
        )
