from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSeller(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.role == "SELLER")

class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.role == "BUYER")

class IsProductOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True

        return obj.seller.user == request.user


# Sellers can only perform CRUD operations on their own products images
class IsProductImageOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True

        return obj.product.seller.user == request.user


# Customer can only edit or delete their own reviews
class IsReviewOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True

        return obj.customer.user == request.user


class IsSellerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return (
            request.user.is_authenticated and request.user.role == "SELLER")

class IsCustomerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return (request.user.is_authenticated and request.user.role == "BUYER")
    
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (
                request.user.is_superuser
                or request.user.role == "ADMIN"
            )
        )

# Only approved sellers can create products or product images.
class CanAddProducts(BasePermission):
    def has_permission(self, request, view):
        if request.method != "POST":
            return True
        profile = getattr(request.user, "seller_profile", None)
        if profile is None:
            return False
        if not profile.can_add_products:
            self.message = profile.verification_message
            return False
        return True