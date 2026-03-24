from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    """
    Form to add user and purchase details to order
    """
    class Meta:
        """
        :model:`checkout.Order`
        """
        model = Order
        fields = (
            "name_surname", "phone_number", "street_address1",
            "street_address2", "town_or_city", "state", "postcode",
            "country"
        )
