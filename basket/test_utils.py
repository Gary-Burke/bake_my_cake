from django.test import TestCase, RequestFactory
from django.contrib.sessions.backends.db import SessionStore
from products.models import Product, Category
from basket.utils import check_basket
from decimal import Decimal


class TestCheckBasket(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.category = Category.objects.create(
            name="birthday_cakes", display_name="Birthday Cakes")
        self.product = Product.objects.create(
            name="Test Cake", slug="test-cake", tags="Some,Tags",
            shape="round", category=self.category, base_price="199.00",
        )

    def _make_request(self, post_data):
        """Helper to build a POST request with session support."""
        request = self.factory.post("/", post_data)
        request.session = SessionStore()
        request.session.create()
        return request

    def _base_post_data(self, overrides=None):
        data = {
            "size": "small",
            "tiers": "1",
            "sponge": "vanilla",
            "filling": "vanilla",
            "icing": "royal_icing",
            "main_colour": "Blue",
            "secondary_colour": "White",
            "cake_topper": "None",
            "quantity": "1",
        }
        if overrides:
            data.update(overrides)
        return data

    def test_new_item_added_to_empty_basket(self):
        """Test a new item is added when basket is empty."""
        request = self._make_request(self._base_post_data())
        basket = {}
        check_basket(request, basket, self.product, "199.00")
        self.assertEqual(len(basket), 1)
        self.assertIn("item_1", basket)
        self.assertEqual(basket["item_1"]["sponge"], "vanilla")

    def test_duplicate_item_increases_quantity_and_total(self):
        """Test adding same item again increases qty and total."""
        request = self._make_request(self._base_post_data())
        basket = {
            "item_1": {
                "name": self.product.name,
                "product_id": self.product.pk,
                "size": "small", "tiers": 1,
                "sponge": "vanilla", "filling": "vanilla",
                "icing": "royal_icing", "main_colour": "Blue",
                "secondary_colour": "White", "cake_topper": "None",
                "quantity": 1, "total": "199.00",
            }
        }
        check_basket(request, basket, self.product, "199.00")
        self.assertEqual(len(basket), 1)  # No new item added
        self.assertEqual(basket["item_1"]["quantity"], 2)
        self.assertEqual(Decimal(basket["item_1"]["total"]), Decimal("398.00"))

    def test_different_item_added_as_new_entry(self):
        """Test item with different options is added as a new basket entry."""
        request = self._make_request(
            self._base_post_data({"sponge": "chocolate"}))
        basket = {
            "item_1": {
                "name": self.product.name,
                "product_id": self.product.pk,
                "size": "small", "tiers": 1,
                "sponge": "vanilla", "filling": "vanilla",
                "icing": "royal_icing", "main_colour": "Blue",
                "secondary_colour": "White", "cake_topper": "None",
                "quantity": 1, "total": "199.00",
            }
        }
        check_basket(request, basket, self.product, "199.00")
        self.assertEqual(len(basket), 2)  # New item added

    def test_invalid_sponge_defaults_to_vanilla(self):
        """Test invalid sponge value is replaced with default."""
        request = self._make_request(
            self._base_post_data({"sponge": "invalid_hacked_value"}))
        basket = {}
        check_basket(request, basket, self.product, "199.00")
        self.assertEqual(basket["item_1"]["sponge"], "vanilla")

    def test_invalid_filling_defaults(self):
        """Test invalid filling value is replaced with default."""
        request = self._make_request(
            self._base_post_data({"filling": "hacked_filling"}))
        basket = {}
        check_basket(request, basket, self.product, "199.00")
        self.assertEqual(basket["item_1"]["filling"], "vanilla")

    def test_invalid_icing_defaults(self):
        """Test invalid icing value is replaced with default."""
        request = self._make_request(
            self._base_post_data({"icing": "hacked_icing"}))
        basket = {}
        check_basket(request, basket, self.product, "199.00")
        self.assertEqual(basket["item_1"]["icing"], "royal_icing")

    def test_unique_item_id_generated_when_id_already_exists(self):
        """Test item_id increments correctly to avoid overwriting items."""
        request = self._make_request(
            self._base_post_data({"sponge": "chocolate"}))
        # Pre-fill basket with item_1 and item_2 already taken
        basket = {
            "item_1": {
                "name": self.product.name, "product_id": self.product.pk,
                "size": "small", "tiers": 1, "sponge": "vanilla",
                "filling": "vanilla", "icing": "royal_icing",
                "main_colour": "Blue", "secondary_colour": "White",
                "cake_topper": "None", "quantity": 1, "total": "199.00",
            },
        }
        check_basket(request, basket, self.product, "199.00")
        self.assertIn("item_2", basket)
