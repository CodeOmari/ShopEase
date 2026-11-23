from django.shortcuts import render
from .serializers import CustomerProfileSerializer, SellerProfileSerializer, AdminProfileSerializer, CustomerAddressSerializer 
from .models import CustomerProfile, SellerProfile, AdminProfile, CustomerAddress
from .permissions import IsBuyer, IsSeller, IsAdmin

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from rest_framework.decorators import action
from rest_framework.response import Response

from django.db import transaction

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

class SellerVerificationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SellerProfileSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_queryset(self):
        qs = SellerProfile.objects.select_related('user', 'verified_by')
        status = self.request.query_params.get('status')
        return qs.filter(verification_status=status.upper()) if status else qs

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        seller = self.get_object()
        seller.review(request.user, SellerProfile.APPROVED)
        return Response(self.get_serializer(seller).data)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        seller = self.get_object()
        seller.review(request.user, SellerProfile.REJECTED)
        return Response(self.get_serializer(seller).data)
    

class AdminProfileViewSet(viewsets.ModelViewSet):
    queryset = AdminProfile.objects.all()
    serializer_class = AdminProfileSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_queryset(self):
        return AdminProfile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CustomerAddressViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerAddressSerializer
    permission_classes = [IsAuthenticated, IsBuyer]

    def get_queryset(self):
        return CustomerAddress.objects.filter(customer__user=self.request.user)

    @transaction.atomic
    def perform_create(self, serializer):
        customer, _ = CustomerProfile.objects.get_or_create(user=self.request.user)
        has_default = CustomerAddress.objects.filter(customer=customer, is_default=True).exists()
        is_default = serializer.validated_data.get("is_default", False) or not has_default
        if is_default:
            CustomerAddress.objects.filter(customer=customer).update(is_default=False)
        serializer.save(customer=customer, is_default=is_default)

    @transaction.atomic
    def perform_update(self, serializer):
        if serializer.validated_data.get("is_default"):
            CustomerAddress.objects.filter(customer=serializer.instance.customer).exclude(
                pk=serializer.instance.pk
            ).update(is_default=False)
        serializer.save()

    @transaction.atomic
    def perform_destroy(self, instance):
        customer, was_default = instance.customer, instance.is_default
        instance.delete()
        if was_default:
            replacement = CustomerAddress.objects.filter(customer=customer).first()
            if replacement:
                replacement.is_default = True
                replacement.save(update_fields=["is_default", "updated_at"])