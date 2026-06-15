from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from api.models import Product, Order, OrderItem, WalletWithdrawal, TrendingDesign
from unittest.mock import patch


User = get_user_model()

class InkifyAPITests(APITestCase):
    def setUp(self):
        # Create a test product matching standard catalog
        self.product = Product.objects.create(
            id=1,
            name="Premium T-Shirt",
            category="Apparel",
            original_price=500.00,
            price=399.00,
            image="assets/tshirt.png",
            description="Ultra-soft 220 GSM combed cotton.",
            is_trending=True
        )
        self.set_product = Product.objects.create(
            id=5,
            name="The Purple Gifting Set",
            category="Signature Bundle",
            original_price=1500.00,
            price=999.00,
            cart_price=1199.00,
            image="assets/gift_box.png",
            description="Premium velvet-feel signature gift box containing full set."
        )
        self.mobile = "9876543210"
        self.name = "Test User"

    def test_register_login(self):
        url = reverse('register_login')
        data = {
            "mobile": self.mobile,
            "name": self.name
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        self.assertIn("user", response.data)
        self.assertEqual(response.data["user"]["mobile"], self.mobile)
        self.assertEqual(response.data["user"]["name"], self.name)

    def test_get_products(self):
        url = reverse('products_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["name"], "Premium T-Shirt")

    def test_place_and_track_order(self):
        # Authenticate first
        auth_url = reverse('register_login')
        auth_data = {"mobile": self.mobile, "name": self.name}
        auth_response = self.client.post(auth_url, auth_data, format='json')
        token = auth_response.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        # Place Order
        order_url = reverse('order_create')
        order_payload = {
            "customer_name": self.name,
            "customer_phone": self.mobile,
            "customer_email": "test@example.com",
            "shipping_address": "123 Test St, Test City - 110001",
            "amount": 399.00,
            "payment_mode": "Cash on Delivery",
            "est_delivery": "30th May 2026",
            "items": [
                {
                    "product_id": self.product.id,
                    "quantity": 1,
                    "price": 399.00,
                    "customization": {
                        "type": "text",
                        "data": "Vibe Test",
                        "font": "sans-serif",
                        "color": "Light Blue",
                        "size": "L",
                        "summary": "Custom Text: \"Vibe Test\""
                    }
                }
            ]
        }
        response = self.client.post(order_url, order_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("tracking_id", response.data)
        tracking_id = response.data["tracking_id"]

        # Track Order
        track_url = reverse('order_track', kwargs={"tracking_id": tracking_id})
        track_response = self.client.get(track_url)
        self.assertEqual(track_response.status_code, status.HTTP_200_OK)
        self.assertEqual(track_response.data["tracking_id"], tracking_id)
        self.assertEqual(track_response.data["status"], "Placed")
        self.assertEqual(len(track_response.data["items"]), 1)
        self.assertEqual(track_response.data["items"][0]["product_name"], "Premium T-Shirt")
        self.assertEqual(track_response.data["items"][0]["customization_color"], "Light Blue")
        self.assertEqual(track_response.data["items"][0]["customization_size"], "L")

    def test_get_user_orders_authenticated(self):
        # Authenticate first
        auth_url = reverse('register_login')
        auth_data = {"mobile": self.mobile, "name": self.name}
        auth_response = self.client.post(auth_url, auth_data, format='json')
        token = auth_response.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        # Place Order
        order_url = reverse('order_create')
        order_payload = {
            "customer_name": self.name,
            "customer_phone": self.mobile,
            "customer_email": "test@example.com",
            "shipping_address": "123 Test St, Test City - 110001",
            "amount": 399.00,
            "payment_mode": "Cash on Delivery",
            "est_delivery": "30th May 2026",
            "items": [
                {
                    "product_id": self.product.id,
                    "quantity": 1,
                    "price": 399.00,
                    "customization": {
                        "type": "text",
                        "data": "Vibe Test",
                        "font": "sans-serif",
                        "summary": "Custom Text: \"Vibe Test\""
                    }
                }
            ]
        }
        self.client.post(order_url, order_payload, format='json')

        # Get my orders
        my_orders_url = reverse('user_orders')
        response = self.client.get(my_orders_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["customer_phone"], self.mobile)

    def test_get_user_orders_unauthenticated(self):
        my_orders_url = reverse('user_orders')
        response = self.client.get(my_orders_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_referral_code_generation_and_wallet_credits(self):
        # Alice registers and places a first order
        first_user_mobile = '9111111111'
        first_user_name = 'Alice'

        auth_url = reverse('register_login')
        response = self.client.post(auth_url, {'mobile': first_user_mobile, 'name': first_user_name}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        first_token = response.data['token']

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + first_token)
        order_url = reverse('order_create')
        order_payload = {
            'customer_name': first_user_name,
            'customer_phone': first_user_mobile,
            'customer_email': 'alice@example.com',
            'shipping_address': '1 Referral Lane, City - 110001',
            'amount': 399.00,
            'payment_mode': 'Cash on Delivery',
            'est_delivery': '30th May 2026',
            'items': [
                {
                    'product_id': self.product.id,
                    'quantity': 1,
                    'price': 399.00,
                    'customization': {
                        'type': 'text',
                        'data': 'Alice Design',
                        'font': 'sans-serif',
                        'summary': 'Custom Text'
                    }
                }
            ]
        }
        order_response = self.client.post(order_url, order_payload, format='json')
        self.assertEqual(order_response.status_code, status.HTTP_201_CREATED)
        
        # Verify Alice does not have a referral code yet (order placed, not completed)
        alice = User.objects.get(mobile=first_user_mobile)
        self.assertIsNone(alice.referral_code)
        
        # Transition Alice's order to Completed
        first_order = Order.objects.get(tracking_id=order_response.data['tracking_id'])
        first_order.status = "Completed"
        first_order.save()
        
        # Verify Alice now has a referral code generated, and wallet is 0 (she didn't use any code)
        alice.refresh_from_db()
        self.assertIsNotNone(alice.referral_code)
        self.assertEqual(alice.wallet_balance, Decimal('0.00'))
        
        alice_referral_code = alice.referral_code

        # Bob registers and wants to use Alice's referral code
        second_user_mobile = '9222222222'
        second_user_name = 'Bob'

        self.client.credentials()  # clear auth
        response = self.client.post(auth_url, {'mobile': second_user_mobile, 'name': second_user_name}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        second_token = response.data['token']

        # Bob tries to apply Alice's code
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + second_token)
        referral_order_payload = {
            'customer_name': second_user_name,
            'customer_phone': second_user_mobile,
            'customer_email': 'bob@example.com',
            'shipping_address': '2 Affiliate Road, City - 110001',
            'amount': 399.00,
            'payment_mode': 'Cash on Delivery',
            'est_delivery': '30th May 2026',
            'referral_code': alice_referral_code,
            'items': [
                {
                    'product_id': self.product.id,
                    'quantity': 1,
                    'price': 399.00,
                    'customization': {
                        'type': 'text',
                        'data': 'Bob Design',
                        'font': 'sans-serif',
                        'summary': 'Custom Text'
                    }
                }
            ]
        }
        referral_response = self.client.post(order_url, referral_order_payload, format='json')
        self.assertEqual(referral_response.status_code, status.HTTP_201_CREATED)
        # Verify direct discount of ₹10 is applied
        self.assertEqual(Decimal(referral_response.data['amount']), Decimal('389.00'))
        
        # Verify wallet balances are still 0 (order is not yet completed)
        bob = User.objects.get(mobile=second_user_mobile)
        self.assertEqual(bob.wallet_balance, Decimal('0.00'))
        alice.refresh_from_db()
        self.assertEqual(alice.wallet_balance, Decimal('0.00'))

        # Complete Bob's order
        bob_order = Order.objects.get(tracking_id=referral_response.data['tracking_id'])
        bob_order.status = "Completed"
        bob_order.save()

        # Both Alice and Bob should get ₹10 cashback
        bob.refresh_from_db()
        self.assertEqual(bob.wallet_balance, Decimal('10.00'))
        alice.refresh_from_db()
        self.assertEqual(alice.wallet_balance, Decimal('10.00'))

        # Now cancel Bob's order: verify reversal of rewards
        bob_order.status = "Cancelled"
        bob_order.save()

        bob.refresh_from_db()
        self.assertEqual(bob.wallet_balance, Decimal('0.00'))
        alice.refresh_from_db()
        self.assertEqual(alice.wallet_balance, Decimal('0.00'))

    def test_self_referral_check(self):
        # Alice registers and places order to activate her code
        first_user_mobile = '9111111111'
        auth_url = reverse('register_login')
        response = self.client.post(auth_url, {'mobile': first_user_mobile, 'name': 'Alice'}, format='json')
        token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        
        alice = User.objects.get(mobile=first_user_mobile)
        alice.referral_code = "ALICE12345"
        alice.save()
        
        # Alice tries to use her own referral code
        order_url = reverse('order_create')
        order_payload = {
            'customer_name': 'Alice',
            'customer_phone': first_user_mobile,
            'customer_email': 'alice@example.com',
            'shipping_address': '1 Referral Lane, City',
            'amount': 399.00,
            'payment_mode': 'Cash on Delivery',
            'referral_code': 'ALICE12345',
            'items': [{'product_id': self.product.id, 'quantity': 1, 'price': 399.00, 'customization': {'type':'text','data':'Alice','summary':'Test'}}]
        }
        res = self.client.post(order_url, order_payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("own referral code", res.data["error"])

    def test_min_payment_amount_wallet_use(self):
        # Authenticate first
        auth_url = reverse('register_login')
        auth_response = self.client.post(auth_url, {'mobile': self.mobile, 'name': self.name}, format='json')
        token = auth_response.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        # Set user wallet balance to 100
        user = User.objects.get(mobile=self.mobile)
        user.wallet_balance = Decimal('100.00')
        user.save()

        # Place order for 399, trying to use 100 wallet balance (grand total 299, min cash payment is 50, which is satisfied)
        order_url = reverse('order_create')
        order_payload = {
            'customer_name': self.name,
            'customer_phone': self.mobile,
            'customer_email': 'test@example.com',
            'shipping_address': '123 Test St, Test City',
            'amount': 399.00,
            'payment_mode': 'Cash on Delivery',
            'wallet_used': '100.00',
            'items': [{'product_id': self.product.id, 'quantity': 1, 'price': 399.00, 'customization': {'type':'text','data':'Test','summary':'Test'}}]
        }
        res1 = self.client.post(order_url, order_payload, format='json')
        self.assertEqual(res1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Decimal(res1.data['amount']), Decimal('299.00'))
        user.refresh_from_db()
        self.assertEqual(user.wallet_balance, Decimal('0.00'))

        # Set user wallet balance to 100 again
        user.wallet_balance = Decimal('100.00')
        user.save()

        # Try to pay for a 70 product using 60 wallet balance (so grand total is 10, but min cash payment is 50, so max wallet allowed is 20)
        product_70 = Product.objects.create(id=22, name="Small Item", category="Test", original_price=70, price=70, image="test.png", description="test")
        order_payload_clamped = {
            'customer_name': self.name,
            'customer_phone': self.mobile,
            'customer_email': 'test@example.com',
            'shipping_address': '123 Test St, Test City',
            'amount': 70.00,
            'payment_mode': 'Cash on Delivery',
            'wallet_used': '60.00',
            'items': [{'product_id': product_70.id, 'quantity': 1, 'price': 70.00, 'customization': {'type':'text','data':'Test','summary':'Test'}}]
        }
        res2 = self.client.post(order_url, order_payload_clamped, format='json')
        self.assertEqual(res2.status_code, status.HTTP_201_CREATED)
        # Should be clamped to pay exactly 50 in cash (70 - 20 wallet)
        self.assertEqual(Decimal(res2.data['amount']), Decimal('50.00'))
        user.refresh_from_db()
        # Used 20, remaining 80
        self.assertEqual(user.wallet_balance, Decimal('80.00'))

    def test_user_profile_endpoint(self):
        # Unauthenticated request should be blocked
        profile_url = reverse('user_profile')
        response = self.client.get(profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authenticate first
        auth_url = reverse('register_login')
        auth_data = {"mobile": self.mobile, "name": self.name}
        auth_response = self.client.post(auth_url, auth_data, format='json')
        token = auth_response.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        # Manually assign referral code since registration/login no longer generates one
        user = User.objects.get(mobile=self.mobile)
        from api.models import generate_referral_code
        user.referral_code = generate_referral_code()
        user.save()

        # Authenticated request should succeed and return referral code and balance
        response = self.client.get(profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["mobile"], self.mobile)
        self.assertEqual(response.data["name"], self.name)
        self.assertIsNotNone(response.data["referral_code"])
        self.assertEqual(len(response.data["referral_code"]), 10)

    @patch('urllib.request.urlopen')
    def test_order_notifications(self, mock_urlopen):
        from django.core import mail
        import json
        
        # Place Order
        order_url = reverse('order_create')
        order_payload = {
            "customer_name": "Notify Customer",
            "customer_phone": "9999999999",
            "customer_email": "customer@example.com",
            "shipping_address": "456 Notification St, Test City",
            "amount": 399.00,
            "payment_mode": "UPI Payment",
            "est_delivery": "5 days",
            "items": [
                {
                    "product_id": self.product.id,
                    "quantity": 2,
                    "price": 399.00,
                    "customization": {
                        "type": "text",
                        "data": "Double Custom",
                        "summary": "Custom Text: \"Double Custom\""
                    }
                }
            ]
        }
        
        # Mock threading.Thread to run synchronously inside the same transaction
        class SyncThread:
            def __init__(self, target, args=(), kwargs={}, daemon=True):
                self.target = target
                self.args = args
                self.kwargs = kwargs
            def start(self):
                self.target(*self.args, **self.kwargs)

        with patch('threading.Thread', SyncThread):
            with self.captureOnCommitCallbacks(execute=True):
                response = self.client.post(order_url, order_payload, format='json')
                self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify email is sent to admin and customer
        self.assertEqual(len(mail.outbox), 1)
        sent_email = mail.outbox[0]
        self.assertIn("jayaprakashporapu84@gmail.com", sent_email.to)
        self.assertIn("customer@example.com", sent_email.to)
        self.assertIn("Order Confirmation", sent_email.alternatives[0][0])
        self.assertIn("Notify Customer", sent_email.alternatives[0][0])
        self.assertIn("Premium T-Shirt", sent_email.alternatives[0][0])
        self.assertIn("Double Custom", sent_email.alternatives[0][0])

        # Verify urllib.request.urlopen was called for Telegram Bot API
        self.assertTrue(mock_urlopen.called)
        called_args, called_kwargs = mock_urlopen.call_args
        req = called_args[0]
        self.assertEqual(req.full_url, "https://api.telegram.org/bot8136363344:AAGd58z4mMC0mifFh-agrGofVqtzWcsbPwQ/sendMessage")
        self.assertEqual(req.get_header("Content-type"), "application/json")
        
        # Verify request body contains required elements
        req_body = json.loads(req.data.decode('utf-8'))
        self.assertEqual(req_body["chat_id"], "5531966096")
        self.assertIn("Notify Customer", req_body["text"])
        self.assertIn("Double Custom", req_body["text"])

    def test_registration_input_validations(self):
        url = reverse('register_login')
        
        # 1. Invalid Mobile
        data = {
            "action": "register",
            "mobile": "12345a7890", # non-digit
            "name": "Mukesh Kumar",
            "age": 25,
            "email": "mukesh@example.com",
            "address": "123 Main St, City",
            "password": "SecurePassword123!"
        }
        res = self.client.post(url, data, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("mobile number containing only digits", res.data["error"])

        # 2. Invalid Name
        data["mobile"] = "9876543210"
        data["name"] = "Mukesh123" # invalid characters
        res = self.client.post(url, data, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("letters, spaces, dots, and hyphens only", res.data["error"])

        # 3. Invalid Age
        data["name"] = "Mukesh Kumar"
        data["age"] = -5
        res = self.client.post(url, data, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("age between 1 and 120", res.data["error"])

        # 4. Invalid Email
        data["age"] = 25
        data["email"] = "invalidemail"
        res = self.client.post(url, data, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("valid email address", res.data["error"])

        # 5. Invalid Address (too short)
        data["email"] = "mukesh@example.com"
        data["address"] = "Short"
        res = self.client.post(url, data, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("complete shipping address", res.data["error"])

        # 6. Invalid Password (missing special character)
        data["address"] = "123 Main St, City"
        data["password"] = "SecurePassword123"
        res = self.client.post(url, data, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("special character", res.data["error"])

    def test_wallet_withdrawal(self):
        # Authenticate first
        auth_url = reverse('register_login')
        auth_data = {"mobile": self.mobile, "name": self.name}
        auth_response = self.client.post(auth_url, auth_data, format='json')
        token = auth_response.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        withdraw_url = reverse('wallet_withdraw')

        # 1. Withdraw with 0 balance (limit is 500)
        res = self.client.post(withdraw_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("reaches ₹500", res.data["error"])

        # Set balance to 500
        user = User.objects.get(mobile=self.mobile)
        user.wallet_balance = Decimal('500.00')
        user.save()

        # 2. Withdraw with missing bank details
        res_missing = self.client.post(withdraw_url, {}, format='json')
        self.assertEqual(res_missing.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("required", res_missing.data["error"])

        # 3. Withdraw with invalid account number (e.g. alphanumeric)
        invalid_data_1 = {
            "account_number": "1234abc789",
            "account_holder_name": "Test User",
            "bank_name": "Test Bank",
            "ifsc_code": "ABCD0123456"
        }
        res_invalid_1 = self.client.post(withdraw_url, invalid_data_1, format='json')
        self.assertEqual(res_invalid_1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("digits", res_invalid_1.data["error"])

        # 4. Withdraw with invalid IFSC code (e.g. wrong length)
        invalid_data_2 = {
            "account_number": "1234567890",
            "account_holder_name": "Test User",
            "bank_name": "Test Bank",
            "ifsc_code": "ABCD0"
        }
        res_invalid_2 = self.client.post(withdraw_url, invalid_data_2, format='json')
        self.assertEqual(res_invalid_2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("alphanumeric", res_invalid_2.data["error"])

        # 5. Withdraw with valid details
        valid_data = {
            "account_number": "123456789012",
            "account_holder_name": "Test User",
            "bank_name": "Test Bank",
            "ifsc_code": "ABCD0123456"
        }
        res_ok = self.client.post(withdraw_url, valid_data, format='json')
        self.assertEqual(res_ok.status_code, status.HTTP_200_OK)
        self.assertIn("withdrawn", res_ok.data["message"])

        # Verify balance reset
        user.refresh_from_db()
        self.assertEqual(user.wallet_balance, Decimal('0.00'))

        # Verify database record exists
        withdrawal = WalletWithdrawal.objects.filter(user=user).first()
        self.assertIsNotNone(withdrawal)
        self.assertEqual(withdrawal.amount, Decimal('500.00'))
        self.assertEqual(withdrawal.account_number, "123456789012")
        self.assertEqual(withdrawal.account_holder_name, "Test User")
        self.assertEqual(withdrawal.bank_name, "Test Bank")
        self.assertEqual(withdrawal.ifsc_code, "ABCD0123456")


    def test_trending_designs_api(self):
        # 1. Access the API when there are no TrendingDesign instances in DB.
        # It should fall back to Product.objects.filter(is_trending=True) or first 4 products
        url = reverse('trending_products_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should return our test product
        self.assertTrue(len(response.data) > 0)
        self.assertEqual(response.data[0]['id'], self.product.id)

        # 2. Create a TrendingDesign instance in the database
        from django.core.files.uploadedfile import SimpleUploadedFile
        test_image = SimpleUploadedFile(
            name='test_trending.png',
            content=b'testimagecontent',
            content_type='image/png'
        )
        trending_design = TrendingDesign.objects.create(
            product_id=self.product.id,
            name="Exclusive Trending Art",
            tagline="Limited Edition Blueprint",
            image=test_image,
            sort_order=1,
            is_active=True
        )

        # 3. Access the API again. It should now return the custom TrendingDesign serialized fields.
        response2 = self.client.get(url)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response2.data), 1)
        self.assertEqual(response2.data[0]['id'], self.product.id)
        self.assertEqual(response2.data[0]['name'], "Exclusive Trending Art")
        self.assertEqual(response2.data[0]['trending_tagline'], "Limited Edition Blueprint")
        self.assertIn("test_trending", response2.data[0]['trending_image_url'])

    def test_gifting_set_referral_reward_and_discount(self):
        # Alice registers and places a first order to activate her code
        first_user_mobile = '9333333333'
        first_user_name = 'Alice'

        auth_url = reverse('register_login')
        response = self.client.post(auth_url, {'mobile': first_user_mobile, 'name': first_user_name}, format='json')
        first_token = response.data['token']

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + first_token)
        order_url = reverse('order_create')
        order_payload = {
            'customer_name': first_user_name,
            'customer_phone': first_user_mobile,
            'customer_email': 'alice@example.com',
            'shipping_address': '1 Referral Lane, City',
            'amount': 399.00,
            'payment_mode': 'Cash on Delivery',
            'items': [
                {
                    'product_id': self.product.id,
                    'quantity': 1,
                    'price': 399.00,
                    'customization': {
                        'type': 'text',
                        'data': 'Alice Design',
                        'summary': 'Custom Text'
                    }
                }
            ]
        }
        order_response = self.client.post(order_url, order_payload, format='json')
        
        # Transition Alice's order to Completed
        first_order = Order.objects.get(tracking_id=order_response.data['tracking_id'])
        first_order.status = "Completed"
        first_order.save()
        
        alice = User.objects.get(mobile=first_user_mobile)
        alice_referral_code = alice.referral_code

        # Bob registers and applies Alice's referral code with the Signature Gifting Set (ID 5) in cart
        second_user_mobile = '9444444444'
        second_user_name = 'Bob'

        self.client.credentials()  # clear auth
        response = self.client.post(auth_url, {'mobile': second_user_mobile, 'name': second_user_name}, format='json')
        second_token = response.data['token']

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + second_token)
        referral_order_payload = {
            'customer_name': second_user_name,
            'customer_phone': second_user_mobile,
            'customer_email': 'bob@example.com',
            'shipping_address': '2 Affiliate Road, City',
            'amount': 1199.00,
            'payment_mode': 'Cash on Delivery',
            'referral_code': alice_referral_code,
            'items': [
                {
                    'product_id': self.set_product.id, # Purple Gifting Set (ID 5)
                    'quantity': 1,
                    'price': 1199.00,
                    'customization': {
                        'type': 'text',
                        'data': 'Bob Design',
                        'summary': 'Custom Text'
                    }
                }
            ]
        }
        referral_response = self.client.post(order_url, referral_order_payload, format='json')
        self.assertEqual(referral_response.status_code, status.HTTP_201_CREATED)
        
        # Verify direct discount of ₹50 is applied immediately to Bob's order amount
        # Subtotal: 1199.00 - 50.00 discount = 1149.00
        self.assertEqual(Decimal(referral_response.data['amount']), Decimal('1149.00'))

        # Complete Bob's order
        bob_order = Order.objects.get(tracking_id=referral_response.data['tracking_id'])
        bob_order.status = "Completed"
        bob_order.save()

        # Both Alice and Bob should receive ₹50 cashback (due to Gifting Set)
        bob = User.objects.get(mobile=second_user_mobile)
        bob.refresh_from_db()
        self.assertEqual(bob.wallet_balance, Decimal('50.00'))
        
        alice.refresh_from_db()
        self.assertEqual(alice.wallet_balance, Decimal('50.00'))

        # Cancel Bob's order: verify reversal of ₹50 rewards
        bob_order.status = "Cancelled"
        bob_order.save()

        bob.refresh_from_db()
        self.assertEqual(bob.wallet_balance, Decimal('0.00'))
        
        alice.refresh_from_db()
        self.assertEqual(alice.wallet_balance, Decimal('0.00'))



