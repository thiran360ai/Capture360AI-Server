from rest_framework import serializers
from .models import *

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '_all_'

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'username','password','mobile', 'email', 'role','success', 'location','first_name','last_name','success']

class TotalEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'username', 'email', 'role','mobile', 'location','first_name','last_name','success']

class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model =UserDetails
        fields=  ['id','name','password','membership','subscribed','premium_amount']


class SaloonOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model =SaloonOrder
        fields=  ['customer_id', 'order_type', 'category', 'services', 'payment_status', 'payment_type', 'amount', 'date', 'time', 'created_at']
        created_at = serializers.SerializerMethodField()
  


class GymOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model =GymOrder
        fields=  ['id','customer_id','employee_id','gender','age','timeslot','status','category','plan','amount','attendance','purchaseddate','expiry_date','created_at','payment_status']
        created_at = serializers.SerializerMethodField()

class SpaOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model =SpaOrder
        fields=  ['id','customer_id','employee_id','category','services','payment_status','payment_type','amount','date','time','created_at','status']
        created_at = serializers.SerializerMethodField()

class HotelOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model =HotelOrder
        fields=  ['id','customer','amount','category','check_in','check_out','room_count','guest_count','created_at','status','payment_status']
        created_at = serializers.SerializerMethodField()
       


class AttendanceSerializer(serializers.ModelSerializer):
    # check_in = serializers.SerializerMethodField()
    class Meta:
        model =Attendance
        fields=['id','employee_attendance','status','check_in','check_out']
       

class PresentSerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField()
    class Meta:
        model =Attendance
        fields= ['id','employee','employee_name','status','latitude','longitude','check_in','check_out']

    def get_employee_name(self, obj):
        return obj.employee.name
