from django.urls import path
from . import views
from .views import ItemListView

urlpatterns = [
    path('', views.profile, name='profile'),
    path('orders/', ItemListView.as_view(), name='order_list')
]
