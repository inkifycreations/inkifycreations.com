from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model as _get_user_model
User = _get_user_model()
from django.db import transaction
from django.views.generic import TemplateView
from typing import cast, Dict, Any
import uuid
from decimal import Decimal
import urllib.request
import json
import html
import base64
import threading
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.db import close_old_connections




from .models import Product, Order, OrderItem, generate_referral_code, WalletWithdrawal, ProductDesign, CustomUser, ProductReview, TrendingDesign, WalletTransaction, ReferralUsageLog
from .serializers import CustomUserSerializer, ProductSerializer, OrderSerializer, ProductDesignSerializer, ProductReviewSerializer, TrendingDesignSerializer, WalletTransactionSerializer

# User is already defined on line 7

def decode_base64_image(data_str):
    if not data_str or "," not in data_str:
        return None, None, None
    try:
        header, base64_data = data_str.split(",", 1)
        if "data:image/" in header:
            # e.g. data:image/png;base64
            mime_type = header.split(";")[0].replace("data:", "")
            ext = mime_type.split("/")[-1]
            # Handle standard image extensions / custom mime mapping
            if ext == "jpeg":
                ext = "jpg"
            photo_bytes = base64.b64decode(base64_data)
            return photo_bytes, mime_type, ext
    except Exception:
        pass
    return None, None, None


def send_order_notifications_bg(order_id):
    close_old_connections()
    try:
        from .models import Order
        order = Order.objects.get(pk=order_id)
        
        # 1. EMAIL NOTIFICATION LOGIC
        try:
            admin_email = 'jayaprakashporapu84@gmail.com'
            subject = f'New Order Placed - Tracking ID: {order.tracking_id}'
            
            lines = [
                f'Tracking ID: {order.tracking_id}',
                f'Customer Name: {order.customer_name}',
                f'Phone: {order.customer_phone}',
                f'Email: {order.customer_email}',
                f'Shipping Address: {order.shipping_address}',
                f'Amount: ₹{order.amount}',
                f'Payment Mode: {order.payment_mode}',
                f'Estimated Delivery: {order.est_delivery}',
                '',
                'Items:'
            ]
            items_html = ""
            attachments = []
            
            for index, item in enumerate(order.items.all()):
                product_name = item.product.name if item.product else 'Deleted Product'
                lines.append(f"- {item.quantity} x {product_name} @ ₹{item.price} | {item.customization_summary or 'No customization'}")
                
                customization_div = ""
                if item.customization_summary:
                    customization_div = f'<div class="item-customization" style="font-size: 12px; color: #888; margin-top: 5px; font-style: italic;">Customization: {html.escape(item.customization_summary)}</div>'
                
                # Extract base64 image if any
                if item.customization_type == 'photo' and item.customization_data:
                    photo_bytes, mime_type, ext = decode_base64_image(item.customization_data)
                    if photo_bytes:
                        filename = f"customization_{order.tracking_id}_{index + 1}.{ext}"
                        attachments.append((filename, photo_bytes, mime_type))
                        customization_div += f'<div style="font-size: 12px; color: #6C63FF; margin-top: 5px; font-weight: bold;">[Image Attachment: {filename}]</div>'
                
                items_html += f"""
                <div class="item-card" style="background: #f8f9fa; border-radius: 8px; padding: 15px; margin-bottom: 10px; border-left: 4px solid #6C63FF;">
                    <div class="item-header" style="display: flex; justify-content: space-between; font-weight: bold; font-size: 14px; margin-bottom: 5px;">
                        <span>{html.escape(product_name)} x {item.quantity}</span>
                        <span>₹{item.price * item.quantity}</span>
                    </div>
                    {customization_div}
                </div>
                """

            message = "\n".join(lines)
            
            # HTML format for the email
            html_message = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>{subject}</title>
</head>
<body style="font-family: 'Inter', Roboto, Arial, sans-serif; background-color: #f4f5f7; margin: 0; padding: 20px; color: #333;">
<div class="container" style="max-width: 600px; background: #ffffff; margin: 0 auto; padding: 30px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
    <div class="header" style="background: linear-gradient(135deg, #6C63FF, #3F3D56); padding: 20px; border-radius: 8px 8px 0 0; text-align: center; color: white;">
        <h2 style="margin: 0; font-size: 24px; font-weight: 600; letter-spacing: 0.5px;">Order Confirmation</h2>
    </div>
    <div class="order-info" style="margin: 25px 0; border-bottom: 1px solid #eee; padding-bottom: 20px;">
        <div class="info-row" style="display: flex; justify-content: space-between; margin-bottom: 10px; font-size: 14px;">
            <span class="info-label" style="font-weight: bold; color: #666;">Tracking ID:</span>
            <span class="info-value" style="color: #111;"><b>{order.tracking_id}</b></span>
        </div>
        <div class="info-row" style="display: flex; justify-content: space-between; margin-bottom: 10px; font-size: 14px;">
            <span class="info-label" style="font-weight: bold; color: #666;">Customer Name:</span>
            <span class="info-value" style="color: #111;">{html.escape(order.customer_name)}</span>
        </div>
        <div class="info-row" style="display: flex; justify-content: space-between; margin-bottom: 10px; font-size: 14px;">
            <span class="info-label" style="font-weight: bold; color: #666;">Phone:</span>
            <span class="info-value" style="color: #111;">{html.escape(order.customer_phone)}</span>
        </div>
        <div class="info-row" style="display: flex; justify-content: space-between; margin-bottom: 10px; font-size: 14px;">
            <span class="info-label" style="font-weight: bold; color: #666;">Email:</span>
            <span class="info-value" style="color: #111;">{html.escape(order.customer_email)}</span>
        </div>
        <div class="info-row" style="display: flex; justify-content: space-between; margin-bottom: 10px; font-size: 14px;">
            <span class="info-label" style="font-weight: bold; color: #666;">Shipping Address:</span>
            <span class="info-value" style="color: #111;">{html.escape(order.shipping_address)}</span>
        </div>
        <div class="info-row" style="display: flex; justify-content: space-between; margin-bottom: 10px; font-size: 14px;">
            <span class="info-label" style="font-weight: bold; color: #666;">Payment Mode:</span>
            <span class="info-value" style="color: #111;">{html.escape(order.payment_mode)}</span>
        </div>
        <div class="info-row" style="display: flex; justify-content: space-between; margin-bottom: 10px; font-size: 14px;">
            <span class="info-label" style="font-weight: bold; color: #666;">Estimated Delivery:</span>
            <span class="info-value" style="color: #111;">{html.escape(order.est_delivery)}</span>
        </div>
    </div>
    <div class="items-title" style="font-size: 16px; font-weight: bold; margin-bottom: 15px; color: #6C63FF;">Ordered Items</div>
    {items_html}
    <div class="total-section" style="margin-top: 25px; padding-top: 20px; border-top: 2px solid #eee; font-size: 18px; font-weight: bold; display: flex; justify-content: space-between; color: #6C63FF;">
        <span>Total Amount Paid:</span>
        <span>₹{order.amount}</span>
    </div>
    <div class="footer" style="text-align: center; margin-top: 30px; font-size: 12px; color: #aaa;">
        Thank you for choosing Inkify Creations! If you have any questions, please contact our support.
    </div>
</div>
</body>
</html>"""

            from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@inkify.local')
            recipients = [admin_email]
            if order.customer_email and order.customer_email.strip().lower() != admin_email.lower():
                recipients.append(order.customer_email.strip())

            # Use EmailMultiAlternatives to attach the images
            email_msg = EmailMultiAlternatives(
                subject=subject,
                body=message,
                from_email=from_email,
                to=recipients
            )
            email_msg.attach_alternative(html_message, "text/html")
            for filename, file_data, file_mime in attachments:
                email_msg.attach(filename, file_data, file_mime)
                
            email_msg.send()
        except Exception:
            pass

        # 2. TELEGRAM NOTIFICATION LOGIC
        try:
            bot_token = getattr(settings, 'TELEGRAM_BOT_TOKEN', '') or '8136363344:AAGd58z4mMC0mifFh-agrGofVqtzWcsbPwQ'
            chat_id = getattr(settings, 'TELEGRAM_PERSONAL_CHAT_ID', '') or '5531966096'
            if bot_token and chat_id:
                # Send standard text details
                telegram_lines = [
                    "<b>🔔 New Order Placed!</b>",
                    f"<b>Tracking ID:</b> <code>{order.tracking_id}</code>",
                    f"<b>Customer Name:</b> {html.escape(order.customer_name)}",
                    f"<b>Phone:</b> {html.escape(order.customer_phone)}",
                    f"<b>Email:</b> {html.escape(order.customer_email)}",
                    f"<b>Address:</b> {html.escape(order.shipping_address)}",
                    f"<b>Amount:</b> ₹{order.amount}",
                    f"<b>Payment Mode:</b> {order.payment_mode}",
                    f"<b>Est. Delivery:</b> {order.est_delivery}",
                    "",
                    "<b>📦 Items Ordered:</b>"
                ]
                for item in order.items.all():
                    product_name = item.product.name if item.product else 'Deleted Product'
                    customization_str = f" | {item.customization_summary}" if item.customization_summary else ""
                    
                    # Try to find a matching product design to get its absolute image URL
                    design_image_url = ""
                    if item.customization_summary:
                        for design in ProductDesign.objects.filter(is_active=True):
                            if design.name.lower() in item.customization_summary.lower():
                                design_image_url = f"http://127.0.0.1:8000{design.image.url}"
                                break
                    
                    if design_image_url:
                        img_info = f" (Image: {design_image_url})"
                    elif item.product and item.product.image and not item.product.image.startswith('<svg'):
                        if item.product.image.startswith('http://') or item.product.image.startswith('https://'):
                            product_img_url = item.product.image
                        else:
                            product_img_url = f"http://127.0.0.1:8000/{item.product.image.lstrip('/')}"
                        img_info = f" (Image: {product_img_url})"
                    else:
                        img_info = ""

                    telegram_lines.append(f"• {item.quantity} x {html.escape(product_name)} @ ₹{item.price}{html.escape(customization_str)}{img_info}")

                telegram_message = "\n".join(telegram_lines)
                telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
                payload = {
                    "chat_id": chat_id,
                    "text": telegram_message,
                    "parse_mode": "HTML"
                }
                req_data = json.dumps(payload).encode('utf-8')
                req = urllib.request.Request(
                    telegram_url,
                    data=req_data,
                    headers={'Content-Type': 'application/json'},
                    method='POST'
                )
                with urllib.request.urlopen(req, timeout=5) as response:
                    pass

                # Send photographs
                for index, item in enumerate(order.items.all()):
                    if item.customization_type == 'photo' and item.customization_data:
                        photo_bytes, mime_type, ext = decode_base64_image(item.customization_data)
                        if photo_bytes:
                            boundary = '----WebKitFormBoundaryOrderAttachment'
                            body_parts = []
                            
                            body_parts.append(f'--{boundary}'.encode('utf-8'))
                            body_parts.append(f'Content-Disposition: form-data; name="chat_id"'.encode('utf-8'))
                            body_parts.append(''.encode('utf-8'))
                            body_parts.append(str(chat_id).encode('utf-8'))
                            
                            caption_text = f"<b>📸 Custom Photo Blueprint</b>\nProduct: {html.escape(item.product.name if item.product else 'Product')}\nTracking ID: <code>{order.tracking_id}</code>"
                            body_parts.append(f'--{boundary}'.encode('utf-8'))
                            body_parts.append(f'Content-Disposition: form-data; name="caption"'.encode('utf-8'))
                            body_parts.append(''.encode('utf-8'))
                            body_parts.append(caption_text.encode('utf-8'))
                            
                            body_parts.append(f'--{boundary}'.encode('utf-8'))
                            body_parts.append(f'Content-Disposition: form-data; name="parse_mode"'.encode('utf-8'))
                            body_parts.append(''.encode('utf-8'))
                            body_parts.append('HTML'.encode('utf-8'))
                            
                            body_parts.append(f'--{boundary}'.encode('utf-8'))
                            body_parts.append(f'Content-Disposition: form-data; name="photo"; filename="customization_{index + 1}.{ext}"'.encode('utf-8'))
                            body_parts.append(f'Content-Type: {mime_type}'.encode('utf-8'))
                            body_parts.append(''.encode('utf-8'))
                            body_parts.append(photo_bytes)
                            
                            body_parts.append(f'--{boundary}--'.encode('utf-8'))
                            body_parts.append(''.encode('utf-8'))
                            
                            multipart_payload = b'\r\n'.join(body_parts)
                            
                            photo_url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
                            photo_req = urllib.request.Request(
                                photo_url,
                                data=multipart_payload,
                                headers={
                                    'Content-Type': f'multipart/form-data; boundary={boundary}',
                                    'Content-Length': str(len(multipart_payload))
                                },
                                method='POST'
                            )
                            with urllib.request.urlopen(photo_req, timeout=30) as response:
                                pass
        except Exception:
            pass
    except Exception:
        pass
    finally:
        close_old_connections()


def send_withdrawal_notifications_bg(withdrawal_id):
    close_old_connections()
    try:
        from .models import WalletWithdrawal
        withdrawal = WalletWithdrawal.objects.get(pk=withdrawal_id)
        
        bot_token = getattr(settings, 'TELEGRAM_WITHDRAW_BOT_TOKEN', '') or '8661735910:AAHpXRIIJbMpEQOsPK183BS1y39fK6s47d4'
        chat_id = getattr(settings, 'TELEGRAM_WITHDRAW_PERSONAL_CHAT_ID', '') or '5531966096'
        
        if bot_token and chat_id:
            telegram_lines = [
                "<b>💰 New Withdrawal Request!</b>",
                f"<b>Customer Name:</b> {html.escape(withdrawal.user.name or withdrawal.user.mobile)}",
                f"<b>Mobile:</b> {html.escape(withdrawal.user.mobile)}",
                f"<b>Amount:</b> ₹{withdrawal.amount}",
                "",
                "<b>🏦 Bank Details:</b>",
                f"<b>Bank Name:</b> {html.escape(withdrawal.bank_name)}",
                f"<b>Account Holder:</b> {html.escape(withdrawal.account_holder_name)}",
                f"<b>Account Number:</b> <code>{html.escape(withdrawal.account_number)}</code>",
                f"<b>IFSC Code:</b> <code>{html.escape(withdrawal.ifsc_code)}</code>"
            ]
            telegram_message = "\n".join(telegram_lines)
            telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            payload = {
                "chat_id": chat_id,
                "text": telegram_message,
                "parse_mode": "HTML"
            }
            req_data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(
                telegram_url,
                data=req_data,
                headers={'Content-Type': 'application/json'},
                method='POST'
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                pass
    except Exception:
        pass
    finally:
        close_old_connections()


def validate_referral_coupon_code(code: str, user) -> tuple[bool, str, Any]:
    """
    Validates a referral or coupon code.
    Returns (is_valid, error_message, eligible_referrer).
    """
    code = code.strip().upper()
    if not code:
        return False, "Please enter a valid code.", None
        
    # Check if code belongs to an Affiliate Partner (ends with 99)
    if code.endswith('99') and len(code) >= 3:
        if user:
            if ReferralUsageLog.objects.filter(referral_code=code, used_by=user).exists():
                return False, "You have already used this coupon code.", None
        return True, "", None
        
    # User Referral Code checks
    referrer_obj = User.objects.filter(referral_code__iexact=code).first()
    if not referrer_obj:
        return False, "Invalid referral code.", None
        
    referrer = referrer_obj
    
    # Rule FR-01: No self-referral
    if user and referrer.pk == user.pk:
        return False, "You cannot use your own referral code.", None
        
    # Rule FR-04: Referral code can only be used on first-time orders (excluding cancelled)
    if user:
        prior_orders = Order.objects.filter(user=user).exclude(status__in=['Cancelled', 'Refunded', 'Returned'])
        if prior_orders.exists():
            return False, "Referral code can only be used on your first order.", None
            
    # Rule FR-10: Same code not reused by same customer
    if user:
        if ReferralUsageLog.objects.filter(referral_code=code, used_by=user).exists():
            return False, "You have already used this referral code.", None
            
    # Rule FR-08: Referrer must have placed at least 1 completed order to activate code
    referrer_completed_orders = Order.objects.filter(user=referrer, status='Completed')
    if not referrer_completed_orders.exists():
        return False, "This referral code is not yet active.", None
        
    return True, "", referrer


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request):
        mobile = request.data.get('mobile')
        name = request.data.get('name', '').strip()
        age = request.data.get('age')
        address = request.data.get('address', '').strip()
        email = request.data.get('email', '').strip()
        password = request.data.get('password')

        if not mobile or len(mobile) != 10 or not mobile.isdigit():
            return Response(
                {"error": "Please provide a valid 10-digit mobile number containing only digits."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        import re
        if not name or not re.match(r"^[a-zA-Z\s.\'-]+$", name):
            return Response(
                {"error": "Please provide a valid name (letters, spaces, dots, and hyphens only)."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not age:
            return Response(
                {"error": "Age is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            age = int(age)
            if age <= 0 or age > 120:
                raise ValueError()
        except ValueError:
            return Response(
                {"error": "Please provide a valid age between 1 and 120."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not address or len(address) < 10:
            return Response(
                {"error": "Please provide a complete shipping address (minimum 10 characters)."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not email:
            return Response(
                {"error": "Email is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        from django.core.validators import validate_email
        from django.core.exceptions import ValidationError
        try:
            validate_email(email)
        except ValidationError:
            return Response(
                {"error": "Please provide a valid email address."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not password or len(password) < 12:
            return Response(
                {"error": "Password must be at least 12 characters long."},
                status=status.HTTP_400_BAD_REQUEST
            )

        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(not c.isalnum() for c in password)

        if not has_upper or not has_lower or not has_digit or not has_special:
            return Response(
                {"error": "Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(mobile=mobile).exists():
            return Response(
                {"error": "An account with this mobile number already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )

        age_value = request.data.get('age')
        age = None
        if age_value:
            try:
                age = int(age_value)
                if age <= 0:
                    raise ValueError()
            except ValueError:
                return Response(
                    {"error": "Please provide a valid age."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        user = cast(CustomUser, User.objects.create_user(  # type: ignore
            mobile=mobile,
            name=name,
            age=age,
            address=address,
            email=email,
            password=password
        ))
        token, _ = Token.objects.get_or_create(user=user)
        user_serializer = CustomUserSerializer(user)
        return Response({
            "token": token.key,
            "user": user_serializer.data,
            "message": "Account registered and authenticated successfully."
        }, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request):
        identifier = request.data.get('login') or request.data.get('email') or request.data.get('mobile')
        password = request.data.get('password')

        if not identifier:
            return Response(
                {"error": "Please provide your mobile number or email address."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not password:
            return Response(
                {"error": "Password is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = None
        if '@' in identifier:
            user = User.objects.filter(email__iexact=identifier).first()
            if not user:
                return Response(
                    {"error": "Account does not exist. Please register first."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            if len(identifier) != 10 or not identifier.isdigit():
                return Response(
                    {"error": "Please provide a valid 10-digit mobile number."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            try:
                user = User.objects.get(mobile=identifier)
            except User.DoesNotExist:
                return Response(
                    {"error": "Account does not exist. Please register first."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        if not user.has_usable_password():
            user.set_password(password)
            user.save()
        elif not user.check_password(password):
            return Response(
                {"error": "Invalid password."},
                status=status.HTTP_400_BAD_REQUEST
            )

        token, _ = Token.objects.get_or_create(user=user)
        user_serializer = CustomUserSerializer(user)
        return Response({
            "token": token.key,
            "user": user_serializer.data,
            "message": "Welcome back! Account authenticated successfully."
        }, status=status.HTTP_200_OK)

class RegisterLoginView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request):
        action = request.data.get('action')
        if action == 'register':
            return RegisterView().post(request)
        elif action == 'login':
            return LoginView().post(request)

        # Legacy fallback
        mobile = request.data.get('mobile')
        name = request.data.get('name', '').strip()

        if not mobile or len(mobile) != 10 or not mobile.isdigit():
            return Response(
                {"error": "Please provide a valid 10-digit mobile number."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user_obj, created = User.objects.get_or_create(mobile=mobile)
        user = cast(CustomUser, user_obj)
        
        if name and (created or not user.name):
            user.name = name
            user.save()
        elif created and not name:
            user.name = f"User #{mobile[6:]}"
        token, _ = Token.objects.get_or_create(user=user)
        user_serializer = CustomUserSerializer(user)
        return Response({
            "token": token.key,
            "user": user_serializer.data,
            "message": "Welcome back! Account authenticated successfully." if not created else "Account registered and authenticated successfully."
        }, status=status.HTTP_200_OK)

class LoginPageView(TemplateView):
    template_name = 'login.html'

class SignupPageView(TemplateView):
    template_name = 'signup.html'

class ProductPageView(TemplateView):
    template_name = 'products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        return context

class ProductListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class OrderCreateView(APIView):
    # Allow placing orders both as authenticated or guest users (but frontend enforces login)
    permission_classes = [permissions.AllowAny]

    @transaction.atomic
    def post(self, request):
        data = request.data
        customer_name = data.get('customer_name')
        customer_phone = data.get('customer_phone')
        customer_email = data.get('customer_email')
        shipping_address = data.get('shipping_address')
        amount = data.get('amount')
        payment_mode = data.get('payment_mode')
        referral_code = data.get('referral_code')
        est_delivery = data.get('est_delivery', '5 days')
        items_data = data.get('items', [])

        if not all([customer_name, customer_phone, customer_email, shipping_address, amount, payment_mode]):
            return Response(
                {"error": "Please provide all required shipping and order details."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not items_data:
            return Response(
                {"error": "Cart cannot be empty."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check token authentication to associate order if token header is present
        user = None
        if request.user and request.user.is_authenticated:
            user = request.user

        # Validate referral/coupon code if supplied
        is_code_applied = False
        if referral_code:
            if not user:
                return Response(
                    {"error": "Please log in to apply referral or coupon codes."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            is_valid, error_msg, referrer = validate_referral_coupon_code(referral_code, user)
            if not is_valid:
                return Response(
                    {"error": error_msg},
                    status=status.HTTP_400_BAD_REQUEST
                )
            is_code_applied = True

        # Calculate order totals from trusted product pricing
        subtotal = Decimal('0.00')
        payload_items = []

        for item in items_data:
            product_id = item.get('product_id')
            quantity = item.get('quantity', 1)
            customization = item.get('customization', {})

            product = get_object_or_404(Product, id=product_id)
            if product.id == 5:
                price = product.cart_price if product.cart_price else Decimal('1199.00')
            else:
                price = product.price
            subtotal += price * quantity

            payload_items.append({
                'product': product,
                'quantity': quantity,
                'price': price,
                'customization': customization
            })

        # Allow wallet balance to be used on checkout
        wallet_used = Decimal(str(data.get('wallet_used', '0') or '0'))
        if user and wallet_used > Decimal('0.00'):
            # Rule FR-06: Wallet cannot pay 100% of order. Minimum ₹50 paid via real payment method.
            max_wallet_allowed = max(Decimal('0.00'), subtotal - Decimal('50.00'))
            wallet_used = min(wallet_used, user.wallet_balance, max_wallet_allowed)
            user.wallet_balance -= wallet_used
            user.save(update_fields=['wallet_balance'])
        else:
            wallet_used = Decimal('0.00')

        final_amount = subtotal - wallet_used
        if final_amount < Decimal('0.00'):
            final_amount = Decimal('0.00')

        tracking_id = f"INK-{uuid.uuid4().hex[:12].upper()}"

        order = Order.objects.create(
            tracking_id=tracking_id,
            user=user,
            customer_name=customer_name,
            customer_phone=customer_phone,
            customer_email=customer_email,
            shipping_address=shipping_address,
            amount=final_amount,
            payment_mode=payment_mode,
            referral_code=referral_code.strip().upper() if is_code_applied else None,
            est_delivery=est_delivery,
            status='Placed'
        )

        # Log wallet payment/withdrawal transaction
        if user and wallet_used > Decimal('0.00'):
            WalletTransaction.objects.create(
                user=user,
                order=order,
                amount=-wallet_used,
                type='withdrawal',
                status='completed',
                note=f"Used ₹{wallet_used} from wallet to pay for order #{order.tracking_id}."
            )

        # Log referral code usage
        if is_code_applied:
            ReferralUsageLog.objects.create(
                referral_code=referral_code.strip().upper(),
                used_by=user,
                order=order,
                reward_status='pending'
            )

        # Create OrderItems
        for payload_item in payload_items:
            customization = payload_item['customization']
            OrderItem.objects.create(
                order=order,
                product=payload_item['product'],
                quantity=payload_item['quantity'],
                price=payload_item['price'],
                customization_type=customization.get('type', 'text'),
                customization_data=customization.get('data', ''),
                customization_font=customization.get('font'),
                customization_color=customization.get('color'),
                customization_size=customization.get('size'),
                customization_summary=customization.get('summary', '')
            )

        serializer = OrderSerializer(order)

        # Send notifications asynchronously to eliminate checkout latency
        transaction.on_commit(lambda: threading.Thread(
            target=send_order_notifications_bg,
            args=(order.id,),
            daemon=True
        ).start())


        response_data = serializer.data  # type: ignore
        if user:
            response_data['user'] = CustomUserSerializer(user).data  # type: ignore
            response_data['wallet_used'] = str(wallet_used)  # type: ignore

        return Response(response_data, status=status.HTTP_201_CREATED)

class WalletWithdrawView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        if user.wallet_balance < Decimal('500.00'):
            return Response(
                {"error": "Withdrawals are available once wallet balance reaches ₹500."},
                status=status.HTTP_400_BAD_REQUEST
            )

        account_number = request.data.get('account_number')
        account_holder_name = request.data.get('account_holder_name')
        bank_name = request.data.get('bank_name')
        ifsc_code = request.data.get('ifsc_code')

        if not all([account_number, account_holder_name, bank_name, ifsc_code]):
            return Response(
                {"error": "All bank details (account number, holder name, bank name, IFSC code) are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        account_number = str(account_number).strip()
        account_holder_name = str(account_holder_name).strip()
        bank_name = str(bank_name).strip()
        ifsc_code = str(ifsc_code).strip().upper()

        import re
        if not re.match(r"^\d{9,20}$", account_number):
            return Response(
                {"error": "Account number must be between 9 and 20 digits containing only digits."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not re.match(r"^[A-Z0-9]{11}$", ifsc_code):
            return Response(
                {"error": "IFSC code must be precisely 11 alphanumeric characters."},
                status=status.HTTP_400_BAD_REQUEST
            )

        withdrawn_amount = user.wallet_balance
        
        # Save withdrawal record in database
        withdrawal = WalletWithdrawal.objects.create(
            user=user,
            amount=withdrawn_amount,
            account_number=account_number,
            account_holder_name=account_holder_name,
            bank_name=bank_name,
            ifsc_code=ifsc_code
        )

        # Create WalletTransaction log
        WalletTransaction.objects.create(
            user=user,
            amount=-withdrawn_amount,
            type='withdrawal',
            status='completed',
            note=f"Bank withdrawal request to {bank_name} A/C ending ...{account_number[-4:] if len(account_number) >= 4 else account_number}."
        )

        user.wallet_balance = Decimal('0.00')
        user.save(update_fields=['wallet_balance'])

        # Send Telegram notification in background thread
        transaction.on_commit(lambda: threading.Thread(
            target=send_withdrawal_notifications_bg,
            args=(withdrawal.id,),
            daemon=True
        ).start())

        return Response({
            "message": f"₹{withdrawn_amount} has been withdrawn from your wallet.",
            "wallet_balance": str(user.wallet_balance)
        }, status=status.HTTP_200_OK)


class WalletTransactionsListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        txns = WalletTransaction.objects.filter(user=request.user).order_by('-created_at')
        serializer = WalletTransactionSerializer(txns, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class WalletBalanceView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({
            "wallet_balance": str(request.user.wallet_balance),
            "referral_code": request.user.referral_code
        }, status=status.HTTP_200_OK)


class OrderTrackView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, tracking_id):
        # Query order by tracking_id case-insensitively
        order = get_object_or_404(Order, tracking_id__iexact=tracking_id)
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserOrdersListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Fetch orders belonging to request.user, ordered by newest first
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ReferralCodeVerifyView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, code):
        user = request.user if request.user and request.user.is_authenticated else None
        is_valid, error_msg, referrer = validate_referral_coupon_code(code, user)
        if is_valid:
            ref_name = "Affiliate Partner"
            if referrer:
                ref_name = referrer.name or referrer.mobile
            return Response({"valid": True, "referrer": ref_name})
        else:
            return Response({"valid": False, "error": error_msg})

class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ClientErrorLogView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        import sys
        data = request.data
        print("!!! CLIENT ERROR LOG !!!", file=sys.stderr)
        print(f"Message: {data.get('message')}", file=sys.stderr)
        print(f"Source: {data.get('source')}:{data.get('lineno')}:{data.get('colno')}", file=sys.stderr)
        print(f"Stack trace: {data.get('stack')}", file=sys.stderr)
        print("------------------------", file=sys.stderr)
        sys.stderr.flush()
        return Response({"status": "logged"})


class ProductDesignListView(APIView):
    """
    GET /api/designs/?product_type=mug
    Returns all active ProductDesign entries for the given product type.
    If no product_type is provided, returns all active designs.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        product_type = request.query_params.get('product_type', '').strip().lower()
        qs = ProductDesign.objects.filter(is_active=True)
        if product_type:
            qs = qs.filter(product_type=product_type)
        serializer = ProductDesignSerializer(qs, many=True, context={'request': request})
        return Response(serializer.data)


class TrendingProductListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        qs = TrendingDesign.objects.filter(is_active=True)
        if not qs.exists():
            products = Product.objects.filter(is_trending=True)
            serializer = ProductSerializer(products, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = TrendingDesignSerializer(qs, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductDetailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductReviewListCreateView(APIView):
    """
    GET  /api/products/<product_id>/reviews/  - list reviews with stats
    POST /api/products/<product_id>/reviews/  - create a new review
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        reviews_qs = ProductReview.objects.filter(product=product).select_related('user')

        # Sorting
        sort = request.query_params.get('sort', 'most_recent')
        if sort == 'most_helpful':
            from django.db.models import Count
            reviews_qs = reviews_qs.annotate(h_count=Count('helpful_users')).order_by('-h_count', '-created_at')
        elif sort == 'highest_rated':
            reviews_qs = reviews_qs.order_by('-rating', '-created_at')
        elif sort == 'lowest_rated':
            reviews_qs = reviews_qs.order_by('rating', '-created_at')
        else:
            reviews_qs = reviews_qs.order_by('-created_at')

        # Filter by verified
        if request.query_params.get('verified') == 'true':
            reviews_qs = reviews_qs.filter(is_verified=True)

        # Rating filter (e.g., ?rating=5)
        rating_filter = request.query_params.get('rating')
        if rating_filter and rating_filter.isdigit():
            reviews_qs = reviews_qs.filter(rating=int(rating_filter))

        total = ProductReview.objects.filter(product=product).count()
        from django.db.models import Avg, Count
        avg_data = ProductReview.objects.filter(product=product).aggregate(avg=Avg('rating'))
        average_rating = round(avg_data['avg'], 1) if avg_data['avg'] else 0.0

        # Distribution breakdown
        distribution = {}
        for star in range(1, 6):
            count = ProductReview.objects.filter(product=product, rating=star).count()
            distribution[str(star)] = {
                'count': count,
                'percent': round((count / total * 100), 1) if total > 0 else 0
            }

        serializer = ProductReviewSerializer(reviews_qs, many=True, context={'request': request})
        return Response({
            'total': total,
            'average_rating': average_rating,
            'distribution': distribution,
            'reviews': serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request, product_id):
        # Must be authenticated
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        token_key = auth_header.replace('Token ', '').strip() if auth_header.startswith('Token ') else None
        if not token_key:
            return Response({'error': 'Authentication required to submit a review.'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            from rest_framework.authtoken.models import Token
            token_obj = Token.objects.select_related('user').get(key=token_key)
            reviewer = token_obj.user
        except Exception:
            return Response({'error': 'Invalid authentication token.'}, status=status.HTTP_401_UNAUTHORIZED)

        product = get_object_or_404(Product, pk=product_id)

        # Prevent duplicate reviews
        if ProductReview.objects.filter(product=product, user=reviewer).exists():
            return Response({'error': 'You have already reviewed this product.'}, status=status.HTTP_400_BAD_REQUEST)

        rating = request.data.get('rating')
        title = (request.data.get('title') or '').strip()
        comment = (request.data.get('comment') or '').strip()

        if not rating or not title or not comment:
            return Response({'error': 'Rating, title, and comment are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            rating = int(rating)
            if not (1 <= rating <= 5):
                raise ValueError
        except (ValueError, TypeError):
            return Response({'error': 'Rating must be a number between 1 and 5.'}, status=status.HTTP_400_BAD_REQUEST)

        # Determine if verified purchase
        is_verified = OrderItem.objects.filter(
            order__user=reviewer,
            product=product
        ).exists()

        review = ProductReview(
            product=product,
            user=reviewer,
            rating=rating,
            title=title,
            comment=comment,
            is_verified=is_verified
        )

        # Handle optional image upload
        if 'image' in request.FILES:
            review.image = request.FILES['image']

        review.save()
        serializer = ProductReviewSerializer(review, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReviewHelpfulToggleView(APIView):
    """
    POST /api/reviews/<review_id>/helpful/  - toggle helpful vote for authenticated user
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request, review_id):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        token_key = auth_header.replace('Token ', '').strip() if auth_header.startswith('Token ') else None
        if not token_key:
            return Response({'error': 'Authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            from rest_framework.authtoken.models import Token
            token_obj = Token.objects.select_related('user').get(key=token_key)
            voter = token_obj.user
        except Exception:
            return Response({'error': 'Invalid authentication token.'}, status=status.HTTP_401_UNAUTHORIZED)

        review = get_object_or_404(ProductReview, pk=review_id)

        if review.helpful_users.filter(id=voter.id).exists():
            review.helpful_users.remove(voter)
            marked = False
        else:
            review.helpful_users.add(voter)
            marked = True


        return Response({
            'helpful_count': review.helpful_users.count(),
            'has_marked_helpful': marked
        }, status=status.HTTP_200_OK)


# ─────────────────────────────────────────────
#  STAFF DASHBOARD — protected by IsAdminUser
# ─────────────────────────────────────────────

from django.contrib.auth.mixins import UserPassesTestMixin

class StaffDashboardPageView(UserPassesTestMixin, TemplateView):
    """Serves the custom staff dashboard HTML page."""
    template_name = 'staff_dashboard.html'
    login_url = '/admin/login/'

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff



class StaffStatsView(APIView):
    """GET /api/staff/stats/ — summary KPIs for the dashboard header cards."""
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        from django.db.models import Sum, Count
        total_orders   = Order.objects.count()
        total_revenue  = Order.objects.aggregate(s=Sum('amount'))['s'] or Decimal('0.00')
        total_customers = User.objects.filter(is_staff=False).count()
        pending_orders  = Order.objects.filter(status='Placed').count()
        return Response({
            'total_orders':    total_orders,
            'total_revenue':   str(total_revenue),
            'total_customers': total_customers,
            'pending_orders':  pending_orders,
        }, status=status.HTTP_200_OK)


class StaffOrdersView(APIView):
    """GET /api/staff/orders/ — full paginated order list for the staff table."""
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        orders = Order.objects.select_related('user').prefetch_related('items__product').order_by('-created_at')[:200]
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StaffOrderStatusUpdateView(APIView):
    """PATCH /api/staff/orders/<tracking_id>/status/ — update order status."""
    permission_classes = [permissions.IsAdminUser]

    def patch(self, request, tracking_id):
        order = get_object_or_404(Order, tracking_id__iexact=tracking_id)
        new_status = request.data.get('status', '').strip()
        valid = [s[0] for s in Order.STATUS_CHOICES]
        if new_status not in valid:
            return Response(
                {'error': f'Invalid status. Must be one of: {", ".join(valid)}.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        order.status = new_status
        order.save(update_fields=['status'])
        return Response({'tracking_id': tracking_id, 'status': new_status}, status=status.HTTP_200_OK)


class StaffCustomersView(APIView):
    """GET /api/staff/customers/ — list all non-staff users."""
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        customers = User.objects.filter(is_staff=False).order_by('-date_joined')[:500]
        serializer = CustomUserSerializer(customers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)






