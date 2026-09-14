from django.urls import path, include

from rest_framework.routers import DefaultRouter
from .views import CustomerProfileViewSet, SellerProfileViewSet, AdminProfileViewSet

router = DefaultRouter()
router.register(r'customer-profile', CustomerProfileViewSet)
router.register(r'seller-profile', SellerProfileViewSet)
router.register(r'admin-profile', AdminProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]