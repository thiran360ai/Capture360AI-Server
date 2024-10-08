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
from .models import VideoUpload

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
        



class VideoUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoUpload
        fields = ('id', 'user','floor', 'description', 'file', 'thumbnail', 'upload_date')



# serializers.py
from rest_framework import serializers
from .models import Location

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'plan', 'latitude', 'longitude', 'timestamp']


# class MarkerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Marker
#         fields = ['id', 'plan', 'x', 'y', 'distance']


# serializers.py
from rest_framework import serializers
from .models import Marker, Plan

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['id', 'floor_or_name', 'image']  # Include the fields you want to serialize

class MarkerSerializer(serializers.ModelSerializer):
    plan = PlanSerializer()  # Embed PlanSerializer for nested serialization

    class Meta:
        model = Marker
        fields = ['id', 'x', 'y', 'distance', 'plan']  # Include plan field with embedded serializer


class VideoUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoUpload
        fields = '__all__'


class VideoFrameSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoFrame
        fields = '__all__'

from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'



from rest_framework import serializers
from .models import VideoUpload

class VideoDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoUpload
        fields = ['id','upload_date', 'file','plan']  # Include only the required fields



class JsonSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaveJson
        fields=['id','name','data']
        