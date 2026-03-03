from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.


class Category(models.Model):
    """
    Stores a single entry of a category for products
    """
    name = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.display_name


class Product(models.Model):
    """
    Stores a single product entry related to :model:`Category`.
    """
    SHAPE = (
        ("round", "Round"),
        ("square", "Square"),
        ("rectangle", "Rectangle"),
    )

    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.SET_NULL
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    shape = models.CharField(choices=SHAPE, default="round", max_length=20)
    base_price = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.CharField(max_length=255, null=True, blank=True)
    image_url = CloudinaryField('image upload')
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["category", "name"]

    def __str__(self):
        return self.name
