from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings

# Create your models here.
def current_price(product):
    if 0 < product.discount_price < product.price:
        return product.discount_price
    return product.price

class Cart(models.Model):
    customer = models.OneToOneField(
        "accounts.CustomerProfile",
        on_delete= models.CASCADE, 
        related_name= 'cart'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Cart"

    def __str__(self):
        return f"{self.customer.user.first_name}'s Cart"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        "shop.Product",
        on_delete=models.CASCADE,
        related_name="cart_items"
    )
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Cart Item"
        ordering = ["-added_at"]
        constraints = [
            models.UniqueConstraint(fields=["cart", "product"], name="unique_product_per_cart")
        ]

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

    @property
    def unit_price(self):
        return current_price(self.product)

    @property
    def line_total(self):
        return self.unit_price * self.quantity

    @property
    def issue(self):
        p = self.product
        if not p.is_available or not p.seller.is_verified:
            return "This product is no longer available."
        if p.stock == 0:
            return "Out of stock."
        if self.quantity > p.stock:
            return f"Only {p.stock} left in stock."
        return None


class Order(models.Model):
    customer = models.ForeignKey(
        "accounts.CustomerProfile",
        on_delete=models.PROTECT,
        related_name='orders'
    )
    order_number = models.CharField(max_length=30, unique=True)
    total_amount = models.PositiveIntegerField()
    shipping_name = models.CharField(max_length=100, blank=True, default="")
    shipping_phone = models.CharField(max_length=20, blank=True, default="")
    shipping_address = models.CharField(max_length=150, blank=True, default="")
    shipping_street = models.CharField(max_length=100, blank=True, default="")
    shipping_county = models.CharField(max_length=100, blank=True, default="")
    shipping_postal_code = models.CharField(max_length=10, blank=True, default="")
    shipping_fee = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Order'

    def __str__(self):
        return f"{self.customer.user.first_name} - {self.order_number}"


class OrderItem(models.Model):
    ITEM_STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("PROCESSING", "Processing"),
        ("SHIPPED", "Shipped"),
        ("DELIVERED", "Delivered"),
        ("CANCELLED", "Cancelled"),
    ]
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        "shop.Product",
        on_delete=models.PROTECT,
        related_name="order_item"
    )
    seller = models.ForeignKey(
        "accounts.SellerProfile",
        on_delete=models.PROTECT,
        related_name='seller'
    )
    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField()
    grand_total = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20,
        choices=ITEM_STATUS_CHOICES,
        default="PENDING"
    )

    class Meta:
        db_table = "Order Item"

    def save(self, *args, **kwargs):
        self.grand_total = self.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"


class Notification(models.Model):
    NEW_ORDER = "NEW_ORDER"
    KIND_CHOICES = [(NEW_ORDER, "New order")]

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications"
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="notifications")
    kind = models.CharField(max_length=20, choices=KIND_CHOICES, default=NEW_ORDER)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Notification"
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["recipient", "is_read"])]

    def __str__(self):
        return f"{self.recipient} - {self.message}"