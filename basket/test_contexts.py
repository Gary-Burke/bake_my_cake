from django.test import TestCase, RequestFactory
from products.models import Product, Category
from basket.contexts import basket_contents


class TestBasketContexts(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.category = Category.objects.create(
            name="birthday_cakes", display_name="Birthday Cakes")
        self.product = Product.objects.create(
            name="Test Cake", slug="test-cake", tags="Some,Tags",
            shape="round", category=self.category, base_price="199.00",
        )

    def test_empty_basket_returns_zero_values(self):
        """Test empty basket returns zero qty and total."""
        request = self.factory.get("/")
        request.session = {}
        context = basket_contents(request)
        self.assertEqual(context["basket_qty"], 0)
        self.assertEqual(context["grand_total"], "0.00")
        self.assertEqual(context["basket_items"], [])

    def test_basket_with_item_returns_correct_qty_and_total(self):
        """Test basket with one item returns correct qty and total."""
        request = self.factory.get("/")
        request.session = {
            "basket": {
                "item_1": {
                    "product_id": self.product.pk,
                    "size": "small", "tiers": 1,
                    "sponge": "vanilla", "filling": "vanilla",
                    "icing": "royal_icing", "main_colour": "Blue",
                    "secondary_colour": "White", "cake_topper": "None",
                    "quantity": 2, "total": "398.00",
                }
            }
        }
        context = basket_contents(request)
        self.assertEqual(context["basket_qty"], 2)
        self.assertEqual(context["grand_total"], "398.00")
        self.assertEqual(len(context["basket_items"]), 1)
        self.assertEqual(context["basket_items"][0]["product"], self.product)

    def test_basket_with_multiple_items_returns_combined_total(self):
        """Test multiple basket items returns combined totals."""
        request = self.factory.get("/")
        request.session = {
            "basket": {
                "item_1": {
                    "product_id": self.product.pk,
                    "size": "small", "tiers": 1,
                    "sponge": "vanilla", "filling": "vanilla",
                    "icing": "royal_icing", "main_colour": "Blue",
                    "secondary_colour": "White", "cake_topper": "None",
                    "quantity": 1, "total": "199.00",
                },
                "item_2": {
                    "product_id": self.product.pk,
                    "size": "small", "tiers": 1,
                    "sponge": "vanilla", "filling": "vanilla",
                    "icing": "royal_icing", "main_colour": "Red",
                    "secondary_colour": "White", "cake_topper": "None",
                    "quantity": 1, "total": "199.00",
                }
            }
        }
        context = basket_contents(request)
        self.assertEqual(context["basket_qty"], 2)
        self.assertEqual(context["grand_total"], "398.00")
        self.assertEqual(len(context["basket_items"]), 2)
