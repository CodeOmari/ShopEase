from django.db import models

# Create your models here.
class Wishlist(models.Model):
    customer = models.OneToOneField(
        "accounts.CustomerProfile",
        on_delete=models.CASCADE,
        related_name="wishlist"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Wishlist'

    def __str__(self):
        return f"{self.customer.user.first_name}'s Wishlist"

class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        "shop.Product",
        on_delete=models.CASCADE,
        related_name="wishlist_items"
    )
    added_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = 'Wishlist Items'
        constraints = [
            models.UniqueConstraint(
                fields=["wishlist", "product"],
                name="unique_product_per_wishlist"
            )
        ]

    def __str__(self):
        return f"{self.wishlist.customer.user.first_name} - {self.product.name}"