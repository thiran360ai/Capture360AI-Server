from rest_framework import serializers
from .models import Employee
from .models import *

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        # fields = ['id', 'name', 'email', 'device_id', 'role', 'organizations', 'employee_id']
        fields='__all__'

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

class AttendanceSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.name', read_only=True)
    employee_email = serializers.EmailField(source='employee.email', read_only=True)
    organization_keys = serializers.SerializerMethodField()

    class Meta:
        model = Attendance
        fields = ['id', 'employee', 'employee_name', 'employee_email', 'date', 'logs', 'total_hours', 'organization_keys']

    def get_organization_keys(self, obj):
        return [org.key for org in obj.employee.organizations.all()]
