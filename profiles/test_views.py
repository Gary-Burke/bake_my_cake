from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import UserProfileForm
from .models import UserProfile

# Create your tests here.


class TestUserProfilesViews(TestCase):
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

    def test_render_profile_page_with_userprofile_form(self):
        """
        Test GET renders profile page with a UserProfile form in context.
        """
        self.client.login(username="myUsername", password="myPassword")
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profiles/profile.html")
        self.assertIsInstance(
            response.context["userprofile_form"], UserProfileForm
        )
        self.assertContains(response, "Someone")

    def test_successful_profile_update(self):
        """
        Test valid POST updates profile and shows success message.
        """
        self.client.login(username="myUsername", password="myPassword")
        profile_data = {
            "name_surname": "Updated Name",
            "phone_number": "987654",
            "email": "updated@test.com",
            "street_address1": "New Street",
            "street_address2": "",
            "town_or_city": "New City",
            "state": "New State",
            "postcode": "54321",
            "country": "GB",
        }
        response = self.client.post(reverse("profile"), profile_data)
        self.assertEqual(response.status_code, 200)
        # Profile was updated in the DB
        self.userprofile.refresh_from_db()
        self.assertEqual(self.userprofile.name_surname, "Updated Name")
        self.assertEqual(self.userprofile.town_or_city, "New City")
        # Success message shown
        messages = list(response.context["messages"])
        self.assertEqual(len(messages), 1)
        self.assertIn(
            "Your profile has been successfully updated!", str(messages[0]))

    def test_invalid_profile_update(self):
        """
        Test invalid POST does not update profile and shows error message.
        """
        self.client.login(username="myUsername", password="myPassword")
        profile_data = {
            "email": "not-a-valid-email",
        }
        response = self.client.post(reverse("profile"), profile_data)
        self.assertEqual(response.status_code, 200)
        # Profile name unchanged in DB
        self.userprofile.refresh_from_db()
        self.assertEqual(self.userprofile.name_surname, "Someone")
        # Error message shown
        messages = list(response.context["messages"])
        self.assertEqual(len(messages), 1)
        self.assertIn(
            "Unable to update your profile.", str(messages[0]))

    def test_profile_view_requires_login(self):
        """
        Test unauthenticated users are redirected away from the profile.
        """
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, f"/accounts/login/?next={reverse('profile')}")

    def test_render_order_list_page(self):
        """
        Test authenticated user can access their order list.
        """
        self.client.login(username="myUsername", password="myPassword")
        response = self.client.get(reverse("order_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profiles/profile.html")
        self.assertIn("order_list", response.context)

    def test_order_list_requires_login(self):
        """
        Test unauthenticated users are redirected away from order list.
        """
        response = self.client.get(reverse("order_list"))
        self.assertEqual(response.status_code, 302)
