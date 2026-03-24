import uuid

from django.db import models
from django_countries.fields import CountryField
from profiles.models import UserProfile

# Create your models here.


class DeliveryDate(models.Model):
    """
    Stores an instance for the delivery date of an order
    """
    date = models.DateField()


class Order(models.Model):
    """
    Stores an instance of an order placed by the user
    """
    date = models.OneToOneField(DeliveryDate, on_delete=models.CASCADE)
    order_number = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    user_profile = models.ForeignKey(
        UserProfile, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='orders')
    name_surname = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    street_address1 = models.CharField(max_length=80, null=True, blank=True)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=True, blank=True)
    state = models.CharField(max_length=80, null=True, blank=True)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    country = CountryField(blank_label='Country', null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    grand_total = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    original_basket = models.TextField(default='')
    stripe_pid = models.CharField(
        max_length=254, default='')

    def __str__(self):
        return self.order_number
