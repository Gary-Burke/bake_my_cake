from django.test import TestCase
from django.urls import reverse
from products.models import Product, Category


class TestBasketViews(TestCase):

    def setUp(self):
        """
        Set up mock data for instance of Category and Product.
        Create valid POST request data.
        """
        self.category = Category.objects.create(
            name="birthday_cakes", display_name="Birthday Cakes")

        self.product = Product.objects.create(
            name="Test Cake", slug="test-cake", tags="Some,Tags",
            shape="round", category=self.category, base_price="199.00",
        )

        self.valid_post_data = {
            "size": "small", "tiers": "1",
            "sponge": "vanilla", "filling": "vanilla",
            "icing": "royal_icing", "main_colour": "Blue",
            "secondary_colour": "White", "cake_topper": "None",
            "quantity": "1",
        }

    def test_render_basket_page(self):
        """
        Test GET renders the basket page.
        """
        response = self.client.get(reverse("view_basket"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "basket/basket.html")

    def test_add_to_basket(self):
        """
        Test POST adds item to session basket and redirects.
        Displays confirmation message to user.
        """
        response = self.client.post(
            reverse("add_to_basket", args=[self.product.pk]),
            self.valid_post_data, follow=True
        )

        messages = list(response.context["messages"])
        self.assertEqual(len(messages), 1)
        self.assertIn("has been added to your basket!", str(messages[0]))

        self.assertRedirects(
            response, reverse("products"),
            fetch_redirect_response=False
        )
        basket = self.client.session.get("basket", {})
        self.assertEqual(len(basket), 1)

    def test_delete_from_basket(self):
        """
        Test delete item from basket removes it from the session basket.
        Displays Django confirmation message.
        """
        # Add item to basket, count = 1
        self.client.post(
            reverse("add_to_basket", args=[self.product.pk]),
            self.valid_post_data
        )
        self.assertEqual(len(self.client.session.get("basket", {})), 1)

        # Delete item from basket, count = 0
        response = self.client.post(
            reverse("delete_from_basket", args=["item_1"]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(self.client.session.get("basket", {})), 0)

        # Use wsgi_request._messages to test for messages
        # since the view returns HttpResponse and not a template
        messages = list(response.wsgi_request._messages)
        # Get only the last message — add_to_basket also adds one
        last_message = str(messages[-1])
        self.assertIn("has been removed from your basket!", last_message)

    def test_edit_basket_get_renders_form(self):
        """
        Test GET on edit_basket renders the edit template and form.
        """
        self.client.post(
            reverse("add_to_basket", args=[self.product.pk]),
            self.valid_post_data
        )

        response = self.client.get(
            reverse("edit_basket", args=["item_1"]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "basket/edit_basket.html")
        self.assertIn("product", response.context)
        self.assertIn("edit_form", response.context)

    def test_edit_basket_post_updates_item(self):
        """
        Test POST on edit_basket updates item and redirects.
        Displays Django confirmation message.
        """
        self.client.post(
            reverse("add_to_basket", args=[self.product.pk]),
            self.valid_post_data
        )

        updated_data = dict(self.valid_post_data)
        updated_data["sponge"] = "chocolate"

        response = self.client.post(
            reverse("edit_basket", args=["item_1"]), updated_data)

        self.assertRedirects(
            response, reverse("view_basket"),
            fetch_redirect_response=False
        )

        # Test if sponge was actually updated in the basket session
        basket = self.client.session.get("basket", {})
        basket_item = list(basket.values())[0]
        self.assertEqual(basket_item["sponge"], "chocolate")

        # Use wsgi_request._messages to test for messages
        # since the view returns HttpResponse and not a template
        messages = list(response.wsgi_request._messages)
        # Get only the last message — add_to_basket also adds one
        last_message = str(messages[-1])
        self.assertIn("Your basket has been updated!", last_message)
