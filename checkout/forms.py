from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    """
    Form to add user and purchase details to order
    """
    delivery_date = forms.DateField(label="Select a Pickup Date",
                                    widget=forms.TextInput(attrs={
                                        "id": "delivery-date",
                                        "name": "delivery_date",
                                        "placeholder": "Click to select a date...",
                                    }))
    name_surname = forms.CharField(
        max_length=255, label="Name and Surname")
    phone_number = forms.CharField(
        max_length=255, label="Phone Number")
    email = forms.EmailField(
        max_length=80,
        widget=forms.TextInput(attrs={
            "id": "email",
        })
    )
    street_address1 = forms.CharField(
        max_length=255, label="Street Address 1")
    street_address2 = forms.CharField(
        max_length=255, label="Street Address 2", required=False)
    town_or_city = forms.CharField(
        max_length=255, label="Town or City")

    class Meta:
        """
        :model:`checkout.Order`
        """
        model = Order
        fields = (
            "delivery_date", "name_surname", "phone_number", "street_address1",
            "street_address2", "town_or_city", "state", "postcode",
            "country"
        )
