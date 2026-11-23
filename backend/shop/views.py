from django.shortcuts import render
from .serializers import ProductSerializer, ProductImageSerializer, CategorySerializer, ReviewSerializer, AnnouncementSerializer
from .models import Category, Product, ProductImage, Review, Announcement, expire_announcements
from .permissions import IsSeller, IsAdmin, IsCustomer, IsProductImageOwner, IsProductOwner, IsReviewOwner, IsCustomerOrReadOnly, IsSellerOrReadOnly, CanAddProducts

from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly, SAFE_METHODS, AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Q, F, Sum, Value
from django.db.models.functions import Coalesce
from django.db import transaction
from django.db.models import ProtectedError

from cart.models import OrderItem


# Create your views here.
SOLD_STATUSES = ("PENDING", "PROCESSING", "SHIPPED", "DELIVERED")

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
    permission_classes = [IsProductOwner, IsSellerOrReadOnly, CanAddProducts]
    lookup_field = "slug"

    @action(detail=False, methods=["get"], url_path="my-products", permission_classes=[IsAuthenticated, IsSeller])
    def my_products(self, request):
        seller = request.user.seller_profile
        expire_announcements(seller)
        products = (Product.objects.filter(seller=seller).select_related("category", "seller__user", "seller__verified_by")
            .prefetch_related("images"))
        return Response(self.get_serializer(products, many=True).data)

    @action(detail=False, methods=["get"], url_path="my-overview", permission_classes=[IsAuthenticated, IsSeller])
    def my_overview(self, request):
        seller = request.user.seller_profile
        expire_announcements(seller)

        stock = Product.objects.filter(seller=seller).aggregate(active_products=Count("id", filter=Q(is_available=True)), inventory_value=Sum(F("price") * F("stock")),)
        sales = OrderItem.objects.filter(seller=seller, status__in=SOLD_STATUSES).aggregate(units_sold=Coalesce(Sum("quantity"), Value(0)), total_revenue=Coalesce(Sum("grand_total"), Value(0)),)
        return Response({"total_revenue": sales["total_revenue"], "units_sold": sales["units_sold"], "active_products": stock["active_products"], "inventory_value": stock["inventory_value"] or 0,})

    @action(detail=False, methods=["get"], url_path="my-sales", permission_classes=[IsAuthenticated, IsSeller])
    def my_sales(self, request):
        counted = Q(order_item__status__in=SOLD_STATUSES)
        products = (Product.objects.filter(seller=request.user.seller_profile).select_related("category").prefetch_related("images")
            .annotate(
                units_sold=Coalesce(Sum("order_item__quantity", filter=counted), Value(0)),
                revenue=Coalesce(Sum("order_item__grand_total", filter=counted), Value(0)),))

        rows = []
        for p in products:
            primary = next(iter(p.images.all()), None)
            rows.append({
                "id": p.id, "name": p.name, "slug": p.slug,
                "category": p.category.get_category_display(),
                "price": p.price,
                "image": request.build_absolute_uri(primary.image.url) if primary else None,
                "units_sold": p.units_sold, "revenue": p.revenue,
            })

        ranked = sorted(rows, key=lambda r: (-r["units_sold"], r["name"]))
        return Response({"sales_by_product": ranked[:8], "best_selling": [r for r in ranked if r["units_sold"] > 0][:5],
            "least_selling": sorted(rows, key=lambda r: (r["units_sold"], r["name"]))[:5],
        })

    def get_queryset(self):
        user = self.request.user
        if (self.action in ["update", "partial_update", "destroy"] and user.is_authenticated and user.role == "SELLER"):
            return Product.objects.filter(seller=user.seller_profile)
        return Product.objects.all()

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user.seller_profile)

    @action(detail=False, methods=["get"], permission_classes=[AllowAny], authentication_classes=[])
    def featured(self, request):
        products = Product.objects.order_by("-created_at")[:6]
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data) 

    @action(detail=False, methods=["get"], url_path="my-stats", permission_classes=[IsAuthenticated, IsSeller],)
    def my_stats(self, request):
        products = Product.objects.filter(seller=request.user.seller_profile)
        stats = products.aggregate(products=Count("id"), categories=Count("category", distinct=True), live_offers=Count("id", filter=Q(discount_price__gt=0, is_available=True)),)
        return Response(stats)   

    @action(detail=False, methods=["get"], url_path="stats", permission_classes=[AllowAny], authentication_classes=[])
    def stats(self, request):
        live = Product.objects.filter(is_available=True, seller__verification_status="APPROVED",)
        data = live.aggregate(products=Count("id"), categories=Count("category", distinct=True), live_offers=Count("id", filter=Q(discount_price__gt=0)),)
        return Response(data)

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            return Response({"detail": "This product has been ordered, so it can't be deleted. Mark it as unavailable instead."}, status=409,)


class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsProductOwner, IsSeller, IsProductImageOwner, IsSellerOrReadOnly, CanAddProducts]

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.role == "SELLER":
            return ProductImage.objects.filter(product__seller=self.request.user.seller_profile)

        return ProductImage.objects.all()


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsCustomer, IsReviewOwner, IsCustomerOrReadOnly]

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user.customer_profile)


class AnnouncementViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet,):
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAuthenticated, IsSeller, CanAddProducts]

    def get_queryset(self):
        seller = self.request.user.seller_profile
        expire_announcements(seller)
        return Announcement.objects.filter(seller=seller, is_active=True).select_related("product")

    @transaction.atomic
    def perform_create(self, serializer):
        announcement = serializer.save(seller=self.request.user.seller_profile)
        announcement.apply_discount()

    @transaction.atomic
    def perform_destroy(self, instance):
        instance.end()
        instance.delete()
        

# SAFE_METHODS - HTTP methods that do not modify data