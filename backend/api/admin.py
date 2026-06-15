from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.html import format_html
from .models import CustomUser, Product, Order, OrderItem, ProductDesign, TrendingDesign

@admin.register(CustomUser)
class CustomUserAdmin(DjangoUserAdmin):
    model = CustomUser
    list_display = ('mobile', 'name', 'email', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('mobile', 'name', 'email')
    ordering = ('mobile',)
    fieldsets = (
        (None, {'fields': ('mobile', 'password')}),
        ('Personal info', {'fields': ('name', 'email', 'age', 'address')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('mobile', 'name', 'password1', 'password2'),
        }),
    )
    filter_horizontal = ('groups', 'user_permissions')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'original_price')
    search_fields = ('name', 'category')
    list_filter = ('category',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('tracking_id', 'customer_name', 'customer_phone', 'status', 'amount', 'created_at')
    search_fields = ('tracking_id', 'customer_name', 'customer_phone')
    list_filter = ('status', 'created_at')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')
    search_fields = ('order__tracking_id', 'product__name')


@admin.register(ProductDesign)
class ProductDesignAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_type', 'category', 'price', 'sort_order', 'is_active', 'image_preview')
    list_filter = ('product_type', 'category', 'is_active')
    search_fields = ('name', 'description')
    list_editable = ('sort_order', 'is_active')
    ordering = ('product_type', 'sort_order', 'name')

    fieldsets = (
        ('Design Info', {
            'fields': ('product_type', 'name', 'category', 'description')
        }),
        ('Image', {
            'fields': ('image',),
            'description': 'Upload a high-quality wrap/print design image (PNG recommended, min 800px wide).'
        }),
        ('Pricing', {
            'fields': ('price', 'original_price'),
        }),
        ('Display', {
            'fields': ('sort_order', 'is_active'),
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:50px; border-radius:4px; object-fit:cover;" />',
                obj.image.url
            )
        return '—'
    image_preview.short_description = 'Preview'  # type: ignore


@admin.register(TrendingDesign)
class TrendingDesignAdmin(admin.ModelAdmin):
    list_display = ('name', 'tagline', 'price', 'original_price', 'product_id', 'sort_order', 'is_active', 'image_preview')
    list_filter = ('is_active',)
    search_fields = ('name', 'tagline')
    list_editable = ('sort_order', 'is_active')
    ordering = ('sort_order', '-created_at')

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:50px; border-radius:4px; object-fit:cover;" />',
                obj.image.url
            )
        return '—'
    image_preview.short_description = 'Preview'  # type: ignore

