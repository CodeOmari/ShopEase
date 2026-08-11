from django.shortcuts import render
import uuid 
from django.db import transaction
from .serializers import CartSerializer, CartItemSerializer, OrderItemSerializer, OrderSerializer
from .models import Cart, CartItem, OrderItem, Order
from .permissions import IsCustomer, IsSeller, IsCustomerOrSeller

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
# Create your views here.

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated, IsCustomer]

    def get_queryset(self):
        return Cart.objects.filter(
            customer=self.request.user.customer_profile
        )

    def perform_create(self, serializer):
        customer = self.request.user.customer_profile

        # Prevent a customer from creating multiple carts
        if Cart.objects.filter(customer=customer).exists():
            raise PermissionDenied("You already have a cart.")

        serializer.save(customer=customer)


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated, IsCustomer]

    def get_queryset(self):
        return CartItem.objects.filter(
            cart__customer=self.request.user.customer_profile
        )

    def perform_create(self, serializer): 
        customer = self.request.user.customer_profile

        # Get the customer's cart 
        cart, created = Cart.objects.get_or_create( customer=customer ) 
        product = serializer.validated_data["product"] 
        quantity = serializer.validated_data["quantity"] 

        # Check if the product already exists in the cart 
        cart_item = CartItem.objects.filter( cart=cart, product=product ).first() 
        if cart_item: 
            cart_item.quantity += quantity 
            cart_item.save() 
        else: 
            serializer.save(cart=cart) 

    def perform_update(self, serializer): 
        cart_item = self.get_object() 
        if cart_item.cart.customer != self.request.user.customer_profile: 
            raise PermissionDenied( "You cannot modify this cart item." ) 
        serializer.save()


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsCustomer]


    def get_queryset(self):
        return Order.objects.filter(
            customer=self.request.user.customer_profile
        )

    def create(self, request, *args, **kwargs): 
        return Response( 
            { 
                "detail": "Orders can only be created through checkout." 
            }, 
            status=status.HTTP_405_METHOD_NOT_ALLOWED 
        )

    def update(self, request, *args, **kwargs): 
        return Response( 
            { 
                "detail": "Orders cannot be modified directly." 
            }, 
            status=status.HTTP_405_METHOD_NOT_ALLOWED 
        )

    def partial_update(self, request, *args, **kwargs): 
        return Response( 
            { 
                "detail": "Orders cannot be modified directly." 
            }, 
            status=status.HTTP_405_METHOD_NOT_ALLOWED 
        ) 
    
    @action( 
        detail=False, 
        methods=["post"], 
        url_path="checkout" 
    )

    @transaction.atomic 
    def checkout(self, request): 
        customer = request.user.customer_profile 
    
        # Get the customer's cart 
        try: 
                cart = Cart.objects.get( customer=customer ) 
        except Cart.DoesNotExist: 
            return Response( 
                {
                    "detail": "Cart does not exist."
                }, 
                status=status.HTTP_400_BAD_REQUEST 
            ) 
        
        # Get cart items 
        cart_items = cart.items.select_related( "product", "product__seller" ) 
        if not cart_items.exists(): 
            return Response( 
                {
                    "detail": "Your cart is empty."
                }, status=status.HTTP_400_BAD_REQUEST 
            ) 
        
        total_amount = 0 

        # Create a unique order number 
        order_number = f"ORD-{uuid.uuid4().hex[:10].upper()}" 

        # For now shipping fee is zero. 
        shipping_fee = 0 

        # Create the order 
        order = Order.objects.create( customer=customer, order_number=order_number, total_amount=0, shipping_fee=shipping_fee ) 

        # Create OrderItems 
        for cart_item in cart_items: 
            product = cart_item.product 
            price = product.price 
            grand_total = price * cart_item.quantity 
            OrderItem.objects.create( order=order, product=product, seller=product.seller, quantity=cart_item.quantity, price=price, grand_total=grand_total ) 
            total_amount += grand_total 

            # Add shipping fee 
            order.total_amount = total_amount + shipping_fee 
            order.save() 

            # Empty the cart 
            cart.items.all().delete() 
            serializer = self.get_serializer(order) 
            return Response( serializer.data, status=status.HTTP_201_CREATED )


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated, IsCustomerOrSeller]


    def get_queryset(self):
        user = self.request.user

        if hasattr(user, "seller_profile"):
            return OrderItem.objects.filter(
                seller=user.seller_profile
            )

        # Customer sees items from their own orders 
        if hasattr(user, "customer_profile"): 
            return OrderItem.objects.filter( 
                order__customer=user.customer_profile 
            ) 
        return OrderItem.objects.none()

    # Prevent direct creation 
    def create(self, request, *args, **kwargs): 
        return Response( 
                { 
                    "detail": ( "Order items are created automatically " "during checkout." ) 
                }, status=status.HTTP_405_METHOD_NOT_ALLOWED 
            ) 

    # Prevent direct deletion 
    def destroy(self, request, *args, **kwargs): 
        return Response( 
                { 
                    "detail": ( "Order items cannot be deleted directly." ) 
                }, status=status.HTTP_405_METHOD_NOT_ALLOWED 
            ) 
    

    # Prevent direct replacement 
    def update(self, request, *args, **kwargs): 
        return Response( 
                { 
                    "detail": ( "Order items cannot be modified directly." ) 
                }, status=status.HTTP_405_METHOD_NOT_ALLOWED 
            )