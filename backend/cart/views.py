import uuid

from django.db import transaction
from django.db.models import F, Prefetch
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models import CustomerAddress, CustomerProfile
from shop.models import Product
from .models import Cart, CartItem, Notification, Order, OrderItem, current_price
from .permissions import IsCustomer, IsCustomerOrSeller
from .serializers import (
    CartSerializer, NotificationSerializer, OrderSerializer, OrderItemSerializer,
    AddToCartSerializer, UpdateQuantitySerializer,
)


# ---------- helpers ----------

def get_customer(user):
    profile, _ = CustomerProfile.objects.get_or_create(user=user)
    return profile


def get_cart(user):
    cart, _ = Cart.objects.get_or_create(customer=get_customer(user))
    return cart


def cart_payload(request):
    """The full serialized cart, with everything the serializer needs prefetched."""
    cart = Cart.objects.prefetch_related(
        Prefetch(
            "items",
            queryset=CartItem.objects.select_related("product__seller").prefetch_related("product__images"),
        )
    ).get(pk=get_cart(request.user).pk)
    return CartSerializer(cart, context={"request": request}).data


def check_stock(product, quantity):
    if product.stock == 0:
        raise ValidationError({"quantity": "Out of stock."})
    if quantity > product.stock:
        raise ValidationError({"quantity": f"Only {product.stock} left in stock."})


def cancel_and_restock(item):
    Product.objects.filter(pk=item.product_id).update(stock=F("stock") + item.quantity)
    item.status = "CANCELLED"
    item.save(update_fields=["status"])


# ---------- cart ----------

class CartViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated, IsCustomer]

    def get_queryset(self):
        return Cart.objects.filter(customer__user=self.request.user)

    @action(detail=False, methods=["get"])
    def mine(self, request):
        """The logged-in customer's cart (created on first use)."""
        return Response(cart_payload(request))


class CartItemViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, IsCustomer]

    def get_queryset(self):
        return CartItem.objects.filter(cart__customer__user=self.request.user).select_related("product__seller")

    @transaction.atomic
    def create(self, request):
        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.validated_data["product"]
        quantity = serializer.validated_data["quantity"]

        cart = get_cart(request.user)
        item = CartItem.objects.filter(cart=cart, product=product).first()
        new_quantity = quantity + (item.quantity if item else 0)
        check_stock(product, new_quantity)

        if item:
            item.quantity = new_quantity
            item.save(update_fields=["quantity", "updated_at"])
        else:
            CartItem.objects.create(cart=cart, product=product, quantity=new_quantity)
        return Response(cart_payload(request), status=201)

    def partial_update(self, request, pk=None):
        item = self.get_object()
        serializer = UpdateQuantitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        quantity = serializer.validated_data["quantity"]
        check_stock(item.product, quantity)

        item.quantity = quantity
        item.save(update_fields=["quantity", "updated_at"])
        return Response(cart_payload(request))

    def destroy(self, request, pk=None):
        self.get_object().delete()
        return Response(cart_payload(request))

    @action(detail=False, methods=["delete"])
    def clear(self, request):
        CartItem.objects.filter(cart__customer__user=request.user).delete()
        return Response(cart_payload(request))


# ---------- orders ----------

class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    """Customers can read their orders. Orders are only ever created by checkout."""
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsCustomer]

    def get_queryset(self):
        return (
            Order.objects.filter(customer__user=self.request.user)
            .prefetch_related("items__product", "items__seller")
            .order_by("-created_at")
        )

    @action(detail=False, methods=["post"])
    def checkout(self, request):
        """Body: {"address_id": <id of one of the customer's saved addresses>}"""
        customer = get_customer(request.user)

        with transaction.atomic():
            cart = Cart.objects.filter(customer=customer).first()
            items = list(cart.items.all()) if cart else []
            if not items:
                return Response({"detail": "Your cart is empty."}, status=400)

            try:
                address = CustomerAddress.objects.get(
                    pk=int(request.data.get("address_id")), customer=customer
                )
            except (TypeError, ValueError, CustomerAddress.DoesNotExist):
                return Response({"detail": "Choose a delivery address to continue."}, status=400)

            # Lock the product rows so two checkouts can't both take the last unit
            # (this lock is a no-op on SQLite but works on PostgreSQL and MySQL).
            products = {
                p.pk: p
                for p in Product.objects.select_for_update()
                .select_related("seller__user")
                .filter(pk__in=[i.product_id for i in items])
            }

            problems = []
            for item in items:
                p = products[item.product_id]
                if not p.is_available or not p.seller.is_verified:
                    problems.append(f"{p.name} is no longer available.")
                elif p.stock == 0:
                    problems.append(f"{p.name} is out of stock.")
                elif item.quantity > p.stock:
                    problems.append(f"{p.name}: only {p.stock} left in stock.")
            if problems:
                return Response(
                    {"detail": "Some items in your cart can't be ordered.", "issues": problems},
                    status=400,
                )

            shipping_fee = 0   # flat zero for now
            # The address is copied onto the order, so later edits or deletes of the
            # saved address never change where an existing order is going.
            order = Order.objects.create(
                customer=customer,
                order_number=f"ORD-{uuid.uuid4().hex[:10].upper()}",
                total_amount=0,
                shipping_fee=shipping_fee,
                shipping_name=request.user.get_full_name().strip(),
                shipping_phone=request.user.phone_number,
                shipping_address=address.shipping_address,
                shipping_street=address.street,
                shipping_county=address.county,
                shipping_postal_code=address.postal_code,
            )

            total = 0
            lines_by_seller = {}
            for item in items:
                p = products[item.product_id]
                price = current_price(p)   # the price the customer saw, including any live offer
                OrderItem.objects.create(
                    order=order, product=p, seller=p.seller,
                    quantity=item.quantity, price=price,   # grand_total is set in OrderItem.save()
                )
                Product.objects.filter(pk=p.pk).update(stock=F("stock") - item.quantity)
                total += price * item.quantity
                lines_by_seller.setdefault(p.seller, []).append(f"{item.quantity} × {p.name}")

            order.total_amount = total + shipping_fee
            order.save(update_fields=["total_amount", "updated_at"])
            cart.items.all().delete()

            # One notification per seller, listing only that seller's items from this order.
            Notification.objects.bulk_create([
                Notification(
                    recipient=seller.user,
                    order=order,
                    message=f"New order {order.order_number}: {', '.join(lines)}"[:255],
                )
                for seller, lines in lines_by_seller.items()
            ])

        return Response(self.get_serializer(order).data, status=201)


# Which status a seller may move an item to from each current status.
SELLER_TRANSITIONS = {
    "PENDING": {"PROCESSING", "CANCELLED"},
    "PROCESSING": {"SHIPPED", "CANCELLED"},
    "SHIPPED": {"DELIVERED"},
}


class OrderItemViewSet(viewsets.ReadOnlyModelViewSet):
    """Sellers see items sold, customers see items they bought. Changes happen only via the actions."""
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated, IsCustomerOrSeller]

    def get_queryset(self):
        user = self.request.user
        qs = OrderItem.objects.select_related("order", "product", "seller").order_by("-order__created_at", "id")
        if user.role == "SELLER":
            return qs.filter(seller__user=user)
        if user.role == "BUYER":
            return qs.filter(order__customer__user=user)
        return qs.none()

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        """A customer cancels an item the seller hasn't started processing."""
        if request.user.role != "BUYER":
            raise PermissionDenied("Only the customer can cancel their own order item.")
        with transaction.atomic():
            item = self.get_object()
            if item.status != "PENDING":
                return Response(
                    {"detail": f"This item is already {item.get_status_display().lower()} and can't be cancelled."},
                    status=400,
                )
            cancel_and_restock(item)
        return Response(self.get_serializer(item).data)

    @action(detail=True, methods=["post"], url_path="update-status")
    def update_status(self, request, pk=None):
        """A seller moves an item along: PENDING → PROCESSING → SHIPPED → DELIVERED (or CANCELLED)."""
        if request.user.role != "SELLER":
            raise PermissionDenied("Only the seller can update an item's status.")
        new_status = request.data.get("status")
        with transaction.atomic():
            item = self.get_object()
            allowed = SELLER_TRANSITIONS.get(item.status, set())
            if new_status not in allowed:
                options = ", ".join(sorted(allowed)) or "none, this item is final"
                return Response(
                    {"detail": f"Can't change a {item.status} item to {new_status}. Allowed: {options}."},
                    status=400,
                )
            if new_status == "CANCELLED":
                cancel_and_restock(item)
            else:
                item.status = new_status
                item.save(update_fields=["status"])
        return Response(self.get_serializer(item).data)


# ---------- notifications ----------

class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    """A user's own notifications. Sellers get one per order that contains their products."""
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = (
            Notification.objects.filter(recipient=self.request.user)
            .select_related("order")
            .prefetch_related("order__items__product__images", "order__items__seller")
        )
        if self.request.query_params.get("unread") == "true":
            qs = qs.filter(is_read=False)
        return qs

    @action(detail=False, methods=["get"], url_path="unread-count")
    def unread_count(self, request):
        count = Notification.objects.filter(recipient=request.user, is_read=False).count()
        return Response({"unread": count})

    @action(detail=True, methods=["post"], url_path="mark-read")
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        if not notification.is_read:
            notification.is_read = True
            notification.save(update_fields=["is_read"])
        return Response(self.get_serializer(notification).data)

    @action(detail=False, methods=["post"], url_path="mark-all-read")
    def mark_all_read(self, request):
        Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
        return Response({"unread": 0})