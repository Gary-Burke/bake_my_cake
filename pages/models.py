from django.db import models
from cloudinary.models import CloudinaryField
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class CustomOrder(models.Model):
    """
    Stores a single custome order entry related to :model:`CustomOrder`.
    """
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    shape = models.CharField(max_length=255)
    size = models.CharField(max_length=255)
    tiers = models.IntegerField(
        validators=[
            MinValueValidator(1, message="Tiers must be at least 1."),
            MaxValueValidator(3, message="Tiers cannot be more than 3."),
        ])
    sponge = models.CharField(max_length=255)
    filling = models.CharField(max_length=255)
    icing = models.CharField(max_length=255)
    additional_info = models.TextField(max_length=255, null=True, blank=True)
    image_url = CloudinaryField('image upload', null=True, blank=True)
    created_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_on", "name"]

    def __str__(self):
        return str(self.pk)
