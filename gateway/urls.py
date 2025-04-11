from django.urls import path
from .views import create_user, create_device, create_gps_data, get_gps_data,login_user,login_view,save_gps_data,get_devices

urlpatterns = [
    path("user/create/", create_user, name="create-user"),
    path("device/create/", create_device, name="create-device"),
    path("gpsdata/create/", save_gps_data, name="create-gpsdata"),
    path("gpsdata/<str:device_id>/", get_gps_data, name="get-gpsdata"),
    path("login/", login_user, name="login"),
    path("get_device_data/",get_devices)
]
