## serializers.py
from rest_framework import serializers
from .models import *


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ['name', 'contact_number']  # Include only name and contact fields
class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'

class LocationExampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationExample
        fields = '__all__'

class LandListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandListing
        fields = '__all__'
