from django.urls import path
from .views import *

urlpatterns = [
    path('create_user/', create_user),
    path('login/', login),
    path('total-users/', total_users, name='total_users'),
    path('post/', create_post, name='create_post'),
    path('project/', total_posts, name='total_post'),#1
    path('create_project_list/', create_item_list, name='create_item_list'),
    path('projectlist/', item_list, name='item_list'),#2
    path('plan_details/', plan_list, name='plan_list'),#3
    path('plans/project/<int:project_id>/', get_plans_by_project_id, name='get_plans_by_project_id'),
    path('generate_floor_plan/<int:project_id>/', save_json),
    path('getFloorPlan/', floor_plan_json),
    path('getFloorPlan/<int:project_id>',floor_plan_project_id),
    path('getFloorPlan/<int:floor_id>/', get_floor_plan_id),
    path('api/video/upload/', video_upload, name='video-upload'),
    path('plan-edit/<int:plan_id>/', plan_edit_view, name='plan_edit_view'),
    path('plan-images/', plan_image_view, name='plan_image_view'),
    path('video_processing/', video_processing, name='video_processing'),
    path('building/video_processing/', video_images, name='video_images'),
    path('notification/', send_email_notification, name='send_email_notification'),
    path('upload-video/', upload_video, name='upload_video'),
    path('success-page/', success_page, name='success_page'),
    path('plans/', plan_list, name='plan_list'),#4
    path('location_tracker/', location_tracker_view, name='location_tracker'),
    path('get-floor-plan/<int:plan_id>/', get_floor_plan, name='get_floor_plan'),
    path('upload-floor-plan/', upload_floor_plan, name='upload_floor_plan'),
    path('add-location/', add_location, name='add_location'),
    path('calculate_distance_and_steps/', calculate_distance_and_steps, name='calculate_distance_and_steps'),
    path('video/<int:video_id>/frames/', get_video_frames, name='get_video_frames'),
    path('markers/', get_markers, name='get_markers'),
    path('get_all_details/', get_all_details, name='get_all_details'),
    path('video-frames/<int:plan_id>/', get_video_frames_by_plan, name='get_video_frames_by_plandetails'),
    path('api/video-frames/plan/<int:plan_id>/video/<int:video_id>/', get_video_frames_by_plan_and_video, name='get_video_frames_by_plan_and_video'),
    path('api/create-customer/', create_customer),
    path('api/video-frames/plan/<int:plan_id>/', get_video_uploads, name='get_video_uploads'),
    path('video/<int:video_id>/upload_date/', get_video_upload_date, name='get_video_upload_date'),
]

