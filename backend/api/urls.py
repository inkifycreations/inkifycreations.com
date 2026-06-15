from django.urls import path
from .views import RegisterView, LoginView, RegisterLoginView, ProductListView, OrderCreateView, OrderTrackView, UserOrdersListView, WalletWithdrawView, ReferralCodeVerifyView, UserProfileView, ClientErrorLogView, ProductDesignListView, TrendingProductListView, ProductDetailView, ProductReviewListCreateView, ReviewHelpfulToggleView, StaffDashboardPageView, StaffStatsView, StaffOrdersView, StaffOrderStatusUpdateView, StaffCustomersView, WalletTransactionsListView, WalletBalanceView

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='auth_register'),
    path('auth/login/', LoginView.as_view(), name='auth_login'),
    path('auth/register-login/', RegisterLoginView.as_view(), name='register_login'),
    path('products/', ProductListView.as_view(), name='products_list'),
    path('orders/', OrderCreateView.as_view(), name='order_create'),
    path('orders/track/<str:tracking_id>/', OrderTrackView.as_view(), name='order_track'),
    path('orders/my/', UserOrdersListView.as_view(), name='user_orders'),
    path('wallet/withdraw/', WalletWithdrawView.as_view(), name='wallet_withdraw'),
    path('wallet/transactions/', WalletTransactionsListView.as_view(), name='wallet_transactions'),
    path('wallet/balance/', WalletBalanceView.as_view(), name='wallet_balance'),
    path('referrals/verify/<str:code>/', ReferralCodeVerifyView.as_view(), name='referral_verify'),
    path('user/profile/', UserProfileView.as_view(), name='user_profile'),
    path('log-error/', ClientErrorLogView.as_view(), name='client_error_log'),
    path('designs/', ProductDesignListView.as_view(), name='designs_list'),
    path('trending-products/', TrendingProductListView.as_view(), name='trending_products_list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/<int:product_id>/reviews/', ProductReviewListCreateView.as_view(), name='product_reviews'),
    path('reviews/<int:review_id>/helpful/', ReviewHelpfulToggleView.as_view(), name='review_helpful_toggle'),
    # Staff dashboard API endpoints (nested under api/)
    path('staff/stats/', StaffStatsView.as_view(), name='staff_stats'),
    path('staff/orders/', StaffOrdersView.as_view(), name='staff_orders'),
    path('staff/orders/<str:tracking_id>/status/', StaffOrderStatusUpdateView.as_view(), name='staff_order_status'),
    path('staff/customers/', StaffCustomersView.as_view(), name='staff_customers'),
]



