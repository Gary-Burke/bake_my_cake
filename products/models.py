from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.


class Category(models.Model):
    """
    Stores a single entry of a category for products
    """
    CATEGORY = (
        ("cake", "Cake"),
        ("cupcake", "Cupcake"),
    )

    name = models.CharField(choices=CATEGORY, default="cake")

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


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
    shape = models.CharField(choices=SHAPE, default="round")
    base_price = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(null=True, blank=True)
    image_url = CloudinaryField('image')
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["category", "name"]

    def __str__(self):
        return self.name
