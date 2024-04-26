# from rest_framework import serializers
# from .models import CustomUser

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ['id', 'username', 'password', 'name', 'email', 'role', 'location']
#         extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         user = CustomUser.objects.create_user(**validated_data)
#         return user

# from rest_framework import serializers
# from .models import CustomUser

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ['username', 'password', 'name', 'email', 'role', 'location']
#         extra_kwargs = {'password': {'write_only': True}}

from rest_framework import serializers
from .models import CustomUser
from .models import *

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ['id', 'username', 'email', 'password', 'role', 'location']
#         extra_kwargs = {
#             # 'password': {'write_only': True},
#             'email': {'read_only': True},  # Assuming email is used as the username
#             'username': {'read_only': True}  # Assuming username is not changed after creation
#         }
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username','password', 'email', 'role', 'location','first_name','last_name','is_active']

class TotalUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role', 'location','first_name','last_name','is_active']


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id','user','project_name','company_name','location']

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['project','floor','floor_or_name','image']
        
class ItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemList
        fields = ['project','image','total_floors','no_of_employees']