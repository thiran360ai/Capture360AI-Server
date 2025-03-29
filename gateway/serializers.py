from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Device, GPSData,CustomUser

User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = "__all__"

class GPSDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = GPSData
        fields = "__all__"
