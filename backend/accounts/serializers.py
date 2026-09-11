from .models import CustomerProfile, SellerProfile, CustomerAddress
from rest_framework import serializers

class CustomerProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    phone_number = serializers.CharField(source='user.phone_number', read_only=True)
    role = serializers.CharField(source='user.role', read_only=True)
    profile_pic = serializers.ImageField(
        source='user.profile_pic',
        read_only=True
    )
    class Meta:
        model = CustomerProfile
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'profile_pic',
            'role',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

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
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    phone_number = serializers.CharField(source='user.phone_number', read_only=True)
    role = serializers.CharField(source='user.role', read_only=True)
    profile_pic = serializers.ImageField(
        source='user.profile_pic',
        read_only=True
    )
    class Meta:
        model = SellerProfile
        fields = [
            "id",
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'profile_pic',
            'role', 
            'business_name',
            'business_email',
            'business_address',
            'phone_number',
            'description',
            'street',
            'county',
            'postal_code',
            'is_verified', 
            'verification_status',
            'verified_by',
            "created_at", 
            "updated_at"
        ]
        read_only_fields = [
                'id', 
                'is_verified', 
                'verification_status',
                'verified_by',
                'created_at', 
                'updated_at'
            ]