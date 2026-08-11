from django.db import models

# Create your models here.
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
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Cart Item"
        constraints = [
            models.UniqueConstraint(
                fields=["cart", "product"],
                name="unique_product_per_cart"
            )
        ]

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"


class Order(models.Model):
    customer = models.ForeignKey(
        "accounts.CustomerProfile",
        on_delete=models.PROTECT,
        related_name='orders'
    )
    order_number = models.CharField(max_length=30, unique=True)
    total_amount = models.PositiveIntegerField()
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