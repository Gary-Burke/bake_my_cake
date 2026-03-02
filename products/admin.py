from django.contrib import admin
from .models import Category, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = ("category", "name", "base_price", "updated_on")
    search_fields = ("name", "shape")
    list_filter = ("category", "shape")


# Register your models here.
admin.site.register(Category)
