from django.urls import path
from . import views
import statistics
from django.conf import Settings, SettingsReference, settings
from django.contrib import admin
from django.urls import path,include
from .models import *
from .views import *
from profile_utility import views
from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static
# from .views import register_and_login
from . import views

 

urlpatterns = [
    path('create_user/',CreateUser),
    path('login/', login),
    path('total-users/', total_users, name='total_users'),

    path('post/', CreatePost, name='create_post'),
    path('project/',Total_Post, name='total_post'),
    path('create_project_list/', create_item_list, name='create_item_list'),
    path('projectlist/',item_list, name='item_list'),
    path('plan_details/',plan_list, name='plan_list')
    


    # path('register/', views.UserRegistration.as_view(), name='user-register'),
    # path('login/', views.UserLogin.as_view(), name='user-login'),
]