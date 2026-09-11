from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


class IsSeller(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.role != 'SELLER':
            raise PermissionDenied("Your role is BUYER. You cannot access a seller profile.")

        return True


class IsBuyer(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.role != 'BUYER':
            raise PermissionDenied("Your role is SELLER. You cannot access a customer profile.")

        return True