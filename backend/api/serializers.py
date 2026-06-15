from rest_framework import serializers
from .models import CustomUser, Product, Order, OrderItem, ProductDesign, ProductReview, TrendingDesign

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['mobile', 'name', 'age', 'email', 'address', 'wallet_balance', 'referral_code', 'is_staff']

class ProductSerializer(serializers.ModelSerializer):
    trending_image_url = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'category', 'original_price', 'price', 'cart_price', 
            'image', 'description', 'is_trending', 'trending_tagline', 'trending_image_url',
            'average_rating', 'reviews_count'
        ]

    def get_trending_image_url(self, obj):
        request = self.context.get('request')
        if obj.trending_image and hasattr(obj.trending_image, 'url'):
            if request:
                return request.build_absolute_uri(obj.trending_image.url)
            return obj.trending_image.url
        return None

    def get_average_rating(self, obj):
        from django.db.models import Avg
        avg = ProductReview.objects.filter(product=obj).aggregate(Avg('rating'))['rating__avg']
        return round(avg, 1) if avg is not None else 0.0

    def get_reviews_count(self, obj):
        return ProductReview.objects.filter(product=obj).count()

class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    product_id = serializers.IntegerField(source='product.id', read_only=False)
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_image = serializers.CharField(source='product.image', read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            'id', 'product', 'product_id', 'product_name', 'product_image',
            'quantity', 'price', 'customization_type',
            'customization_data', 'customization_font',
            'customization_color', 'customization_size', 'customization_summary'
        ]
        extra_kwargs = {'product': {'write_only': True}}

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    status = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id', 'tracking_id', 'customer_name', 'customer_phone',
            'customer_email', 'shipping_address', 'amount',
            'payment_mode', 'referral_code', 'status',
            'created_at', 'est_delivery', 'items'
        ]

    def get_status(self, obj):
        # Return the dynamically simulated status
        return obj.get_simulated_status()


class ProductDesignSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    category_label = serializers.CharField(source='get_category_display', read_only=True)
    product_type_label = serializers.CharField(source='get_product_type_display', read_only=True)

    class Meta:
        model = ProductDesign
        fields = [
            'id', 'product_type', 'product_type_label',
            'name', 'category', 'category_label',
            'image_url', 'price', 'original_price', 'description',
        ]

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class ProductReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.name', read_only=True)
    user_mobile = serializers.SerializerMethodField()
    helpful_count = serializers.IntegerField(source='helpful_users.count', read_only=True)
    has_marked_helpful = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductReview
        fields = [
            'id', 'product', 'username', 'user_mobile', 'rating', 'title',
            'comment', 'image_url', 'is_verified', 'helpful_count',
            'has_marked_helpful', 'created_at'
        ]
        read_only_fields = ['id', 'username', 'user_mobile', 'is_verified', 'helpful_count', 'created_at']

    def get_user_mobile(self, obj):
        # Mask the mobile number for privacy (e.g. 98******12)
        mobile = obj.user.mobile
        if len(mobile) >= 10:
            return f"{mobile[:2]}******{mobile[-2:]}"
        return mobile

    def get_has_marked_helpful(self, obj):
        request = self.context.get('request')
        if request and request.user and request.user.is_authenticated:
            return obj.helpful_users.filter(id=request.user.id).exists()
        return False

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class TrendingDesignSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='product_id', allow_null=True, read_only=True)
    name = serializers.CharField(read_only=True)
    price = serializers.SerializerMethodField()
    trending_image_url = serializers.SerializerMethodField()
    trending_tagline = serializers.CharField(source='tagline', read_only=True)
    image = serializers.SerializerMethodField()
    description = serializers.CharField(source='tagline', read_only=True)
    average_rating = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()

    class Meta:
        model = TrendingDesign
        fields = [
            'id', 'name', 'price', 'trending_image_url', 'trending_tagline',
            'image', 'description', 'average_rating', 'reviews_count'
        ]

    def get_price(self, obj):
        return str(obj.price) if obj.price is not None else None

    def get_trending_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

    def get_image(self, obj):
        return self.get_trending_image_url(obj)

    def get_average_rating(self, obj):
        return 5.0

    def get_reviews_count(self, obj):
        return 0

