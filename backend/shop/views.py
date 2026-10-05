from django.shortcuts import render
from .serializers import ProductSerializer, ProductImageSerializer, CategorySerializer, ReviewSerializer
from .models import Category, Product, ProductImage, Review
from .permissions import IsSeller, IsAdmin, IsCustomer, IsProductImageOwner, IsProductOwner, IsReviewOwner, IsCustomerOrReadOnly, IsSellerOrReadOnly

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, SAFE_METHODS, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response


# Create your views here.
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdmin]

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]

        return [IsAdmin()]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsProductOwner, IsSellerOrReadOnly]
    lookup_field = "slug"

    def get_queryset(self):
        user = self.request.user
        if (
            self.action in ["update", "partial_update", "destroy"]
            and user.is_authenticated
            and user.role == "SELLER"
        ):
            return Product.objects.filter(seller=user.seller_profile)
        return Product.objects.all()

    def perform_create(self, serializer):
        serializer.save(
            seller=self.request.user.seller_profile
        )

    @action(detail=False, methods=["get"], permission_classes=[AllowAny])
    def featured(self, request):
        products = Product.objects.order_by("-created_at")[:6]
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)    

class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsProductOwner, IsSeller, IsProductImageOwner, IsSellerOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.role == "SELLER":
            return ProductImage.objects.filter(
                product__seller=self.request.user.seller_profile
            )

        return ProductImage.objects.all()


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsCustomer, IsReviewOwner, IsCustomerOrReadOnly]

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        serializer.save(
            customer=self.request.user.customer_profile
        )



# SAFE_METHODS - HTTP methods that do not modify data