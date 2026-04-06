from django.test import TestCase
from .forms import OrderForm


class TestOrderForm(TestCase):

    def test_order_form_is_valid(self):
        """Test all required fields makes form valid."""
        form = OrderForm({
            "name_surname": "John Smith",
            "phone_number": "123456789",
            "email": "john@test.com",
            "street_address1": "123 Test Street",
            "street_address2": "",
            "town_or_city": "Test City",
            "state": "Test State",
            "postcode": "12345",
            "country": "DE",
        })
        self.assertTrue(form.is_valid(), msg=f"Form errors: {form.errors}")

    def test_order_form_missing_required_fields_is_invalid(self):
        """Test empty form is invalid."""
        form = OrderForm({})
        self.assertFalse(form.is_valid(), msg="Form should be invalid")

    def test_order_form_invalid_email_is_invalid(self):
        """Test invalid email makes form invalid."""
        form = OrderForm({
            "name_surname": "John Smith",
            "phone_number": "123456789",
            "email": "not-a-valid-email",
            "street_address1": "123 Test Street",
            "town_or_city": "Test City",
            "state": "Test State",
            "postcode": "12345",
            "country": "DE",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_street_address2_is_not_required(self):
        """Test street_address2 is optional."""
        form = OrderForm({
            "name_surname": "John Smith",
            "phone_number": "123456789",
            "email": "john@test.com",
            "street_address1": "123 Test Street",
            "town_or_city": "Test City",
            "state": "Test State",
            "postcode": "12345",
            "country": "DE",
        })
        self.assertTrue(form.is_valid(), msg=f"Form errors: {form.errors}")
