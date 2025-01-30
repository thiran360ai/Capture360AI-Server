from rest_framework import serializers
from .models import *
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'email', 'role', 'location', 'first_name', 'last_name', 'is_active']
        extra_kwargs = {'password': {'write_only': True}}

class TotalUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role', 'location', 'first_name', 'last_name', 'is_active']

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'user', 'project_name', 'company_name', 'location']

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['id', 'project', 'floor', 'floor_or_name', 'image']

class ItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemList
        fields = ['project', 'image', 'total_floors', 'no_of_employees']

class VideoUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoUpload
        fields = ['id', 'user', 'floor', 'description', 'file', 'thumbnail', 'upload_date','plan','json']

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'plan', 'latitude', 'longitude', 'timestamp']

class MarkerSerializer(serializers.ModelSerializer):
    plan = PlanSerializer()  # Nested serialization

    class Meta:
        model = Marker
        fields = ['id', 'x', 'y', 'distance', 'plan']

class VideoFrameSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoFrame
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class VideoDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoUpload
        fields = ['id', 'upload_date', 'file', 'plan','json']

class JsonSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaveJson
        fields = ['id','project', 'name', 'data','plan']
