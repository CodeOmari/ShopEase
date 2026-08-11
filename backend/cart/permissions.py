from rest_framework.permissions import BasePermission

class IsCustomer(BasePermission):
    def has_permission(self, request, view): 
        return ( 
            request.user.is_authenticated and hasattr(request.user, "customer_profile") 
        )

class IsSeller(BasePermission):
    def has_permission(self, request, view): 
        return ( 
            request.user.is_authenticated and hasattr(request.user, "seller_profile") 
        )

class IsCustomerOrSeller(BasePermission):
    def has_permission(self, request, view): 
        return ( 
            request.user.is_authenticated 
            and ( 
                hasattr(request.user, "customer_profile") 
                or hasattr(request.user, "seller_profile") 
            ) 
        )