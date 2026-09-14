from django.db.models.signals import post_save
from django.dispatch import receiver
from user_management.models import CustomUser
from .models import CustomerProfile, SellerProfile, AdminProfile


@receiver(post_save, sender=CustomUser)
def create_customer_profile(sender, instance, created, **kwargs):
    if created and instance.role == "BUYER":
        CustomerProfile.objects.create(user=instance)


@receiver(post_save, sender=CustomUser)
def create_seller_profile(sender, instance, created, **kwargs):
    if created and instance.role == "SELLER":
        SellerProfile.objects.create(
            user=instance,
            business_email=instance.email
        )

@receiver(post_save, sender=CustomUser)
def create_admin_profile(sender, instance, created, **kwargs):
    if created and instance.role == "ADMIN":
        AdminProfile.objects.create(user=instance)