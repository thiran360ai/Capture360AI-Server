from django.contrib import admin
from .models import * 
from django.contrib.auth.admin import UserAdmin 
from import_export.admin import ImportExportModelAdmin
from import_export import resources

# Creating resource classes for import/export functionality
class UserProfileResource(resources.ModelResource):
    class Meta:
        model = UserProfile

class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category

class ProductsResource(resources.ModelResource):
    class Meta:
        model = Products

class AccessoriesResource(resources.ModelResource):
    class Meta:
        model = Accessories

class ItemsResource(resources.ModelResource):
    class Meta:
        model = Items

class BannerResource(resources.ModelResource):
    class Meta:
        model = Banner

class WishResource(resources.ModelResource):
    class Meta:
        model = Wish

# Admin configurations with import/export enabled
class UserProfileAdmin(ImportExportModelAdmin, UserAdmin):
    resource_class = UserProfileResource
    list_display = ("username", "email", "phone_number", "is_staff", "is_active")

class CategoryAdmin(ImportExportModelAdmin):
    resource_class = CategoryResource
    list_display = ("id", "image") 

class ProductsAdmin(ImportExportModelAdmin):
    resource_class = ProductsResource
    list_display = ("id", "name", "Category_reference", "image")

class AccessoriesAdmin(ImportExportModelAdmin):
    resource_class = AccessoriesResource
    list_display = ("id", "name", "Product_reference",)

class ItemsAdmin(ImportExportModelAdmin):
    resource_class = ItemsResource
    list_display = ("Accessories_reference","name", "image", "price", "description", "stock")

class BannerAdmin(ImportExportModelAdmin):
    resource_class = BannerResource
    list_display = ("id", "image")

# class WishAdmin(ImportExportModelAdmin):
#     resource_class = WishResource
#     list_display = ("id", "user", "item", "image", "name","price", "quantity", "added_at")
    
class CustomUserAdmin(UserAdmin):
    model = UserProfile
    list_display = ['username', 'email', 'role', 'is_staff', 'is_superuser']
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role', 'phone_number')}),
    )
from django.contrib import admin
from .models import Order, Wish

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_amount', 'order_status', 'created_at')  # Fields shown in list
    # list_filter = ('order_status', 'created_at')  # Filters in admin panel
    # search_fields = ('user__username', 'id')  # Search by username and order ID
    # ordering = ('-created_at',)  # Orders by newest first
    # filter_horizontal = ('wishlist_items',)  # Many-to-Many field for better UI

admin.site.register(Order, OrderAdmin)  # Register Order model
# admin.site.register(Wish)  # Register Wish model

# Avoid re-registering the model
if not admin.site.is_registered(UserProfile):
    admin.site.register(UserProfile, CustomUserAdmin)

# Registering models with admin
admin.site.register(Category, CategoryAdmin)
admin.site.register(Products, ProductsAdmin)
admin.site.register(Accessories, AccessoriesAdmin)
admin.site.register(Items, ItemsAdmin)
admin.site.register(Banner, BannerAdmin)
admin.site.register(Wish)