from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from .models import Wishlist, WishlistItem
from .serializers import WishlistItemSerializer, WishlistSerializer
from .permissions import IsCustomer

# Create your views here.
class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated, IsCustomer]

    def get_queryset(self):
        return Wishlist.objects.filter(
            customer=self.request.user.customer_profile
        )

    def perform_create(self, serializer):
        customer = self.request.user.customer_profile

        wishlist, created = Wishlist.objects.get_or_create(
            customer=customer
        )

        if not created:
            return

        serializer.save(customer=customer)

    @action(
        detail=False,
        methods=["get"],
        url_path="my-wishlist"
    )
    def my_wishlist(self, request):
        customer = request.user.customer_profile

        wishlist, created = Wishlist.objects.get_or_create(
            customer=customer
        )

        serializer = self.get_serializer(wishlist)

        return Response(serializer.data)


class WishlistItemViewSet(viewsets.ModelViewSet):
    queryset = WishlistItem.objects.all()
    serializer_class = WishlistItemSerializer
    permission_classes = [IsCustomer]

    def get_queryset(self):
        return WishlistItem.objects.filter(
            wishlist__customer=self.request.user.customer_profile
        )

    def create(self, request, *args, **kwargs):
        customer = request.user.customer_profile

        wishlist, created = Wishlist.objects.get_or_create(
            customer=customer
        )

        product_id = request.data.get("product")

        if not product_id:
            return Response(
                {"detail": "Product is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if WishlistItem.objects.filter(
            wishlist=wishlist,
            product_id=product_id
        ).exists():

            return Response(
                {
                    "detail": (
                        "This product is already "
                        "in your wishlist."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        serializer.save(wishlist=wishlist)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )