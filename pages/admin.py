from django.contrib import admin
from .models import CustomOrder


@admin.register(CustomOrder)
class CustomOrderAdmin(admin.ModelAdmin):

    list_display = ("pk", "name", "created_on", "read")
    search_fields = ("name", "pk")
    list_filter = ("read", "name")


# Register your models here.
