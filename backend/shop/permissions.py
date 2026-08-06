from rest_framework.permissions import BasePermission

# Ensure CRUD operations for sellers on products and product images
class IsSeller(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == "SELLER"
        )

# Only customers can create reviews
class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == "BUYER"
        )

# Sellers can only perform CRUD operations on their own products
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


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.is_staff
        )