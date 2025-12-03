from django.urls import path
from .views import create_checkout_session, sucesso, cancelado, stripe_webhook

urlpatterns = [
    path("create-checkout-session/", create_checkout_session, name="create_checkout_session"),
    path("sucesso/", sucesso, name="sucesso"),
    path("cancelado/", cancelado, name="cancelado"),
    path("webhook/", stripe_webhook, name="stripe-webhook"),
]
