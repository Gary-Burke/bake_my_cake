from django import forms
from cloudinary.forms import CloudinaryFileField
from .models import CustomOrder


class CustomOrderForm(forms.ModelForm):
    """
    Form for user to submit custom order.
    """
    image_url = CloudinaryFileField(
        label="Image Upload", options={'folder': 'custom orders'},
        required=False)
    name = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={"placeholder": "e.g. John"}))
    email = forms.EmailField(max_length=255, widget=forms.TextInput(
        attrs={"placeholder": "e.g. John@testmail.com"}))
    shape = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={"placeholder": "e.g. Hexagon, L-Shaped or Heart"}))
    size = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={"placeholder": "e.g. 20 x 30cm"}))
    tiers = forms.IntegerField(widget=forms.TextInput(
        attrs={"placeholder": "e.g. 1 (we offer 1-3 tier options)"}))
    sponge = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={"placeholder": "e.g. Red Velvet"}))
    filling = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={"placeholder": "e.g. Caramel Treat"}))
    icing = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={"placeholder": "e.g. Buttercream"}))
    additional_info = forms.CharField(
        max_length=255, required=False, widget=forms.TextInput(
            attrs={"placeholder": "e.g. Paw Patrol, "
                   "6 year old boy, birthday party"}))

    class Meta:
        """
        :model:`pages.CustomOrder`
        """
        model = CustomOrder
        fields = (
            "name", "email", "shape", "size", "tiers", "sponge",
            "filling", "icing", "additional_info", "image_url",
        )
