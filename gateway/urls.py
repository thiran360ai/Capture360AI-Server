from django.urls import path
from .views import *

urlpatterns = [
    path("user/create/", create_user, name="create-user"),
    path("device/create/", create_device, name="create-device"),
    path("gpsdata/create/", save_gps_data, name="create-gpsdata"),
    path("gpsdata/<str:device_id>/", get_gps_data, name="get-gpsdata"),
    path("login/", login_user, name="login"),
    path("get_device_data/",get_devices),
    path('gps/device/', get_device_gps_data),
    path('gps/user/<int:user_id>', get_user_gps_data),
]
