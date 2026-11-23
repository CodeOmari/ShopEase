from rest_framework import serializers

from shop.models import Product
from .models import Cart, CartItem, Notification, Order, OrderItem


class CartProductSerializer(serializers.ModelSerializer):
    """Slim product summary for the cart (no seller contact details)."""
    image = serializers.SerializerMethodField()
    seller_name = serializers.CharField(source="seller.business_name", read_only=True)

    class Meta:
        model = Product
        fields = ["id", "name", "slug", "brand", "price", "discount_price", "stock", "image", "seller_name"]

    def get_image(self, obj):
        primary = next(iter(obj.images.all()), None)   # images are ordered primary-first
        if not primary:
            return None
        request = self.context.get("request")
        return request.build_absolute_uri(primary.image.url) if request else primary.image.url


class CartItemSerializer(serializers.ModelSerializer):
    product = CartProductSerializer(read_only=True)
    unit_price = serializers.IntegerField(read_only=True)
    line_total = serializers.IntegerField(read_only=True)
    issue = serializers.CharField(read_only=True)

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "unit_price", "line_total", "issue"]


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    item_count = serializers.SerializerMethodField()
    subtotal = serializers.SerializerMethodField()
    has_issues = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["id", "items", "item_count", "subtotal", "has_issues", "updated_at"]

    def get_item_count(self, cart):
        return sum(item.quantity for item in cart.items.all())

    def get_subtotal(self, cart):
        # Only lines that can actually be bought count towards the total.
        return sum(item.line_total for item in cart.items.all() if item.issue is None)

    def get_has_issues(self, cart):
        return any(item.issue for item in cart.items.all())


class AddToCartSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.select_related("seller"))
    quantity = serializers.IntegerField(min_value=1, default=1)

    def validate_product(self, product):
        if not product.is_available or not product.seller.is_verified:
            raise serializers.ValidationError("This product is not available.")
        if product.stock == 0:
            raise serializers.ValidationError("This product is out of stock.")
        return product


class UpdateQuantitySerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)


class OrderItemSerializer(serializers.ModelSerializer):
    order_number = serializers.CharField(source="order.order_number", read_only=True)
    ordered_at = serializers.DateTimeField(source="order.created_at", read_only=True)
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_slug = serializers.CharField(source="product.slug", read_only=True)
    seller_name = serializers.CharField(source="seller.business_name", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            "id", "order", "order_number", "ordered_at",
            "product", "product_name", "product_slug",
            "seller", "seller_name",
            "quantity", "price", "grand_total",
            "status", "status_display",
        ]
        read_only_fields = fields   # status changes go through the dedicated actions


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id", "order_number", "total_amount", "shipping_fee",
            "shipping_name", "shipping_phone", "shipping_address",
            "shipping_street", "shipping_county", "shipping_postal_code",
            "items", "created_at", "updated_at",
        ]
        read_only_fields = fields


class NotificationSerializer(serializers.ModelSerializer):
    """What a seller sees: the order, only THEIR items from it, and where to deliver."""
    order_number = serializers.CharField(source="order.order_number", read_only=True)
    ordered_at = serializers.DateTimeField(source="order.created_at", read_only=True)
    items = serializers.SerializerMethodField()
    shipping = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            "id", "kind", "message", "is_read", "created_at",
            "order_number", "ordered_at", "items", "shipping",
        ]
        read_only_fields = fields

    def _seller_items(self, obj):
        cached = getattr(obj, "_seller_items_cache", None)
        if cached is None:
            cached = [i for i in obj.order.items.all() if i.seller.user_id == obj.recipient_id]
            obj._seller_items_cache = cached
        return cached

    def get_items(self, obj):
        request = self.context.get("request")
        rows = []
        for item in self._seller_items(obj):
            primary = next(iter(item.product.images.all()), None)
            image = None
            if primary:
                image = request.build_absolute_uri(primary.image.url) if request else primary.image.url
            rows.append({
                "id": item.id,
                "product_name": item.product.name,
                "product_slug": item.product.slug,
                "image": image,
                "quantity": item.quantity,
                "price": item.price,
                "grand_total": item.grand_total,
                "status": item.status,
                "status_display": item.get_status_display(),
            })
        return rows

    def get_shipping(self, obj):
        order = obj.order
        return {
            "name": order.shipping_name,
            "phone": order.shipping_phone,
            "address": order.shipping_address,
            "street": order.shipping_street,
            "county": order.shipping_county,
            "postal_code": order.shipping_postal_code,
        }