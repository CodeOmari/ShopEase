from django.db import models
from django.contrib.auth.models import AbstractUser

import os
import uuid

# Create your models here.

def generate_unique_name(instance, filename):
    name = uuid.uuid4()
    full_file_name = f'{name}-{filename}'
    return os.path.join("profile_pictures", full_file_name)

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('BUYER', 'Buyer'),
        ('SELLER', 'Seller'),
    ]
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=10, help_text="0712345678")
    profile_pic = models.ImageField(upload_to=generate_unique_name, null=True, blank=True, default='profile_pictures/default-user.svg')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='BUYER')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'