from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CartItemViewSet, CartViewSet, NotificationViewSet, OrderItemViewSet, OrderViewSet,
)

router = DefaultRouter()
router.register(r'shopping-cart', CartViewSet, basename='shopping-cart')
router.register(r'cart-items', CartItemViewSet, basename='cart-item')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'order-items', OrderItemViewSet, basename='order-item')
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    path('', include(router.urls))
]
