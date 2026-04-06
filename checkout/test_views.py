import json
from unittest.mock import patch, MagicMock
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date, timedelta

from .models import Order
from .forms import OrderForm
from products.models import Product, Category
from profiles.models import UserProfile


# Shared valid order data used across multiple tests
VALID_ORDER_DATA = {
    "name_surname": "John Smith",
    "phone_number": "123456789",
    "email": "john@test.com",
    "street_address1": "123 Test Street",
    "street_address2": "",
    "town_or_city": "Test City",
    "state": "Test State",
    "postcode": "12345",
    "country": "DE",
    "delivery_date": (date.today() + timedelta(days=5)).strftime("%Y-%m-%d"),
    "save_info": False,
}

# Minimal basket stored in session
VALID_BASKET = {
    "item_1": {
        "product_id": None,  # Set in setUp after product is created
        "size": "20x30cm",
        "tiers": 2,
        "sponge": "Vanilla",
        "filling": "Caramel",
        "icing": "Buttercream",
        "main_colour": "Blue",
        "secondary_colour": "White",
        "cake_topper": "None",
        "quantity": 1,
        "total": "199.00",
    }
}


class TestCheckoutView(TestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(
            username="myUsername",
            password="myPassword",
            email="test@test.com"
        )
        self.category = Category.objects.create(
            name="birthday_cakes",
            display_name="Birthday Cakes"
        )
        self.product = Product.objects.create(
            name="Test Cake",
            slug="test-cake",
            tags="Some,Tags",
            shape="round",
            category=self.category,
            base_price="199.00",
        )
        # Update basket with real product id after creation
        self.basket = dict(VALID_BASKET)
        self.basket["item_1"] = dict(VALID_BASKET["item_1"])
        self.basket["item_1"]["product_id"] = self.product.pk

    def test_checkout_redirects_with_empty_basket(self):
        """Test empty basket redirects away from checkout."""
        response = self.client.get(reverse("checkout"))
        self.assertRedirects(response, reverse("products"))

    def test_render_checkout_page_with_order_form(self):
        """Test GET with basket renders checkout with OrderForm."""
        session = self.client.session
        session["basket"] = self.basket
        session.save()
        response = self.client.get(reverse("checkout"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "checkout/checkout.html")
        self.assertIsInstance(response.context["order_form"], OrderForm)
        self.assertIn("stripe_public_key", response.context)
        self.assertIn("date_context", response.context)

    def test_checkout_prepopulates_form_for_logged_in_user(self):
        """Test form is prepopulated from UserProfile for logged in users."""
        self.client.login(username="myUsername", password="myPassword")
        profile, _ = UserProfile.objects.get_or_create(user=self.user)
        profile.email = "profile@test.com"
        profile.name_surname = "Profile User"
        profile.save()

        session = self.client.session
        session["basket"] = self.basket
        session.save()

        response = self.client.get(reverse("checkout"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "profile@test.com")


class TestValidateOrderFormView(TestCase):

    def test_valid_form_data_returns_valid_true(self):
        """Test valid JSON POST returns valid: true."""
        response = self.client.post(
            reverse("validate"),
            data=json.dumps(VALID_ORDER_DATA),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data["valid"])

    def test_missing_delivery_date_returns_valid_false(self):
        """Test missing delivery date returns valid: false with error."""
        order_data = dict(VALID_ORDER_DATA)
        order_data["delivery_date"] = ""
        response = self.client.post(
            reverse("validate"),
            data=json.dumps(order_data),
            content_type="application/json"
        )
        data = json.loads(response.content)
        self.assertFalse(data["valid"])
        self.assertIn("delivery_date", data["errors"])

    def test_invalid_form_data_returns_valid_false(self):
        """Test invalid email returns valid: false with errors."""
        order_data = dict(VALID_ORDER_DATA)
        order_data["email"] = "not-a-valid-email"
        response = self.client.post(
            reverse("validate"),
            data=json.dumps(order_data),
            content_type="application/json"
        )
        data = json.loads(response.content)
        self.assertFalse(data["valid"])
        self.assertIn("email", data["errors"])


class TestCheckoutCompleteView(TestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(
            username="myUsername",
            password="myPassword",
            email="test@test.com"
        )
        self.category = Category.objects.create(
            name="birthday_cakes",
            display_name="Birthday Cakes"
        )
        self.product = Product.objects.create(
            name="Test Cake",
            slug="test-cake",
            tags="Some,Tags",
            shape="round",
            category=self.category,
            base_price="199.00",
        )
        self.basket = dict(VALID_BASKET)
        self.basket["item_1"] = dict(VALID_BASKET["item_1"])
        self.basket["item_1"]["product_id"] = self.product.pk

    @patch("checkout.views.send_confirmation_email")
    @patch("checkout.views.stripe.checkout.Session.retrieve")
    def test_checkout_complete_creates_order_line_items(
            self, mock_retrieve, mock_email):
        """
        Test successful payment creates an OrderLineItem for each basket item.
        """
        mock_retrieve.return_value = self._mock_stripe_session()

        session = self.client.session
        session["pending_order"] = VALID_ORDER_DATA
        session["basket"] = self.basket
        session.save()

        self.client.get(
            reverse("checkout_complete") + "?session_id=test123")

        order = Order.objects.first()
        # One line item created per basket item
        self.assertEqual(order.lineitem.count(), 1)
        line_item = order.lineitem.first()
        self.assertEqual(line_item.product, self.product)
        self.assertEqual(line_item.sponge, "Vanilla")
        self.assertEqual(line_item.size, "20x30cm")

    @patch("checkout.views.send_confirmation_email")
    @patch("checkout.views.stripe.checkout.Session.retrieve")
    def test_checkout_complete_invalid_product_deletes_order(
            self, mock_retrieve, mock_email):
        """
        Test basket with non-existent product deletes the order and redirects.
        """
        mock_retrieve.return_value = self._mock_stripe_session()

        # Point basket at a product ID that doesn't exist
        bad_basket = dict(self.basket)
        bad_basket["item_1"] = dict(self.basket["item_1"])
        bad_basket["item_1"]["product_id"] = 99999

        session = self.client.session
        session["pending_order"] = VALID_ORDER_DATA
        session["basket"] = bad_basket
        session.save()

        response = self.client.get(
            reverse("checkout_complete") + "?session_id=test123")

        # Order should have been deleted after the bad product was found
        self.assertEqual(Order.objects.count(), 0)
        self.assertRedirects(
            response, reverse("view_basket"),
            fetch_redirect_response=False)

    def _mock_stripe_session(self, payment_status="paid"):
        """Helper to build a mock Stripe session."""
        mock_session = MagicMock()
        mock_session.payment_status = payment_status
        mock_session.payment_intent = "pi_test123"
        mock_session.amount_total = 19900  # £199.00 in pence
        return mock_session

    @patch("checkout.views.stripe.checkout.Session.retrieve")
    def test_checkout_complete_no_session_id_redirects(self, mock_retrieve):
        """Test missing session_id redirects to checkout."""
        response = self.client.get(reverse("checkout_complete"))
        self.assertRedirects(
            response, reverse("checkout"),
            fetch_redirect_response=False
            )

    @patch("checkout.views.stripe.checkout.Session.retrieve")
    def test_checkout_complete_unpaid_redirects(self, mock_retrieve):
        """Test unpaid session redirects back to checkout."""
        mock_retrieve.return_value = self._mock_stripe_session(
            payment_status="unpaid")
        response = self.client.get(
            reverse("checkout_complete") + "?session_id=test123")
        self.assertRedirects(
            response, reverse("checkout"),
            fetch_redirect_response=False
            )

    @patch("checkout.views.send_confirmation_email")
    @patch("checkout.views.stripe.checkout.Session.retrieve")
    def test_checkout_complete_creates_order(
            self, mock_retrieve, mock_email):
        """Test successful payment creates Order and renders complete page."""
        mock_retrieve.return_value = self._mock_stripe_session()

        # Set up session with pending order and basket
        session = self.client.session
        session["pending_order"] = VALID_ORDER_DATA
        session["basket"] = self.basket
        session.save()

        response = self.client.get(
            reverse("checkout_complete") + "?session_id=test123")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "checkout/complete.html")
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.first()
        self.assertEqual(order.stripe_pid, "pi_test123")
        self.assertIn("order", response.context)
        mock_email.assert_called_once()

    @patch("checkout.views.send_confirmation_email")
    @patch("checkout.views.stripe.checkout.Session.retrieve")
    def test_checkout_complete_clears_session(
            self, mock_retrieve, mock_email):
        """
        Test basket and pending_order are cleared from session after checkout.
        """
        mock_retrieve.return_value = self._mock_stripe_session()

        session = self.client.session
        session["pending_order"] = VALID_ORDER_DATA
        session["basket"] = self.basket
        session.save()

        self.client.get(
            reverse("checkout_complete") + "?session_id=test123")

        # Reload session and confirm keys are gone
        session = self.client.session
        self.assertNotIn("basket", session)
        self.assertNotIn("pending_order", session)

    @patch("checkout.views.send_confirmation_email")
    @patch("checkout.views.stripe.checkout.Session.retrieve")
    def test_checkout_complete_sends_confirmation_email(
            self, mock_retrieve, mock_email):
        """Test confirmation email is sent on successful order."""
        mock_retrieve.return_value = self._mock_stripe_session()

        session = self.client.session
        session["pending_order"] = VALID_ORDER_DATA
        session["basket"] = self.basket
        session.save()

        self.client.get(
            reverse("checkout_complete") + "?session_id=test123")
        mock_email.assert_called_once()
