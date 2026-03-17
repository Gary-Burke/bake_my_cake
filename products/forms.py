from django import forms
from cloudinary.forms import CloudinaryFileField
from .models import Product, Category


class ProductForm(forms.ModelForm):
    """
    Form to add products to database for superuser
    """
    image_url = CloudinaryFileField(
        label="Image Upload", options={'folder': 'products'},
        required=True)
    name = forms.CharField(
        max_length=255, label="Name of Cake",
        widget=forms.TextInput(
            attrs={"placeholder": "e.g. Death by Chocolate"})
    )
    tags = forms.CharField(
        max_length=255, label="Search Tags",
        widget=forms.TextInput(
            attrs={"placeholder": "e.g. Frozen, Disney, Elsa"}))
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=True
    )

    class Meta:
        """
        :model:`products.Product`
        """
        model = Product
        fields = (
            "name", "tags", "shape", "category",
            "base_price", "image_url",
        )


class EditProductForm(forms.ModelForm):
    """
    Form to edit products from the database for superuser
    """
    image_url = CloudinaryFileField(
        label="Image Upload", options={'folder': 'products'},
        required=False)

    class Meta:
        """
        :model:`products.Product`
        """
        model = Product
        fields = (
            "name", "tags", "shape", "category",
            "base_price", "image_url",
        )
