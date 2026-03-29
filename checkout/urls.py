from django.urls import path
from . import views

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('complete/', views.checkout_complete,  name='checkout_complete'),
    path('session-status/', views.session_status, name='session_status'),
    path('validate/', views.validate_order_form, name='validate')
]
