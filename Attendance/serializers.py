from .models import *
from rest_framework import serializers


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        datetime_fields = ['start_time', 'pause_time', 'resume_time', 'stop_time']

        for field in datetime_fields:
            if data.get(field):
                data[field] = instance.__getattribute__(field).strftime("%Y-%m-%d %H:%M")
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'mobile', 'email', 'role', 'success', 'location', 'latitude', 'longitude', 'profileStatus']