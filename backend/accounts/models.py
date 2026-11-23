from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.
class CustomerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer_profile')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    class Meta:
        db_table = "Customer Profiles"


class CustomerAddress(models.Model):
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name="customer_addresses")
    label = models.CharField(max_length=50, help_text="Example: Home, Work, Office")
    shipping_address = models.CharField(max_length=150, help_text="Example: House 15, Green Valley Apartments")
    street = models.CharField(max_length=100, help_text="Example: Ngong Road")
    county = models.CharField(max_length=100, help_text= "Example: Nairobi")
    postal_code = models.CharField(max_length=10, help_text="00100")
    is_default = models.BooleanField( default=False, help_text="Marks this as the customer's default shipping address" )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Customer Address"
        ordering = ["-is_default", "-created_at"]

    def __str__(self): 
        return f"{self.customer.user.first_name} - {self.label}"

    

class SellerProfile(models.Model):
    PENDING = 'PENDING'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'

    VERIFICATION_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='seller_profile')
    business_name = models.CharField(max_length=100)
    business_email = models.EmailField(unique=True)
    business_address = models.CharField(max_length=150, help_text="Example: Stall 24, Greenspan Mall")
    description = models.TextField()
    street = models.CharField(max_length=100, help_text="Example: Ngong Road")
    county = models.CharField(max_length=100, help_text= "Example: Nairobi")
    postal_code = models.CharField(max_length=10, help_text="00100")
    is_verified = models.BooleanField(default=False)
    verification_status = models.CharField(max_length=10, choices=VERIFICATION_CHOICES, default='PENDING')
    verified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.SET_NULL, null=True, blank=True, related_name = 'verified_sellers')
    verified_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.user.first_name} {self.business_name}'

    def save(self, *args, **kwargs):
        self.is_verified = self.verification_status == self.APPROVED
        super().save(*args, **kwargs)

    def review(self, admin_user, status):
        if status not in (self.APPROVED, self.REJECTED):
            raise ValueError("Status must be APPROVED or REJECTED.")
        self.verification_status = status
        self.verified_by = admin_user
        self.verified_at = timezone.now()
        self.save()

    @property
    def can_add_products(self):
        return self.verification_status == self.APPROVED

    @property
    def verification_message(self):
        if self.verification_status == self.PENDING:
            return ("Your seller account is pending verification. "
                    "You can add products once an admin approves it.")
        if self.verification_status == self.REJECTED:
            return ("Your seller verification was rejected, so you can't add "
                    "products. Please review your business details or contact support.")
        return ""

    class Meta:
        db_table = "Seller Profiles"


class AdminProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='admin_profile')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    class Meta:
        db_table = "Admin Profiles"