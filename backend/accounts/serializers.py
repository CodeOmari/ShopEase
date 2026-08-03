from .models import CustomerProfile, SellerProfile
from rest_framework import serializers

class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = '__all__'
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


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