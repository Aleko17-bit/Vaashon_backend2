from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, Order, CartItem, Payment

# -------------------
# Category Admin
# -------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


# -------------------
# Product Admin
# -------------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'get_category', 'price', 'image_tag', 'available', 'edit_link')
    list_filter = ('category', 'available')
    search_fields = ('name', 'description')
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width:50px; height:50px;" />', obj.image.url)
        return "-"
    image_tag.short_description = 'Image'

    def get_category(self, obj):
        return getattr(obj.category, "name", "-")
    get_category.short_description = "Category"

    def edit_link(self, obj):
        return format_html(
            '<a style="padding:2px 8px; background:#ffa500; color:#000; border-radius:4px;" href="/admin/shop/product/{}/change/">Edit</a>',
            obj.id
        )
    edit_link.short_description = 'Edit Product'


# -------------------
# Order Admin
# -------------------
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'get_user', 'product', 'size', 'quantity', 'address',
        'payment_method', 'paid', 'delivered', 'created_at'
    )
    list_filter = ('payment_method', 'paid', 'delivered', 'created_at')
    search_fields = ('product__name', 'user__username', 'address')
    readonly_fields = ('created_at',)

    def get_user(self, obj):
        return getattr(obj.user, "username", "-")
    get_user.short_description = "User"


# -------------------
# CartItem Admin
# -------------------
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_user', 'product', 'size', 'quantity', 'added_at')
    list_filter = ('added_at',)
    search_fields = ('product__name', 'user__username')
    readonly_fields = ('added_at',)

    def get_user(self, obj):
        return getattr(obj.user, "username", "-")
    get_user.short_description = "User"


# -------------------
# Payment Admin
# -------------------
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'get_user', 'amount', 'transaction_id', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('transaction_id', 'user__username')
    readonly_fields = ('created_at',)

    def get_user(self, obj):
        return getattr(obj.user, "username", "-")
    get_user.short_description = "User"
