from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


class IsSeller(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.role != 'SELLER':
            raise PermissionDenied("You cannot access a seller profile.")

        return True


class IsBuyer(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.role != 'BUYER':
            raise PermissionDenied("You cannot access a customer profile.")

        return True


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.role != 'ADMIN':
            raise PermissionDenied("You cannot access the admin profile.")

        return True