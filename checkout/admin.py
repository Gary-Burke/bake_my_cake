from django.contrib import admin
from .models import DeliveryDate, Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = ("order_number", "name_surname",
                    "grand_total", "created_on", "delivery_date",)
    search_fields = ("order_number", "name_surname",)
    list_filter = ("name_surname", "delivery_date",)


# Register your models here.
admin.site.register(DeliveryDate)
