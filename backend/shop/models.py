from django.db import models
from django.utils.text import slugify

import os
import uuid

from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
def generate_unique_name(instance, filename):
    name = uuid.uuid4()
    full_file_name = f'{name}-{filename}'
    return os.path.join("product_images", full_file_name)

class Category(models.Model):
    CATEGORY_CHOICES = [
        ("ELECTRONICS", "Electronics"),
        ("FASHION", "Fashion"),
        ("APPLIANCES", "Appliances"),
        ("HOME & OFFICE", "Home & Office"),
        ("HEALTH & BEAUTY", "Health & Beauty"),
        ("SPORTS", "Sports"),
        ("BOOKS", "Books"),
        ("TOYS", "Toys"),
        ("AUTOMOTIVE", "Automotive"),
        ("GROCERIES", "Groceries"),
        ("GAMING", "Gaming"),
        ("COMPUTING", "Computing"),
        ("PHONES & TABLETS", "Phones & Tablets"),
        ("BABY PRODUCTS", "Baby Products"),
    ]
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.get_category_display())

        super().save(*args, **kwargs)

    def __str__(self):
        return self.get_category_display()

    class Meta:
        db_table = "Category"


class Product(models.Model):
    seller = models.ForeignKey('accounts.SellerProfile', on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    name = models.CharField(max_length=250, help_text="Enter the product name")
    brand = models.CharField(max_length=100, blank=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(help_text="Provide a detailed description of the product")
    price = models.PositiveIntegerField()
    discount_price = models.PositiveIntegerField(default=0, help_text="Enter the discount amount")
    stock = models.PositiveIntegerField(default=0, help_text='Enter the number of items available')
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Products"
        ordering =["-created_at"]


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} {self.brand}'   


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=generate_unique_name)
    is_primary = models.BooleanField(default=False, help_text="Determines if the image uploaded is the main image to be displayed for the product")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Product Images"
        ordering = ['-is_primary', 'id']

    def __str__(self):
        return f'{self.product.name} Image'


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    customer = models.ForeignKey("accounts.CustomerProfile", on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ],
        help_text="Rate this product from 1 to 5 stars"
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Product Reviews"
        ordering = ["-created_at"]

        constraints = [
            models.UniqueConstraint(
                fields=["product", "customer"],
                name="unique_product_review"
            )
        ]


    def __str__(self):
        return f'{self.customer.user.name} - {self.product.name}'