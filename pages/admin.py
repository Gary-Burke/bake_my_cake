from django.contrib import admin
from .models import CustomOrder


@admin.register(CustomOrder)
class CustomOrderAdmin(admin.ModelAdmin):

    list_display = ("pk", "name", "created_on")
    search_fields = ("name", "pk")
    list_filter = ("name", )


# Register your models here.
