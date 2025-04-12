from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'

class AccessoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accessories
        fields = '__all__'

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'
        
# class WishSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Wish
#         fields = '__all__'
        
# class itemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Items
#         fields = '__all__'
from rest_framework import serializers
from .models import Items, Wish

class itemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = '__all__'  # This ensures all item fields are included

from rest_framework import serializers
from .models import Items, Wish

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = ['id', 'name', 'image', 'price', 'description', 'stock']  # Include necessary fields

class WishSerializer(serializers.ModelSerializer):
    item_details = ItemSerializer(source='item', read_only=True)  # Fetch item details

    class Meta:
        model = Wish
        fields = ['id', 'user', 'quantity', 'added_at', 'gst', 'shipping_charge', 'item_details']


class WishSerializer(serializers.ModelSerializer):
    item_details = itemSerializer(source='item', read_only=True)  # Fetch item details

    class Meta:
        model = Wish
        fields = ['id', 'user', 'item', 'quantity', 'added_at', 'gst', 'shipping_charge', 'item_details']


    def get_items(self, obj):
        items = obj.items.all()  # Adjust based on your model relationship
        return itemSerializer(items, many=True).data
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class contactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
        
        
# User = get_user_model()

# User Registration Serializer
# User Signup Serializer
# class UserSignupSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, min_length=6)
#     role = serializers.ChoiceField(choices=UserProfile.ROLE_CHOICES, default='user')

#     class Meta:
#         model = UserProfile
#         fields = ['id', 'username', 'email', 'password', 'role']

#     def create(self, validated_data):
#         role = validated_data.pop('role', 'user')  # Default role is "user"
#         user = UserProfile.objects.create_user(
#             username=validated_data['username'],
#             email=validated_data.get('email', ''),
#             password=validated_data['password'],
#             role=role
#         )

#         if role == 'admin':  # If admin is selected, set the permissions
#             user.is_staff = True
#             user.is_superuser = True
#             user.save()

#         return user
from .models import UserProfile  # Ensure you're importing this

from rest_framework import serializers
from .models import UserProfile

class UserSignupSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=UserProfile.ROLE_CHOICES, default='user')

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password', 'role']

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

# User Login Serializer
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])

        if not user:
            raise serializers.ValidationError("Invalid username or password")

        refresh = RefreshToken.for_user(user)

        return {
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,  # Return role in response
            },
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
        


# class OrderSerializer(serializers.ModelSerializer):
#     wishlist_items = serializers.PrimaryKeyRelatedField(many=True, queryset=Wish.objects.all(), write_only=True)
#     total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

#     class Meta:
#         model = Order
#         fields = ['id', 'user', 'wishlist_items', 'total_amount', 'order_status', 'created_at']

#     def create(self, validated_data):
#         wishlist_items = validated_data.pop('wishlist_items')
#         order = Order.objects.create(**validated_data)
#         order.wishlist_items.set(wishlist_items)  # Add wishlist items to order
#         order.save()
#         return order
from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
from rest_framework import serializers

class WishEmailSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    address = serializers.CharField(max_length=500)
