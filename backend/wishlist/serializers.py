from rest_framework import serializers
from .models import Wishlist, WishlistItem

class WishlistItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(
        source="product.name",
        read_only=True
    )

    product_price = serializers.DecimalField(
        source="product.price",
        max_digits=12,
        decimal_places=2,
        read_only=True
    )

    class Meta:
        model = WishlistItem

        fields = [
            "id",
            "wishlist",
            "product",
            "product_name",
            "product_price",
            "product_image",
            "added_at",
        ]

        read_only_fields = [
            "id",
            "wishlist",
            "added_at",
        ]


class WishlistSerializer(serializers.ModelSerializer):
    items = WishlistItemSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Wishlist

        fields = [
            "id",
            "customer",
            "items",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "customer",
            "created_at",
            "updated_at",
        ]