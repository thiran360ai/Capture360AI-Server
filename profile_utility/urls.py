from django.urls import path
# from . import views
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
from .views import video_upload
from .views import video_processing
# from .views import video_processing_view

urlpatterns = [
    path('create_user/',CreateUser),
    path('login/', login),
    path('total-users/', total_users, name='total_users'),
    path('post/', CreatePost, name='create_post'),
    path('project/',Total_Post, name='total_post'),
    path('create_project_list/', create_item_list, name='create_item_list'),
    path('projectlist/',item_list, name='item_list'),
    path('plan_details/',plan_list, name='plan_list'),
    path('plans/project/<int:project_id>/', get_plans_by_project_id, name='get_plans_by_project_id'),
    path('generate_floor_plan/',save_json),
    path('getFloorPlan/',floorplan_json),
    path('getFloorPlan/<int:floor_id>',get_floorplan_id),
    # path('upload/', upload_video, name='upload_video'),
    # path('videos/', video_list, name='video_list'),
    # path('videos/<int:video_id>/', view_video, name='view_video'),
    path('api/video/upload/', video_upload, name='video-upload'),
    # path('plan-images/',plan_image_view, name='plan_image_view'),
    # path('plan-edit/<int:plan_id>/', plan_edit_view, name='plan_edit_view'),
    path('plan-edit/<int:plan_id>/', plan_edit_view, name='plan_edit_view'),
    path('plan-images/', plan_image_view, name='plan_image_view'),
    path('video_processing/', video_processing, name='video_processing'),
    # path('video_processing/', video_processing_view, name='video_processing'),
    # path('video_images', views.video_images, name='video_images'),
    path('building/video_processing/', video_images, name='video_images'),
    path('notification/', send_email_notification, name='send_email_notification'),
    path('building/api/send-email-notification/', send_email_notification, name='send_email_notification'),
    # path('send-email-notification/', send_email_notification, name='send_email_notification'),
    path('upload-video/', upload_video, name='upload_video'),
    path('success-page/', success_page, name='success_page'),
    path('plans/', views.plan_list, name='plan_list'),
    # path('plans/<int:plan_id>/distance/', calculate_distance, name='calculate_distance'),
    # path('register/', views.UserRegistration.as_view(), name='user-register'),
    # path('login/', views.UserLogin.as_view(), name='user-login'),
    path('location_tracker/', location_tracker_view, name='location_tracker'),
    path('get-floor-plan/<int:plan_id>/', get_floor_plan, name='get_floor_plan'),
    path('upload-floor-plan/', upload_floor_plan, name='upload_floor_plan'),
    path('add-location/', add_location, name='add_location'),
    path('calculate_distance_and_steps/', calculate_distance_and_steps, name='calculate_distance_and_steps'),
    # path('calculate-distance/<int:plan_id>/', calculate_distance, name='calculate_distance'),
    # path('get_frames_by_date/', get_frames_by_date, name='get_frames_by_date'),
    path('video/<int:video_id>/frames/', get_video_frames, name='get_video_frames'),
    # path('video_frames/<int:video_id>/', get_video_frames, name='get_video_frames'),
    path('markers/', get_markers, name='get_markers'),
    path('get_all_details/', get_all_details, name='get_all_details'),
    # path('video-frames/', get_all_video_frames, name='get_all_video_frames'),
    path('video-frames/<int:plan_id>/', get_video_frames_by_plandetails, name='get_video_frames_by_plandetails'),
    path('api/video-frames/plan/<int:plan_id>/video/<int:video_id>/', get_video_frames_by_plan_and_video, name='get_video_frames_by_plan_and_video'),


    path('api/create-customer',views.create_customer),
    # path('api/video/details/', get_video_uploads, name='get_video_uploads'),
    path('api/video-frames/plan/<int:plan_id>/', get_video_uploads, name='get_video_uploads'),

    path('video/<int:video_id>/upload_date/', get_video_upload_date, name='get_video_upload_date'),

]