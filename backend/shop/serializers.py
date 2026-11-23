from rest_framework import serializers
from .models import Category, Product, ProductImage, Review, Announcement
from accounts.serializers import SellerProfileSerializer

from django.db import transaction
from django.utils import timezone

class CategorySerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source="get_category_display", read_only=True)

    class Meta:
        model = Category
        fields =  ["id", "category", "category_display", "slug", "description"]
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

        if not ProductImage.objects.filter(product=product).exists():
            validated_data["is_primary"] = True

        elif is_primary:
            ProductImage.objects.filter(
                product=product
            ).update(is_primary=False)

        return super().create(validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):
        is_primary = validated_data.get("is_primary", instance.is_primary)

        if is_primary:
            ProductImage.objects.filter(product=instance.product).exclude(pk=instance.pk).update(is_primary=False)

        return super().update(instance, validated_data)


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category', write_only=True)

    images = ProductImageSerializer(many=True, read_only=True)
    seller = SellerProfileSerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'seller',
            'category',
            'category_id',
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

    def validate(self, data):
        price = data.get("price", getattr(self.instance, "price", None))
        discount = data.get("discount_price", getattr(self.instance, "discount_price", 0))
        if discount and price is not None and discount >= price:
            raise serializers.ValidationError(
                {"discount_price": "The discounted price must be lower than the price."}
            )
        return data


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

class AnnouncementSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    is_live = serializers.BooleanField(read_only=True)

    class Meta:
        model = Announcement
        fields = [
            "id", "title", "message", "product", "product_name",
            "discount_percent", "ends_at", "is_active", "is_live", "created_at",
        ]
        read_only_fields = ["id", "is_active", "created_at"]

    def get_product_name(self, obj):
        return obj.product.name if obj.product else None

    def validate_ends_at(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError("The end date must be in the future.")
        return value

    def validate(self, data):
        seller = self.context["request"].user.seller_profile
        product = data.get("product")
        percent = data.get("discount_percent")

        if product and product.seller_id != seller.id:
            raise serializers.ValidationError({"product": "You can only run offers on your own products."})
        if product and not percent:
            raise serializers.ValidationError({"discount_percent": "Enter a discount for the selected product."})
        if percent and not product:
            raise serializers.ValidationError({"product": "Select the product this discount applies to."})
        if product and Announcement.objects.filter(
            product=product, is_active=True, ends_at__gt=timezone.now(), discount_percent__isnull=False
        ).exists():
            raise serializers.ValidationError({"product": "This product already has a live offer. Delete it first."})
        return data