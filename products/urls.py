from django.urls import path
from . import views

urlpatterns = [
    path('cakes/', views.CakeList.as_view(), name='cakes'),
]
