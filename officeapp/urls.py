from django.urls import path
from django.contrib import admin
from .views import *
from .views import  CreateEmployeeView
from . import views

urlpatterns = [
        path('create-user/', create_user, name='create_user'),
        path('login/', login_view, name='login'),
        path('create-employee/', CreateEmployeeView.as_view(), name='create_employee'),
        path('inactive-employees/<str:organization_key>/', InactiveEmployeeListView.as_view(), name='inactive-employees'),
        path('update-employee-status/', UpdateEmployeeStatusView.as_view(), name='update-employee-status'),
        path('employee-login/', EmployeeLoginView.as_view(), name='employee-login'),
        path('start/', views.start_attendance, name='start_attendance'),
        path('stop/', views.stop_attendance, name='stop_attendance'),
        path('pause/', views.pause_attendance, name='pause_attendance'),

]