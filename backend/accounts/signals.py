from django.db.models.signals import post_save
from django.dispatch import receiver
from user_management.models import CustomUser
from .models import CustomerProfile, SellerProfile


@receiver(post_save, sender=CustomUser)
def create_customer_profile(sender, instance, created, **kwargs):
    if created:
        CustomerProfile.objects.create(user=instance)


@receiver(post_save, sender=CustomUser)
def create_seller_profile(sender, instance, created, **kwargs):
    if created:
        SellerProfile.objects.create(user=instance)