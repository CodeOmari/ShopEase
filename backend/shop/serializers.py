from rest_framework import serializers
from .models import Category, Product, ProductImage, Review

from django.db import transaction

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = [
            'id',
            'slug',
            'created_at',
            'updated_at'
        ]

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'
        read_only_fields = [
            'id',
            'created_at',
            'updated_at'
        ]

    
    @transaction.atomic
    def create(self, validated_data):
        product = validated_data["product"]
        is_primary = validated_data.get("is_primary", False)

        # Make the first uploaded image the primary image
        if not ProductImage.objects.filter(product=product).exists():
            validated_data["is_primary"] = True

        # If this image is selected as primary,
        # remove primary status from the others
        elif is_primary:
            ProductImage.objects.filter(
                product=product
            ).update(is_primary=False)

        return super().create(validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):
        is_primary = validated_data.get(
            "is_primary",
            instance.is_primary
        )

        if is_primary:
            ProductImage.objects.filter(
                product=instance.product
            ).exclude(
                pk=instance.pk
            ).update(is_primary=False)

        return super().update(instance, validated_data)


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'seller',
            'category',
            'name',
            'brand',
            'slug',
            'description',
            'price',
            'discount_price',
            'stock',
            'is_available',
            'images',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'id',
            'seller',
            'slug',
            'created_at',
            'updated_at'
        ]


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = [
            'id',
            'customer',
            'created_at',
            'updated_at'
        ]