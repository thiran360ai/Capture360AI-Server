from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Device, GPSData,CustomUser

User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = "__all__"

class GPSDataSerializer(serializers.ModelSerializer):
    # timestamp = serializers.SerializerMethodField()
    class Meta:
        model = GPSData
        fields = "__all__"
    # def get_timestamp(self, obj):
    #     return obj.date.strftime("%Y-%m-%d %H:%M:%S")