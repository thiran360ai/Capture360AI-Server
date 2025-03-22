from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Property, Banner, LandListing, LocationExample
from .serializers import PropertySerializer, BannerSerializer, LandListingSerializer, LocationExampleSerializer

# Home View (Basic Welcome Message)
@api_view(['GET'])
def home(request):
    return Response({"message": "Welcome to the Property App!"})

# Property List & Create View
@api_view(['GET', 'POST'])
def property_list_create(request):
    if request.method == 'GET':
        properties = Property.objects.all()
        serializer = PropertySerializer(properties, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PropertySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Banner List & Create View
@api_view(['GET', 'POST'])
def banner_list_create(request):
    if request.method == 'GET':
        banners = Banner.objects.all()
        serializer = BannerSerializer(banners, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = BannerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Land Listing List & Create View
@api_view(['GET', 'POST'])
def land_list_create(request):
    if request.method == 'GET':
        lands = LandListing.objects.all()
        serializer = LandListingSerializer(lands, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = LandListingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# LocationExample List & Create View
@api_view(['GET', 'POST'])
def location_list_create(request):
    if request.method == 'GET':
        locations = LocationExample.objects.all()
        serializer = LocationExampleSerializer(locations, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = LocationExampleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
