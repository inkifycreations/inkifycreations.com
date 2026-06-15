# -*- coding: utf-8 -*-
"""
Django models for the API application.

Defines custom user, product, order, and order item models with
clear string representations and type annotations.
"""

from __future__ import annotations

import re
import uuid
from decimal import Decimal
from typing import Any

from django.conf import settings
from django.db import models
from django.db.models import QuerySet
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
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
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

    id: int
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cart_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.TextField()  # Stores SVG string or asset path
    description = models.TextField()
    is_trending = models.BooleanField(default=False)
    trending_tagline = models.CharField(max_length=255, blank=True, default="")
    trending_image = models.ImageField(upload_to='products/', null=True, blank=True, help_text="High-quality image for the trending popup")

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"<Product id={self.id!r} name={self.name!r}>"


class Order(models.Model):
    """Order placed by a user or guest."""

    id: int
    items: QuerySet[OrderItem]

    STATUS_CHOICES = [
        ("Placed", "Placed"),
        ("Printing", "Printing"),
        ("Dispatched", "Dispatched"),
        ("Delivery", "Out for Delivery"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
        ("Refunded", "Refunded"),
        ("Returned", "Returned"),
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
    reward_credited = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    est_delivery = models.CharField(max_length=50)

    def get_simulated_status(self) -> str:
        """Dynamically calculate order status unless it has reached a finalized state."""
        if self.status in ["Completed", "Cancelled", "Refunded", "Returned"]:
            return self.status
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

    id: int
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_id: int | None
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

    id: int
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

    id: int
    PRODUCT_TYPES = [
        ('mug',    'Mug'),
        ('tshirt', 'T-Shirt'),
        ('polo',   'Polo T-Shirt'),
        ('bottle', 'Bottle'),
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
    price          = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('239.00'))
    original_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('299.00'))
    description    = models.TextField(blank=True, default="")
    sort_order     = models.PositiveIntegerField(default=0, help_text="Lower numbers appear first")
    is_active      = models.BooleanField(default=True)
    created_at     = models.DateTimeField(auto_now_add=True)

    def get_product_type_display(self) -> str:
        return dict(self.PRODUCT_TYPES).get(self.product_type, self.product_type)

    class Meta:
        ordering = ['sort_order', '-created_at']
        verbose_name = "Product Design"
        verbose_name_plural = "Product Designs"

    def __str__(self) -> str:
        return f"[{self.get_product_type_display()}] {self.name}"

    def __repr__(self) -> str:
        return f"<ProductDesign id={self.id!r} type={self.product_type!r} name={self.name!r}>"


class ProductReview(models.Model):
    """
    Flipkart/Amazon style product review and rating model.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(default=5)  # 1 to 5 stars
    title = models.CharField(max_length=150)
    comment = models.TextField()
    image = models.ImageField(upload_to='reviews/', null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    helpful_users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='helpful_reviews')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"{self.product.name} - {self.rating}* by {self.user.mobile}"

    def __repr__(self) -> str:
        return f"<ProductReview id={self.id!r} product={self.product.name!r} rating={self.rating}>"


class TrendingDesign(models.Model):
    """
    A trending design template with custom tagline, name, image, price, and product ID.
    Used for advertisement purposes.
    """
    name = models.CharField(max_length=100, help_text="Name of the trending design")
    tagline = models.CharField(max_length=255, blank=True, help_text="Tagline or short description")
    image = models.ImageField(upload_to='trending/', help_text="Upload high-quality image for the trending blueprints display")
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Price to display (blank to hide)")
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Original price to show strike-through (optional)")
    product_id = models.IntegerField(null=True, blank=True, help_text="ID of the product to customize when clicked (e.g. 1 for T-Shirt, 4 for Mug)")
    sort_order = models.PositiveIntegerField(default=0, help_text="Lower numbers appear first")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sort_order', '-created_at']
        verbose_name = "Trending Design"
        verbose_name_plural = "Trending Designs"

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"<TrendingDesign id={self.id!r} name={self.name!r}>"


class WalletTransaction(models.Model):
    """Logs user wallet credit, debit, withdrawal, and reversal transactions."""

    TYPE_CHOICES = [
        ('referral_credit', 'Referral Credit'),
        ('coupon_credit', 'Coupon Credit'),
        ('reversal', 'Reversal'),
        ('withdrawal', 'Withdrawal'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('reversed', 'Reversed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="wallet_transactions")
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, related_name="wallet_transactions")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')
    linked_code = models.CharField(max_length=50, blank=True, default='')
    linked_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="referral_earnings")
    note = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"WalletTransaction {self.id}: {self.user.mobile} - {self.type} - ₹{self.amount}"

    def __repr__(self) -> str:
        return f"<WalletTransaction id={self.id} user={self.user.mobile} type={self.type} amount={self.amount}>"


class ReferralUsageLog(models.Model):
    """Tracks usage of coupon or referral codes per user to prevent duplicate abuse."""

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('credited', 'Credited'),
        ('reversed', 'Reversed'),
    ]

    referral_code = models.CharField(max_length=50, db_index=True)
    used_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="referral_usages")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="referral_usages")
    reward_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"ReferralUsage {self.referral_code} used by {self.used_by.mobile} (Order #{self.order.tracking_id})"

    def __repr__(self) -> str:
        return f"<ReferralUsageLog code={self.referral_code} user={self.used_by.mobile} status={self.reward_status}>"


# Signal receivers to trigger wallet rewards and reversals on Order status updates
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

@receiver(pre_save, sender=Order)
def order_pre_save(sender, instance, **kwargs):
    if instance.pk:
        try:
            instance._old_status = Order.objects.get(pk=instance.pk).status
        except Order.DoesNotExist:
            instance._old_status = None
    else:
        instance._old_status = None


@receiver(post_save, sender=Order)
def order_post_save(sender, instance, created, **kwargs):
    old_status = getattr(instance, '_old_status', None)
    new_status = instance.status

    # Transition to Completed: credit wallet cashback
    if new_status == "Completed" and old_status != "Completed":
        # Generate referral code for user if they don't have one yet
        buyer = instance.user
        if buyer and not buyer.referral_code:
            buyer.referral_code = generate_referral_code(buyer.name or buyer.mobile)
            buyer.save(update_fields=['referral_code'])

        if instance.referral_code and not instance.reward_credited:
            from decimal import Decimal
            from django.contrib.auth import get_user_model
            
            User = get_user_model()
            code = instance.referral_code.strip()
            
            # Find the referrer (owner of referral_code), excluding the buyer to prevent self-referral
            ref_owner_query = User.objects.filter(referral_code__iexact=code)
            if buyer:
                ref_owner_query = ref_owner_query.exclude(pk=buyer.pk)
            referrer = ref_owner_query.first()
            
            # 1. Credit the buyer (only if registered user)
            if buyer:
                buyer.wallet_balance += Decimal('10.00')
                buyer.save(update_fields=['wallet_balance'])
                
                # Create WalletTransaction for buyer
                WalletTransaction.objects.create(
                    user=buyer,
                    order=instance,
                    amount=Decimal('10.00'),
                    type='referral_credit' if referrer else 'coupon_credit',
                    status='completed',
                    linked_code=instance.referral_code,
                    linked_user=referrer,
                    note=f"₹10 cashback reward for using code {instance.referral_code} on order #{instance.tracking_id}."
                )

            # 2. Credit the referrer (if valid user referral code applied)
            if referrer:
                referrer.wallet_balance += Decimal('10.00')
                referrer.save(update_fields=['wallet_balance'])
                
                # Create WalletTransaction for referrer
                WalletTransaction.objects.create(
                    user=referrer,
                    order=instance,
                    amount=Decimal('10.00'),
                    type='referral_credit',
                    status='completed',
                    linked_code=instance.referral_code,
                    linked_user=buyer,
                    note=f"₹10 referral reward for order #{instance.tracking_id} placed by {buyer.name or buyer.mobile if buyer else 'Guest'}."
                )

            # Prevent signal loop using query update
            Order.objects.filter(pk=instance.pk).update(reward_credited=True)
            instance.reward_credited = True
            
            # Update log in ReferralUsageLog
            ReferralUsageLog.objects.filter(order=instance).update(reward_status='credited')

    # Transition to Cancelled/Refunded/Returned: reverse credits and refund payments
    elif new_status in ["Cancelled", "Refunded", "Returned"] and old_status not in ["Cancelled", "Refunded", "Returned"]:
        from decimal import Decimal
        
        # 1. Reverse credits
        if instance.reward_credited:
            txns = WalletTransaction.objects.filter(order=instance, type__in=['referral_credit', 'coupon_credit'], status='completed')
            for txn in txns:
                u = txn.user
                u.wallet_balance = max(Decimal('0.00'), u.wallet_balance - txn.amount)
                u.save(update_fields=['wallet_balance'])
                
                WalletTransaction.objects.create(
                    user=u,
                    order=instance,
                    amount=-txn.amount,
                    type='reversal',
                    status='completed',
                    linked_code=txn.linked_code,
                    note=f"Reversal of ₹{txn.amount} reward from order #{instance.tracking_id} due to order status: {new_status}."
                )
                
                txn.status = 'reversed'
                txn.save(update_fields=['status'])
            
            Order.objects.filter(pk=instance.pk).update(reward_credited=False)
            instance.reward_credited = False
            
            ReferralUsageLog.objects.filter(order=instance).update(reward_status='reversed')

        # 2. Refund wallet payment
        wallet_payment_txn = WalletTransaction.objects.filter(order=instance, type='withdrawal', status='completed').first()
        if wallet_payment_txn:
            u = wallet_payment_txn.user
            refund_amount = abs(wallet_payment_txn.amount)
            u.wallet_balance += refund_amount
            u.save(update_fields=['wallet_balance'])
            
            WalletTransaction.objects.create(
                user=u,
                order=instance,
                amount=refund_amount,
                type='reversal',
                status='completed',
                note=f"Refund of ₹{refund_amount} wallet payment for order #{instance.tracking_id} due to cancellation."
            )
            
            wallet_payment_txn.status = 'reversed'
            wallet_payment_txn.save(update_fields=['status'])




