from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    """
    Form to add user details to user profile
    """
    email = forms.EmailField(
        max_length=80, label="Billing Email", required=False)
    name_surname = forms.CharField(
        max_length=255, label="Name and Surname", required=False)
    town_or_city = forms.CharField(
        max_length=40, label="Town or City", required=False)
    street_address1 = forms.CharField(
        max_length=80, label="Street Address 1", required=False)
    street_address2 = forms.CharField(
        max_length=80, label="Street Address 2", required=False)

    class Meta:
        """
        :model:`profiles.UserProfile`
        """
        model = UserProfile
        exclude = ("user",)
