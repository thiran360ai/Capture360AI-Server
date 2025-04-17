from django.urls import path
from django.contrib import admin
from .views import *
from .views import  CreateEmployeeView
from . import views

urlpatterns = [
        path('create-user/', create_user, name='create_user'),
        path('login/', login_view, name='login'),
        path('create-employee/', CreateEmployeeView.as_view(), name='create_employee'),
        
        path('list-user-request/', InactiveEmployeesView.as_view(), name='inactive-employees'),
        path('list-device-id-request/', ActiveDevicesView.as_view(), name='devices'),
     
        path('user/status/', CheckUserActiveStatusView.as_view(), name='user-status'),
        path('Approve-User/', UpdateUserActiveStatusView.as_view(), name='user-update-status'),
        path('Approve-Device-ID/', UpdateDeviceActiveStatusView.as_view(), name='device-update-status'),
        path('check-user-approve-status/', CheckEmployeeStatusView.as_view(), name='check-employee-status'),
        path('check-device-id-approve-status/', CheckDeviceStatusView.as_view(), name='check-device-status'),

        path('attendance/total-hours/', GetTotalHoursView.as_view(), name='get-total-hours'),


        path('inactive-employees/<str:organization_key>/', InactiveEmployeeListView.as_view(), name='inactive-employees'),
        path('update-employee-status/', UpdateEmployeeStatusView.as_view(), name='update-employee-status'),
        path('employee-login/', EmployeeLoginView.as_view(), name='employee-login'),
        path('start/', views.start_attendance, name='start_attendance'),
        path('stop/', views.stop_attendance, name='stop_attendance'),
        path('pause/', views.pause_attendance, name='pause_attendance'),
        
        path('attendance/daily/', get_daily_attendance),
        
        path('attendance/organization/daily/', organization_daily_attendance, name='organization_daily_attendance'),

        path('attendance-range/', get_attendance_by_range, name='get_attendance_by_range'),

        path('api/devices/', create_device, name='create_device'),

        path('register/device/', RegisterDeviceView.as_view(), name='device-detail'),
]