from django.urls import path
from . import views, tasks
from .applications import webhooks


app_name = 'payment'


urlpatterns = [
    path('process/', views.payment_process, name='process'),
    path('comleted/', views.payment_completed, name='completed'),
    path('canceled/', views.payment_canceled, name='canceled'),
    path('webhook/', webhooks.stripe_webhook, name='stripe-webhook'),
]
