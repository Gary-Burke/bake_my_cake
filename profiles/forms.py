from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    """
    Form to add user details to user profile
    """
    email = forms.EmailField(
        max_length=80, label="Email for Billing", required=False)

    class Meta:
        """
        :model:`profiles.UserProfile`
        """
        model = UserProfile
        exclude = ("user",)
