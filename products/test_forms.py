from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch
from .forms import ProductForm, EditProductForm
from .models import Category


class TestProductForm(TestCase):
    """
    Set up mock data for category instance
    """

    def setUp(self):
        self.category = Category.objects.create(
            name="birthday_cakes",
            display_name="Birthday Cakes"
        )

    # Code related to Cloudinary fields incl. patch decorators from Claude.ai
    # Need to patch model and form fields to test mock data with Cloudinary.
    @patch("cloudinary.models.CloudinaryField.to_python")
    @patch("cloudinary.forms.CloudinaryFileField.to_python")
    def test_product_form_is_valid(self, mock_form_field, mock_model_field):
        """
        Test all required fields to be completed - valid form data.
        """
        mock_form_field.return_value = "image/upload/test.jpg"  # String
        mock_model_field.return_value = "image/upload/test.jpg"
        dummy_image = SimpleUploadedFile(
            "test.jpg", b"file_content", content_type="image/jpeg"
        )
        form = ProductForm({
            "name": "Test Cake",
            "tags": "Some,Tags",
            "shape": "round",
            "category": self.category.pk,
            "base_price": "199.00",
        }, files={"image_url": dummy_image})

        self.assertTrue(
            form.is_valid(),
            msg=f"Form is not valid: {form.errors}"
        )

    @patch("cloudinary.models.CloudinaryField.to_python")
    @patch("cloudinary.forms.CloudinaryFileField.to_python")
    def test_product_form_missing_required_fields_is_invalid(
            self, mock_form_field, mock_model_field):
        """
        Test missing required fields - invalid form data.
        """
        mock_form_field.return_value = "image/upload/test.jpg"
        mock_model_field.return_value = "image/upload/test.jpg"
        form = ProductForm({})

        self.assertFalse(
            form.is_valid(),
            msg="Form should be invalid with no data"
        )


class TestEditProductForm(TestCase):
    """
    Set up mock data for category instance
    """

    def setUp(self):
        self.category = Category.objects.create(
            name="birthday_cakes",
            display_name="Birthday Cakes"
        )

    def test_edit_product_form_is_valid(self):
        """
        Test all required fields to be completed - valid form data.
        EditProductForm has image_url required=False so no mock needed.
        """
        form = EditProductForm({
            "name": "Updated Cake",
            "tags": "Some,Tags",
            "shape": "square",
            "category": self.category.pk,
            "base_price": "149.00",
        })

        self.assertTrue(
            form.is_valid(),
            msg=f"Form is not valid: {form.errors}"
        )

    def test_edit_product_form_missing_required_fields_is_invalid(self):
        """
        Test missing required fields - invalid form data.
        EditProductForm has image_url required=False so no mock needed.
        """
        form = EditProductForm({})

        self.assertFalse(
            form.is_valid(),
            msg="Form should be invalid with no data"
        )
