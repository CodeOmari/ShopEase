from django.urls import path, include

from rest_framework.routers import DefaultRouter
from .views import CustomerProfileViewSet, SellerProfileViewSet

router = DefaultRouter()
router.register(r'customer-profile', CustomerProfileViewSet)
router.register(r'seller-profile', SellerProfileViewSet)


urlpatterns = [
    path('', include(router.urls)),
]