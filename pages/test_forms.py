from django.test import TestCase
from .forms import CustomOrderForm


# Create your tests here.


class TestCustomOrderForm(TestCase):

    def test_form_is_valid(self):
        """
        Test all required fields to be completed.
        ``Form``
        :form:`pages.CustomOrderForm`
        """

        form = CustomOrderForm({
            "name": "Test-User",
            "email": "test@test.com",
            "shape": "Hexagon",
            "size": "20x30cm",
            "tiers": "2",
            "sponge": "Strawberry",
            "filling": "Lemon",
            "icing": "Ganache",
        })
        self.assertTrue(
            form.is_valid(),
            msg="Form is not valid, missing fields"
        )

    def test_tiers_out_of_range_is_invalid(self):
        """
        Test field tiers to be invalid when range is outside of 1-3.
        ``Form``
        :form:`pages.CustomOrderForm`
        """

        form = CustomOrderForm({
            "name": "Test-User",
            "email": "test@test.com",
            "shape": "Hexagon",
            "size": "20x30cm",
            "tiers": "4",
            "sponge": "Strawberry",
            "filling": "Lemon",
            "icing": "Ganache",
        })
        self.assertFalse(
            form.is_valid(),
            msg="Tiers value is valid - within min/max range"
        )
