from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductList.as_view(), name='products'),
    path('<slug:slug>/<int:product_id>',
         views.product_details, name='product_details'),
]
