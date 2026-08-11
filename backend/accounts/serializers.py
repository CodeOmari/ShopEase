from .models import CustomerProfile, SellerProfile, CustomerAddress
from rest_framework import serializers

class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = '__all__'
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

class CustomerAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerAddress
        field = [
            "id",
            "label", 
            "shipping_address", 
            "street", 
            "county", 
            "postal_code", 
            "is_default", 
            "created_at", 
            "updated_at"
        ]
        read_only_fields = [
            "id",
            "created_at", 
            "updated_at",
        ]

class SellerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerProfile
        fields = '__all__'
        read_only_fields = [
                'id', 
                'user', 
                'is_verified', 
                'verification_status',
                'verified_by',
                'created_at', 
                'updated_at'
            ]