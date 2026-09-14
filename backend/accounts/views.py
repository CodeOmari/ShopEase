from django.shortcuts import render
from .serializers import CustomerProfileSerializer, SellerProfileSerializer, AdminProfileSerializer
from .models import CustomerProfile, SellerProfile, AdminProfile
from .permissions import IsBuyer, IsSeller, IsAdmin

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class CustomerProfileViewSet(viewsets.ModelViewSet):
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerProfileSerializer
    permission_classes = [IsAuthenticated, IsBuyer]

    def get_queryset(self):
        return CustomerProfile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SellerProfileViewSet(viewsets.ModelViewSet):
    queryset = SellerProfile.objects.all()
    serializer_class = SellerProfileSerializer
    permission_classes = [IsAuthenticated, IsSeller]

    def get_queryset(self):
        return SellerProfile.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AdminProfileViewSet(viewsets.ModelViewSet):
    queryset = AdminProfile.objects.all()
    serializer_class = AdminProfileSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    
    def get_queryset(self):
        return AdminProfile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)