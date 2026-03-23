from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    """
    Form to add user details to user profile
    """
    class Meta:
        """
        :model:`profiles.UserProfile`
        """
        model = UserProfile
        exclude = ("user",)
