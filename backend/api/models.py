# -*- coding: utf-8 -*-
"""
Django models for the API application.

Defines custom user, product, order, and order item models with
clear string representations and type annotations.
"""

from __future__ import annotations

import re
import uuid
from typing import Any

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


def generate_tracking_id() -> str:
    return f"INK-{uuid.uuid4().hex[:12].upper()}"


def generate_referral_code(name: str = "") -> str:
    import random
    import string
    chars = string.ascii_uppercase + string.digits
    while True:
        code = "".join(random.choices(chars, k=10))
        if not CustomUser.objects.filter(referral_code=code).exists():
            return code


class CustomUserManager(BaseUserManager):
    """Manager for ``CustomUser`` with mobile number validation."""

    def _validate_mobile(self, mobile: str) -> None:
        if not re.fullmatch(r"\d{10}", mobile):
            raise ValueError("Mobile number must be exactly 10 digits.")

    def create_user(self, mobile: str, name: str = "", password: str | None = None, **extra_fields: Any) -> "CustomUser":
        self._validate_mobile(mobile)
        user = self.model(mobile=mobile, name=name, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile: str, name: str = "", password: str | None = None, **extra_fields: Any) -> "CustomUser":
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if not password:
            raise ValueError("Superuser must have a password")
        return self.create_user(mobile, name, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """User identified by mobile number."""

    mobile = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100, blank=True)
    age = models.IntegerField(null=True, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    referral_code = models.CharField(max_length=20, unique=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = "mobile"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def get_full_name(self) -> str:
        return self.name or self.mobile

    def get_short_name(self) -> str:
        return self.name or self.mobile

    def __str__(self) -> str:
        return f"{self.name or 'User'} ({self.mobile})"

    def __repr__(self) -> str:
        return f"<CustomUser mobile={self.mobile!r} name={self.name!r}>"


class Product(models.Model):
    """Product available for purchase."""

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cart_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.TextField()  # Stores SVG string or asset path
    description = models.TextField()

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"<Product id={self.id!r} name={self.name!r}>"


class Order(models.Model):
    """Order placed by a user or guest."""

    STATUS_CHOICES = [
        ("Placed", "Placed"),
        ("Printing", "Printing"),
        ("Dispatched", "Dispatched"),
        ("Delivery", "Out for Delivery"),
    ]

    tracking_id = models.CharField(max_length=50, unique=True, default=generate_tracking_id, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders")
    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=10)
    customer_email = models.EmailField()
    shipping_address = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_mode = models.CharField(max_length=50)
    referral_code = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Placed")
    created_at = models.DateTimeField(auto_now_add=True)
    est_delivery = models.CharField(max_length=50)

    def get_simulated_status(self) -> str:
        """Dynamically calculate order status based on time elapsed since creation."""
        elapsed = (timezone.now() - self.created_at).total_seconds()
        if elapsed < 15:
            return "Placed"
        elif elapsed < 35:
            return "Printing"
        elif elapsed < 60:
            return "Dispatched"
        else:
            return "Delivery"

    def __str__(self) -> str:
        return f"Order {self.tracking_id} - {self.customer_name}"

    def __repr__(self) -> str:
        return f"<Order tracking_id={self.tracking_id!r} status={self.status!r}>"


class OrderItem(models.Model):
    """Individual item within an order."""

    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    CUSTOMIZATION_CHOICES = [
        ("text", "Text"),
        ("photo", "Photo"),
    ]
    customization_type = models.CharField(max_length=10, choices=CUSTOMIZATION_CHOICES)
    customization_data = models.TextField()  # Text content or base64 image data
    customization_font = models.CharField(max_length=50, null=True, blank=True)
    customization_color = models.CharField(max_length=50, null=True, blank=True)
    customization_size = models.CharField(max_length=50, null=True, blank=True)
    customization_summary = models.CharField(max_length=255)

    def __str__(self) -> str:
        product_name = self.product.name if self.product else "Deleted Product"
        return f"{self.quantity} x {product_name} (Order {self.order.tracking_id})"

    def __repr__(self) -> str:
        return f"<OrderItem order={self.order.tracking_id!r} product={self.product_id!r} qty={self.quantity}>"


class WalletWithdrawal(models.Model):
    """Model to track user wallet withdrawals along with bank details."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="withdrawals")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    account_number = models.CharField(max_length=50)
    account_holder_name = models.CharField(max_length=100)
    bank_name = models.CharField(max_length=100)
    ifsc_code = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Withdrawal of ₹{self.amount} by {self.user.name or self.user.mobile} at {self.created_at}"

    def __repr__(self) -> str:
        return f"<WalletWithdrawal id={self.id!r} user={self.user.mobile!r} amount={self.amount}>"


class ProductDesign(models.Model):
    """
    A ready-made design template that can be applied to a product.
    Managed entirely from Django admin — admins upload images and set metadata.
    """

    PRODUCT_TYPES = [
        ('mug',    'Mug'),
        ('tshirt', 'T-Shirt'),
        ('polo',   'Polo T-Shirt'),
        ('cup',    'Cup'),
    ]

    CATEGORY_CHOICES = [
        ('birthday',  'Birthday'),
        ('love',      'Love & Anniversary'),
        ('family',    'Family & Parents'),
        ('friends',   'Friends'),
        ('cats',      'Cats & Pets'),
        ('general',   'General & Holiday'),
        ('motivational', 'Motivational'),
        ('custom',    'Custom / Other'),
    ]

    product_type   = models.CharField(max_length=20, choices=PRODUCT_TYPES, db_index=True)
    name           = models.CharField(max_length=120)
    category       = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='general')
    image          = models.ImageField(upload_to='designs/', help_text="Upload the design wrap image")
    price          = models.DecimalField(max_digits=10, decimal_places=2, default=219)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, default=299)
    description    = models.TextField(blank=True, default="")
    sort_order     = models.PositiveIntegerField(default=0, help_text="Lower numbers appear first")
    is_active      = models.BooleanField(default=True)
    created_at     = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sort_order', '-created_at']
        verbose_name = "Product Design"
        verbose_name_plural = "Product Designs"

    def __str__(self) -> str:
        return f"[{self.get_product_type_display()}] {self.name}"

    def __repr__(self) -> str:
        return f"<ProductDesign id={self.id!r} type={self.product_type!r} name={self.name!r}>"

