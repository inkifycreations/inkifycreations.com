from rest_framework import serializers
from .models import CustomUser, Product, Order, OrderItem, ProductDesign

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['mobile', 'name', 'age', 'email', 'address', 'wallet_balance', 'referral_code']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'original_price', 'price', 'cart_price', 'image', 'description']

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

