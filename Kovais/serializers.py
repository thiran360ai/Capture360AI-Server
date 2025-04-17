from rest_framework import serializers
from .models import *


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '_all_'


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        # fields = ['id', 'username', 'password', 'mobile', 'email', 'role', 'success', 'location', 'first_name',
                #   'last_name', 'success']
        fields = '__all__'

class TotalEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'username', 'email', 'role', 'mobile', 'location', 'first_name', 'last_name', 'success']


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        # fields = ['id', 'name', 'password', 'membership', 'subscribed', 'premium_amount']
        # fields = '_all_'
        fields = ('id','name', 'membership', 'points', 'emblem_url','password')

class SaloonOrdersSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source="customer_id.name", read_only=True)

    class Meta:
        model = SaloonOrder
        fields = '__all__'  # This includes all model fields
        extra_fields = ['customer_name']
        created_at = serializers.SerializerMethodField()


class GymOrderSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source="customer_id.name", read_only=True)

    class Meta:
        model = GymOrder
        fields = '__all__'  # This includes all model fields
        extra_fields = ['customer_name']


class SpaOrdersSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source="customer_id.name", read_only=True)

    class Meta:
        model = SpaOrder
        fields = '__all__'  # This includes all model fields
        extra_fields = ['customer_name']


class HotelOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelOrder
        fields= '__all__'
        # fields = ['id', 'customer_id', 'employee_id', 'guest_name', 'amount', 'check_in', 'check_out', 'category',
        #           'room_count', 'guest_count', 'status', 'payment_status', 'created_at']
        created_at = serializers.SerializerMethodField()


class AttendanceSerializer(serializers.ModelSerializer):
    # check_in = serializers.SerializerMethodField()
    class Meta:
        model = Attendance
        fields = ['id', 'employee_attendance', 'status', 'check_in', 'check_out']


class PresentSerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField()

    class Meta:
        model = Attendance
        fields = ['id', 'employee', 'employee_name', 'status', 'latitude', 'longitude', 'check_in', 'check_out']

    def get_employee_name(self, obj):
        return obj.employee.name


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'description', 'status', 'employee']




class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'customer_id', 'order_id', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'created_at']
