from django.contrib import admin
from django.utils import timezone
from .models import CustomerProfile, CustomerAddress, SellerProfile


class CustomerAddressInline(admin.TabularInline):
    model = CustomerAddress
    extra = 0
    fields = ("label", "shipping_address", "street", "county", "postal_code", "is_default")

@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "phone_number", "address_count", "created_at")
    search_fields = ("user__first_name", "user__last_name", "user__email", "user__phone_number",)
    list_filter = ("created_at",)
    readonly_fields = ("created_at", "updated_at")
    list_select_related = ("user",)
    inlines = [CustomerAddressInline]

    @admin.display(description="Name", ordering="user__first_name")
    def full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    @admin.display(description="Email", ordering="user__email")
    def email(self, obj):
        return obj.user.email

    @admin.display(description="Phone")
    def phone_number(self, obj):
        return obj.user.phone_number

    @admin.display(description="Addresses")
    def address_count(self, obj):
        return obj.customer_addresses.count()

@admin.register(CustomerAddress)
class CustomerAddressAdmin(admin.ModelAdmin):
    list_display = ("customer", "label", "street", "county", "postal_code", "is_default")
    list_filter = ("county", "is_default")
    search_fields = ("customer__user__email", "label", "street", "county")


@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ("business_name", "owner", "business_email", "county", "verification_status", "is_verified", "created_at",)
    list_filter = ("verification_status", "is_verified", "county", "created_at")
    search_fields = ("business_name", "business_email", "user__first_name", "user__last_name", "user__email",)
    readonly_fields = ("verified_by", "verified_at", "created_at", "updated_at")
    list_select_related = ("user",)
    actions = ["approve_sellers", "reject_sellers"]

    fieldsets = (
        ("Owner", {"fields": ("user",)}),
        ("Business details", {
            "fields": ("business_name", "business_email", "description"),
        }),
        ("Location", {
            "fields": ("business_address", "street", "county", "postal_code"),
        }),
        ("Verification", {
            "fields": ("verification_status", "is_verified", "verified_by", "verified_at"),
        }),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )
    
    readonly_fields = ("is_verified", "verified_by", "verified_at", "created_at", "updated_at")

    def save_model(self, request, obj, form, change):
        if change and "verification_status" in form.changed_data:
            if obj.verification_status in (SellerProfile.APPROVED, SellerProfile.REJECTED):
                obj.verified_by = request.user
                obj.verified_at = timezone.now()
            else:  # moved back to pending
                obj.verified_by = None
                obj.verified_at = None
        super().save_model(request, obj, form, change)

    @admin.action(description="Approve selected sellers")
    def approve_sellers(self, request, queryset):
        for seller in queryset:
            seller.review(request.user, SellerProfile.APPROVED)
        self.message_user(request, f"{queryset.count()} seller(s) approved.")

    @admin.action(description="Reject selected sellers")
    def reject_sellers(self, request, queryset):
        for seller in queryset:
            seller.review(request.user, SellerProfile.REJECTED)
        self.message_user(request, f"{queryset.count()} seller(s) rejected.")

    @admin.display(description="Owner", ordering="user__first_name")
    def owner(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    @admin.action(description="Approve selected sellers")
    def approve_sellers(self, request, queryset):
        updated = queryset.update(verification_status="APPROVED", is_verified=True, verified_by=request.user, verified_at=timezone.now(),)
        self.message_user(request, f"{updated} seller(s) approved.")

    @admin.action(description="Reject selected sellers")
    def reject_sellers(self, request, queryset):
        updated = queryset.update(verification_status="REJEECTED", is_verified=False, verified_by=request.user, verified_at=timezone.now(),)
        self.message_user(request, f"{updated} seller(s) rejected.")