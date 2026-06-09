from django.urls import path
from .views import RegisterView, LoginView, RegisterLoginView, ProductListView, OrderCreateView, OrderTrackView, UserOrdersListView, WalletWithdrawView, ReferralCodeVerifyView, UserProfileView, ClientErrorLogView, ProductDesignListView

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='auth_register'),
    path('auth/login/', LoginView.as_view(), name='auth_login'),
    path('auth/register-login/', RegisterLoginView.as_view(), name='register_login'),
    path('products/', ProductListView.as_view(), name='products_list'),
    path('orders/', OrderCreateView.as_view(), name='order_create'),
    path('orders/track/<str:tracking_id>/', OrderTrackView.as_view(), name='order_track'),
    path('orders/my/', UserOrdersListView.as_view(), name='user_orders'),
    path('wallet/withdraw/', WalletWithdrawView.as_view(), name='wallet_withdraw'),
    path('referrals/verify/<str:code>/', ReferralCodeVerifyView.as_view(), name='referral_verify'),
    path('user/profile/', UserProfileView.as_view(), name='user_profile'),
    path('log-error/', ClientErrorLogView.as_view(), name='client_error_log'),
    path('designs/', ProductDesignListView.as_view(), name='designs_list'),
]


