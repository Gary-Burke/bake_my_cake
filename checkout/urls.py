from django.urls import path
from . import views
from . import webhooks

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('complete/', views.checkout_complete, name='checkout_complete'),
    path('validate/', views.validate_order_form, name='validate'),
    path('session-status/', views.session_status, name='session_status'),
    path('update-session/', views.update_session_metadata,
         name='update_session_metadata'),
    path('webhook/', webhooks.stripe_webhook, name='stripe_webhook'),
]
