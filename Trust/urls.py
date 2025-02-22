from django.urls import path

from .views import *

# from .views import video_processing_view

urlpatterns = [
    path('save-contact/',contact)
]