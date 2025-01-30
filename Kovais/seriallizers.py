from rest_framework import serializers
from .models import *

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '_all_'

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'username','password','mobile', 'email', 'role','success', 'location','first_name','last_name']

class TotalEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'username', 'email', 'role','mobile', 'location','first_name','last_name']

class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model =UserDetails
        fields=  ['id','name','password','membership','subscribed','premium_amount']


class SaloonOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model =SaloonOrder
        fields=  ['username', 'order_type', 'category', 'services', 'payment_status', 'payment_type', 'amount', 'date', 'time', 'created_at']
        created_at = serializers.SerializerMethodField()
  


class GymOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model =GymOrder
        fields=  ['id','gender','timeslot','status','category','plan','amount','attendance','purchaseddate','created_at']
        created_at = serializers.SerializerMethodField()

class SpaOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model =SpaOrder
        fields=  ['id','username','order_type','category','services','date','time','created_at']
        created_at = serializers.SerializerMethodField()

class HotelOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model =HotelOrder
        fields=  ['id','username','order_type','category','services','date','time','created_at']
        created_at = serializers.SerializerMethodField()
