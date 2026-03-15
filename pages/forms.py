from django import forms
from cloudinary.forms import CloudinaryFileField
from .models import CustomOrder


class CustomOrderForm(forms.ModelForm):
    """
    Form for user to submit custom order.
    """
    image_url = CloudinaryFileField(
        options={'folder': 'products'},
        required=False
    )

    class Meta:
        """
        :model:`pages.CustomOrder`
        """
        model = CustomOrder
        fields = (
            "name", "email", "shape", "size", "tiers", "sponge",
            "filling", "icing", "additional_info", "image_url",
        )
