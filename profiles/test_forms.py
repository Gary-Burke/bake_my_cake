from django.test import TestCase
from django.contrib.auth.models import User
from .forms import UserProfileForm
from .models import UserProfile

# Create your tests here.


class TestUserProfilesForms(TestCase):
    """
    Set up mock data for superuser and userprofile instance
    """

    def setUp(self):
        self.user = User.objects.create_superuser(
            username="myUsername",
            password="myPassword",
            email="test@test.com"
        )

        # Signal automatically creates the profile
        # Get or create it if not already created and update it.
        self.userprofile, _ = UserProfile.objects.get_or_create(user=self.user)
        self.userprofile.name_surname = "Someone"
        self.userprofile.phone_number = "123456"
        self.userprofile.email = "Someone@test.com"
        self.userprofile.street_address1 = "Somewhere"
        self.userprofile.town_or_city = "Some Place"
        self.userprofile.state = "Any"
        self.userprofile.postcode = "12345"
        self.userprofile.country = "DE"
        self.userprofile.save()

    def test_form_is_valid_with_no_required_fields(self):
        """
        All fields are optional so an empty form should be valid.
        """
        form = UserProfileForm({})
        self.assertTrue(form.is_valid(), msg=f"Form errors: {form.errors}")

    def test_form_is_invalid_with_invalid_email(self):
        """
        Invalid email should make the form invalid.
        """
        form = UserProfileForm({"email": "not-a-valid-email"})
        self.assertFalse(form.is_valid(), msg="Form should be invalid")
        self.assertIn("email", form.errors)
