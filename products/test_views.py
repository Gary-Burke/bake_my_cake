from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch
from .forms import ProductForm, EditProductForm
from .models import Category, Product


# Create your tests here.

class TestProductsViews(TestCase):
    """
    Set up mock data for superuser, category and product instance
    """

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

    def test_render_products_page(self):
        """
        Test GET request renders the products page with the products
        """
        response = self.client.get(reverse("products"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/products.html")
        # Test if view passes the product through in context
        self.assertIn(self.product, response.context["products_list"])
        # Test if template actually renders the product name
        self.assertContains(response, "Test Cake")

    def test_render_product_details_page(self):
        """
        Test GET request renders the product details page with the details
        """
        response = self.client.get(
            reverse(
                "product_details", args=[self.product.slug, self.product.pk]
            ))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/product_details.html")
        # Test if view passes the product through in context
        self.assertEqual(response.context["product"], self.product)
        # Test if template actually renders the product name
        self.assertContains(response, "Test Cake")

    def test_render_add_product_page_with_add_product_form(self):
        """
        Test GET request renders the add product page with an empty form.
        """
        self.client.login(username="myUsername", password="myPassword")
        response = self.client.get(reverse("add_product"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/add_product.html")
        self.assertIsInstance(
            response.context["product_form"], ProductForm
        )

    # Code related to Cloudinary fields incl. patch decorators from Claude.ai
    # Need to patch model and form fields to test mock data with Cloudinary.
    @patch("cloudinary.models.CloudinaryField.to_python")
    @patch("cloudinary.forms.CloudinaryFileField.to_python")
    def test_successfull_add_product_submission(
            self, mock_form_field, mock_model_field):
        """
        Test POST request with valid form data.
        Saves an instance of product.
        Displays Django message.
        """
        self.client.login(username="myUsername", password="myPassword")
        mock_form_field.return_value = "image/upload/test.jpg"
        mock_model_field.return_value = "image/upload/test.jpg"
        dummy_image = SimpleUploadedFile(
            "test.jpg", b"file_content", content_type="image/jpeg"
        )

        product_data = {
            "name": "Add Cake",
            "tags": "Some,Tags",
            "shape": "round",
            "category": self.category.pk,
            "base_price": "99.00",
        }

        response = self.client.post(
            reverse("add_product"),
            product_data, files={"image_url": dummy_image}
        )
        self.assertEqual(response.status_code, 200)

        # setUp(self) already created 1 instance of Product so count must be 2
        self.assertEqual(Product.objects.count(), 2)
        messages = list(response.context["messages"])
        self.assertEqual(len(messages), 1)
        self.assertIn(
            "Add Cake was successfully added to the database!",
            str(messages[0]))

    def test_invalid_add_product_submission(self):
        """
        Test POST request with invalid form data.
        Does not save an instance of product.
        Does not display Django message.
        """
        self.client.login(username="myUsername", password="myPassword")
        product_data = {}
        response = self.client.post(reverse("add_product"), product_data)
        self.assertEqual(response.status_code, 200)

        # setUp(self) already created 1 instance of Product so count must be 1
        self.assertEqual(Product.objects.count(), 1)
        self.assertTrue(response.context["product_form"].errors)

    def test_render_edit_product_page_with_edit_product_form(self):
        """
        Test GET request renders the edit product page with an empty form.
        """
        self.client.login(username="myUsername", password="myPassword")
        response = self.client.get(
            reverse(
                "edit_product", args=[self.product.pk]
            ))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/edit_product.html")
        self.assertIsInstance(
            response.context["edit_product_form"], EditProductForm
        )

    # Code related to Cloudinary fields incl. patch decorators from Claude.ai
    # Need to patch model and form fields to test mock data with Cloudinary.
    @patch("cloudinary.models.CloudinaryField.to_python")
    @patch("cloudinary.forms.CloudinaryFileField.to_python")
    def test_successfull_edit_product_submission(
            self, mock_form_field, mock_model_field):
        """
        Test POST request with valid form data.
        Saves an updated instance of product.
        Displays Django message.
        """
        self.client.login(username="myUsername", password="myPassword")
        mock_form_field.return_value = "image/upload/test.jpg"
        mock_model_field.return_value = "image/upload/test.jpg"
        dummy_image = SimpleUploadedFile(
            "test.jpg", b"file_content", content_type="image/jpeg"
        )

        product_data = {
            "name": "Change Cake",
            "tags": "Some,Tags",
            "shape": "round",
            "category": self.category.pk,
            "base_price": "99.00",
        }

        response = self.client.post(
            reverse("edit_product", args=[self.product.pk]),
            product_data, files={"image_url": dummy_image},
            follow=True  # Follows redirect so context is available
        )

        # Assert redirect target as per view
        self.assertRedirects(response, reverse("products_admin"))

        # setUp(self) already created 1 instance of Product so count must be 1
        self.assertEqual(Product.objects.count(), 1)

        messages = list(response.context["messages"])
        self.assertEqual(len(messages), 1)
        self.assertIn(
            "Change Cake successfully updated!",
            str(messages[0]))

        # Test if the product was actually updated in the DB
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, "Change Cake")

    def test_invalid_edit_product_submission(self):
        """
        Test POST request with invalid form data.
        Does not save an updated instance of product.
        Does not display Django message.
        """
        self.client.login(username="myUsername", password="myPassword")
        product_data = {}
        response = self.client.post(
            reverse("edit_product", args=[self.product.pk]), product_data
        )
        self.assertEqual(response.status_code, 200)

        # setUp(self) already created 1 instance of Product so count must be 1
        self.assertEqual(Product.objects.count(), 1)
        self.assertTrue(response.context["edit_product_form"].errors)

    def test_delete_product_submission(self):
        """
        Test POST request to delete an instance of product
        """
        self.client.login(username="myUsername", password="myPassword")
        response = self.client.post(
            reverse("delete_product", args=[self.product.pk]), follow=True
        )

        messages = list(response.context["messages"])
        self.assertEqual(len(messages), 1)
        self.assertIn(
            "Test Cake was successfully deleted from the database.",
            str(messages[0]))

        self.assertRedirects(response, reverse("products_admin"))
        self.assertEqual(Product.objects.count(), 0)
