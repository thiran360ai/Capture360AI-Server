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
