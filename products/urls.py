from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductList.as_view(), name='products'),
    path('admin-edit/', views.ProductListAdmin.as_view(),
         name='products_admin'),
    path('<slug:slug>/<int:product_id>/',
         views.product_details, name='product_details'),
    path('add/', views.add_product, name='add_product'),
    path('edit/<int:product_id>', views.edit_product, name='edit_product')
]
