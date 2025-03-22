from django.urls import path
from .views import *

urlpatterns = [
    # path('', home, name='home'),  # Home Page
    path('properties/', property_list_create, name='property-list-create'),
    path('banners/', banner_list_create, name='banner-list-create'),
    # path('land-images/', land_image_list_create, name='land-images'),
    path('landslist/', land_list_create, name='land-list-create'),
    path('locations/', location_list_create, name='location-list-create'),
]
