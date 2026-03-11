from django.contrib import admin
from .models import Category, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = ("name", "category", "base_price", "updated_on")
    search_fields = ("name", "shape")
    list_filter = ("category", "shape")
    prepopulated_fields = {'slug': ('name',)}


# Register your models here.
admin.site.register(Category)
