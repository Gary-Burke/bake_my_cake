from django.core import mail
from django.urls import reverse
from django.test import TestCase
from .forms import CustomOrderForm
from .models import CustomOrder

# Create your tests here.


class TestPagesViews(TestCase):

    def test_render_custom_order_page_with_custom_order_form(self):
        """
        Test GET request renders the page with an empty form.

        ``View``
        :view:`pages.custom_order`

        ``Model``
        :model:`pages.CustomOrder`

        ``Form``
        :form:`pages.CustomOrderForm`

        ``Template``
        :template:`pages/custom_order.html`
        """
        response = self.client.get(reverse("custom_order"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/custom_order.html")
        self.assertIsInstance(
            response.context["custom_order_form"], CustomOrderForm
        )

    def test_successful_custom_order_submission(self):
        """
        Test POST request with valid form data.
        Saves an instance of custom_order.
        Displays Django message and sends email.
        """
        order_data = {
            "name": "Test-User",
            "email": "test@test.com",
            "shape": "Hexagon",
            "size": "20x30cm",
            "tiers": "2",
            "sponge": "Strawberry",
            "filling": "Lemon",
            "icing": "Ganache",
        }
        response = self.client.post(reverse("custom_order"), order_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CustomOrder.objects.count(), 1)
        messages = list(response.context["messages"])
        self.assertEqual(len(messages), 1)
        self.assertIn("Custom order submitted successfully!", str(messages[0]))
        self.assertEqual(len(mail.outbox), 1)

    def test_invalid_custom_order_submission(self):
        """
        Test POST request with invalid form data.
        Does not save order or send email.
        """
        order_data = {
            "name": "Test-User",
            "email": "not-a-valid-email",
            "shape": "Hexagon",
            "size": "20x30cm",
            "tiers": "2",
            "sponge": "Strawberry",
            "filling": "Lemon",
            "icing": "Ganache",
        }
        response = self.client.post(reverse("custom_order"), order_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CustomOrder.objects.count(), 0)
        self.assertEqual(len(mail.outbox), 0)
        self.assertTrue(response.context["custom_order_form"].errors)
