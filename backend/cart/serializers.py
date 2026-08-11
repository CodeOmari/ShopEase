from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderItem

class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField( source="product.name", read_only=True )
    product_price = serializers.IntegerField( source="product.price", read_only=True )

    class Meta:
        model = CartItem
        fields = [
            "id", 
            "cart", 
            "product", 
            "product_name", 
            "product_price", 
            "quantity", 
            "added_at", 
            "updated_at"
        ]
        read_only_fields = [
            "id", 
            "cart", 
            "added_at", 
            "updated_at"
        ]



class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer( many=True, read_only=True )

    class Meta:
        model = Cart
        fields = [
            "id", 
            "customer", 
            "items", 
            "created_at", 
            "updated_at"
        ]
        read_only_fields = [
            "id", 
            "customer", 
            "created_at", 
            "updated_at"
        ]


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField( source="product.name", read_only=True ) 
    seller_name = serializers.CharField( source="seller.user.first_name", read_only=True )

    class Meta:
        model = OrderItem
        fields = [
            "id", 
            "order",
            "product", 
            "product_name", 
            "seller", 
            "seller_name", 
            "quantity", 
            "price", 
            "grand_total", 
            "status"
        ] 
        read_only_fields = [
            "id", 
            "order", 
            "seller", 
            "price", 
            "grand_total"
        ]

        
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer( many=True, read_only=True ) 
    class Meta:
        model = Order 
        fields = [ 
            "id", 
            "order_number", 
            "customer", 
            "total_amount", 
            "shipping_fee", 
            "items", 
            "created_at", 
            "updated_at"
        ] 
        read_only_fields = [ 
            "id", 
            "order_number", 
            "customer", 
            "total_amount", 
            "created_at", 
            "updated_at"
        ]