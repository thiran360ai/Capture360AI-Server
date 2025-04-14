from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Customer, Banner, Category, Subcategory, Profile, Product, ProductImage,
    ProductVariation, Cart, CartItem, Order, OrderItem, Wishlist,
    Review, Address, Payment, DeliveryPartner
)


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Customer

class CustomerAdmin(UserAdmin):
    model = Customer
    list_display = ('username', 'email', 'role', 'mobile_number', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active', 'is_staff')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('email', 'mobile_number', 'role', 'latitude', 'longitude', 'user_address')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'mobile_number', 'role', 'latitude', 'longitude', 'user_address'),
        }),
    )

    search_fields = ('username', 'email', 'mobile_number')
    ordering = ('username',)

admin.site.register(Customer, CustomerAdmin)


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'shopkeeper', 'prize_offer', 'start_date', 'end_date', 'is_active')
    search_fields = ('title', 'shopkeeper__username')
    list_filter = ('is_active', 'start_date', 'end_date')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    search_fields = ('name', 'category__name')
    list_filter = ('category',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('shop_name', 'employee', 'category', 'is_verified')
    search_fields = ('shop_name', 'employee__username')
    list_filter = ('category', 'is_verified')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'shop', 'category', 'is_active', 'created_at')
    search_fields = ('name', 'shop__shop_name')
    list_filter = ('category', 'is_active')


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product',)


@admin.register(ProductVariation)
class ProductVariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_type', 'value', 'price', 'offer_price', 'stock')
    list_filter = ('variation_type',)
    search_fields = ('product__name', 'value')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product_variation', 'quantity')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__email',)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product_variation', 'quantity', 'price')


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'created_at')
    list_filter = ('rating',)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'state', 'is_default')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'order', 'payment_method', 'amount', 'status', 'created_at')
    list_filter = ('payment_method', 'status')


@admin.register(DeliveryPartner)
class DeliveryPartnerAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'get_phone', 'vehicle_number', 'is_available')

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'

    def get_phone(self, obj):
        return obj.user.phone_number
    get_phone.short_description = 'Phone Number'
