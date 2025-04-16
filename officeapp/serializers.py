from rest_framework import serializers
from .models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'name', 'email', 'device_id', 'role', 'organizations', 'employee_id']

from rest_framework import serializers
from .models import Device

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['id', 'device_id', 'user', 'is_active']
        read_only_fields = ['is_active']  # Prevent client from setting this

    def create(self, validated_data):
        validated_data['is_active'] = False  # Force to False
        return super().create(validated_data)
