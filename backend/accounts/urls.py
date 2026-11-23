from django.urls import path, include

from rest_framework.routers import DefaultRouter
from .views import CustomerProfileViewSet, SellerProfileViewSet, AdminProfileViewSet, SellerVerificationViewSet, CustomerAddressViewSet

router = DefaultRouter()
router.register(r'customer-profile', CustomerProfileViewSet)
router.register(r'seller-profile', SellerProfileViewSet)
router.register(r'admin-profile', AdminProfileViewSet)
router.register(r'seller-verifications', SellerVerificationViewSet, basename='seller-verification')
router.register(r'customer-addresses', CustomerAddressViewSet, basename='customer-address')

urlpatterns = [
    path('', include(router.urls)),
]