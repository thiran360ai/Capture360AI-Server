from django.urls import path
from .views import *
from .views import AttendanceAPIView
urlpatterns = [
    path('attendance/<str:action>/', AttendanceAPIView.as_view(), name='attendance-action'),
    path('attendance/', get_attendance_by_user_device_and_date_range, name='get_attendance'),
    path('attendance-by-date/', get_users_present_on_date, name='get_attendance on date'),
    path('create-user/', create_user),
    path('login/', Emp_login)

]

