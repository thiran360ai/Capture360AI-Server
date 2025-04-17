from rest_framework import serializers
from .models import *
from ecomapp.models import Customer 
from django.contrib.auth.hashers import make_password

from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from ecomapp.models import Customer  # Ensure you import the correct model

from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from ecomapp.models import Customer  # Import your custom user model

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        # fields = ['id', 'username', 'email', 'password', 'role']
        fields = "__all__"

    def validate_password(self, value):
        """Ensure password is hashed before saving"""
        return make_password(value)

    def create(self, validated_data):
        """Create user with hashed password"""
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["role"] = user.role  # Include user role in token
        return token



class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'

# class SubcategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Subcategory
#         fields = ["id", "name", "category", "image"]


# class SubcategorySerializer(serializers.ModelSerializer):
#     category = serializers.CharField(source='category.name', read_only=True)

#     class Meta:
#         model = Subcategory
#         fields = ["id", "name", "category", "image"]


# class SubcategorySerializer(serializers.ModelSerializer):
#     category_id = serializers.IntegerField(write_only=True)
#     category = serializers.CharField(source='category.name', read_only=True)
    

#     class Meta:
#         model = Subcategory
#         fields = ["id", "name", "category_id", "category", "image"]

# class SubcategorySerializer(serializers.ModelSerializer):
#     category = serializers.CharField(source='category.name', read_only=True)

#     class Meta:
#         model = Subcategory
#         fields = ["id", "name", "category", "image"]


# class SubcategorySerializer(serializers.ModelSerializer):
#     category_id = serializers.IntegerField(write_only=True)
#     category = serializers.CharField(source='category.name', read_only=True)
    

#     class Meta:
#         model = Subcategory
#         fields = ["id", "name", "category_id", "category", "image"]

class SubcategorySerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(write_only=True)
    category_id = serializers.IntegerField(write_only=True)
    category = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Subcategory
        fields = ["id", "name", "category_id", "category", "image"]

    def create(self, validated_data):
        # Pull category_id and replace it with the actual category object
        category_id = validated_data.pop('category_id')
        category = Category.objects.get(id=category_id)
        return Subcategory.objects.create(category=category, **validated_data)


        fields = ["id", "name", "category_id", "category", "image"]

    def create(self, validated_data):
        # Pull category_id and replace it with the actual category object
        category_id = validated_data.pop('category_id')
        category = Category.objects.get(id=category_id)
        return Subcategory.objects.create(category=category, **validated_data)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'image']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ['employee']  # Ensure employee can't be overwritten from client


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name', read_only=True)
    subcategory = serializers.CharField(source='subcategory.name', read_only=True)
    shop_name = serializers.CharField(source='shop.shop_name', read_only=True)  # Display only

    shop_id = serializers.PrimaryKeyRelatedField(
        source='shop', 
        queryset=Profile.objects.all(), 
        write_only=True  # Accept shop_id during POST
    )  

  

    class Meta:
        model = Product
        fields = [
            "id", "name", "brand", "description", "warranty", "return_policy",
            "is_active", "created_at", "updated_at",

            "shop_id",      # Required for POST
            "shop_name",    # Used in GET

            "category", "subcategory"
        ]
    
    def validate_shop_id(self, value):
        # Check if the shop ID corresponds to a valid Profile
        try:
            profile = Profile.objects.get(id=value.id)
            # Optionally, you can check if the shop is active or some other business logic
        except Profile.DoesNotExist:
            raise serializers.ValidationError("Invalid shop ID provided")
        return value


class ProductVariationSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = ProductVariation
        fields = ['id', 'variation_type', 'value', 'price', 'offer_price', 'stock', 'product', 'product_name']
        extra_kwargs = {
            'product': {'required': False},  # Auto-assigned
        }

    def create(self, validated_data):
        product = self.context['product']
        validated_data['product'] = product
        return super().create(validated_data)


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage  # ✅ Correct model
        fields = '__all__'

from rest_framework import serializers
from .models import (
    CartItem, Order, OrderItem, Wishlist, Review, Address, Payment,
    DeliveryPartner, OrderTracking, Notification
)


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)  # ✅ This retrieves related cart items

    class Meta:
        model = Cart  # ✅ Corrected model reference
        fields = ['id', 'user', 'items', 'created_at']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
        extra_kwargs = {
            'user': {'required': False}
        }



class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class DeliveryPartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryPartner
        fields = '__all__'


class OrderTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderTracking
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
