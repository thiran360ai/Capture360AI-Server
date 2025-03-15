import datetime, json, os, cv2
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from building_construction.settings import EMAIL_HOST_USER
from profile_utility.form import PlanForm
from profile_utility.forms import VideoUploadForm
from profile_utility.utils import calculate_distance_and_steps_from_sensor_data
from .models import *
from .serializers import *


@api_view(['GET', 'POST'])
def create_user(request):
    if request.method == 'GET':
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
            user = CustomUser.objects.create(**serializer.validated_data)
            return Response({'message': 'User created successfully', 'user': serializer.data},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    try:
        user = CustomUser.objects.get(username=username)
    except CustomUser.DoesNotExist:
        return JsonResponse({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

    if check_password(password, user.password):
        return JsonResponse({'Success': 'Login successfully', 'user_id': user.id, 'result': user.role},
                            status=status.HTTP_200_OK)

    return JsonResponse({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def total_users(request):
    users = CustomUser.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_post(request):
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def total_posts(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_item_list(request):
    serializer = ItemListSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def item_list(request):
    if request.method == 'GET':
        item_lists = ItemList.objects.all()
        serializer = ItemListSerializer(item_lists, many=True)
        return Response(serializer.data)

    serializer = ItemListSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Utility function for validating serializer
def validate_and_save(serializer):
    if serializer.is_valid():
        serializer.save()
        return True, serializer.data
    return False, serializer.errors


@api_view(['GET', 'POST'])
def plan_list(request):
    if request.method == 'GET':
        plans = Plan.objects.all()
        serializer = PlanSerializer(plans, many=True)
        return Response(serializer.data)

        # POST request
        serializer = PlanSerializer(data=request.data)
        success, data_or_errors = validate_and_save(serializer)

    return Response(data_or_errors, status=status.HTTP_201_CREATED if success else status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def video_upload(request):
    serializer = VideoUploadSerializer(data=request.data)
    success, data_or_errors = validate_and_save(serializer)

    if success:
        total_video_uploads = VideoUpload.objects.count()
        response_data = {
            'message': 'Video uploaded successfully',
            'data': data_or_errors,
            'total_video_uploads': total_video_uploads
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

    return Response(data_or_errors, status=status.HTTP_400_BAD_REQUEST)


def upload_video(request):
    form = VideoUploadForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('success_page')  # Redirect to a success page after upload
    return render(request, 'upload_video.html', {'form': form})


def success_page(request):
    return render(request, 'success_page.html')


@api_view(['POST'])
def save_json(request, project_id):
    """Save JSON data for a specific project."""
    # Try to get the project or return a 404 response
    project = Post.objects.filter(id=project_id).first()
    if not project:
        return Response({'error': 'Project not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Initialize the serializer with request data, including the project ID
    serializer = JsonSerializer(data={**request.data, 'project': project_id})

    # Validate and save the data or return errors
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'JSON saved successfully.'}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def floor_plan_json(request):
    floor_plan = SaveJson.objects.all()
    serializer = JsonSerializer(floor_plan, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def floor_plan_project_id(request, project_id):
    """Retrieve floor plan JSON data for a specific project ID."""

    # Filter floor plans by the given project ID
    floor_plan = SaveJson.objects.filter(project_id=project_id)

    # If no data found, return a 404 response
    if not floor_plan.exists():
        return Response(
            {'error': f'No floor plans found for project ID {project_id}.'},
            status=status.HTTP_404_NOT_FOUND
        )

    # Serialize the data
    serializer = JsonSerializer(floor_plan, many=True)

    # Return the serialized data with a 200 OK status
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_floor_plan_id(request, floor_id):
    floor_plans = SaveJson.objects.filter(id=floor_id)
    if not floor_plans.exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = JsonSerializer(floor_plans, many=True)
    return Response(serializer.data)


import os
import cv2
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import VideoUpload


def save_frame(image, output_directory, frame_count, video):
    try:
        # Save the frame as an image file
        image_filename = f"{output_directory}/frame_{frame_count}.jpg"
        cv2.imwrite(image_filename, image)
        return image_filename
    except Exception as e:
        print(f"Error saving frame: {e}")
        return None


# @api_view(['GET'])
# def video_processing(request):
#     video_id = request.query_params.get('video_id')
#     if not video_id:
#         return Response({'error': 'Video ID is required'}, status=status.HTTP_400_BAD_REQUEST)

#     video = VideoUpload.objects.filter(id=video_id).first()
#     if not video:
#         return Response({'error': 'Video not found'}, status=status.HTTP_404_NOT_FOUND)

#     try:
#         video_path = video.file.path
#         output_directory = f'media/video_images/{video_id}'

#         # Ensure the output directory exists
#         os.makedirs(output_directory, exist_ok=True)

#         # Open the video file
#         cap = cv2.VideoCapture(video_path)
#         if not cap.isOpened():
#             print("Error opening video file.")
#             return Response({'error': 'Error opening video file'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         fps = cap.get(cv2.CAP_PROP_FPS)
#         if fps == 0:
#             print("Error: FPS is zero, possibly an invalid video file.")
#             return Response({'error': 'Invalid FPS, possibly an invalid video file'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         frame_count = 0

#         # Process each frame
#         while True:
#             success, image = cap.read()
#             if not success:
#                 break

#             # Save one frame per second
#             if frame_count % int(fps) == 0:
#                 image_path = save_frame(image, output_directory, frame_count, video)
#                 if not image_path:
#                     print("Error saving frame.")
#                     return Response({'error': 'Error saving frame'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#             frame_count += 1

#         cap.release()
#         return Response({'message': 'Video processed successfully'}, status=status.HTTP_200_OK)

#     except Exception as e:
#         print(f"Exception occurred: {e}")
#         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# def save_frame(image, output_directory, frame_count, video):
#     """Resizes and saves a frame image, creating a VideoFrame object."""
#     try:
#         # Resize image to 2:1 aspect ratio
#         height, width, _ = image.shape
#         new_width = int(height * 2)
#         resized_image = cv2.resize(image, (new_width, height))

#         # Create image path and save the image
#         image_path = os.path.join(output_directory, f'frame_{frame_count}.png')
#         cv2.imwrite(image_path, resized_image)
#         print('VideoFrame manik')

#         # Create VideoFrame entry in the database
#         VideoFrame.objects.create(
#             video=video,
#             frame_number=frame_count,
#             image=image_path,
#             timestamp=timezone.now()
#             # plan=plan
#         )
#         print(VideoFrame)
#         return image_path

#     except Exception:
#         return None

# def get_video_frames(request, video_id):
#     frames = VideoFrame.objects.filter(video_id=video_id).order_by('frame_number')
#     frame_data = [{'frame_number': frame.frame_number, 'image_url': request.build_absolute_uri(frame.image.url)} for frame in frames]

#     if not frame_data:
#         return JsonResponse({'error': 'Video frames not found'}, status=404)

#     return JsonResponse({'video_id': video_id, 'frames': frame_data}, status=200)

import os
import cv2
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import VideoUpload, VideoFrame
from PIL import Image


# @api_view(['GET'])
# def video_processing(request):
#     video_id = request.query_params.get('video_id')
#     if not video_id:
#         return Response({'error': 'Video ID is required'}, status=status.HTTP_400_BAD_REQUEST)

#     try:
#         video = VideoUpload.objects.get(id=video_id)
#     except VideoUpload.DoesNotExist:
#         return Response({'error': 'Video not found'}, status=status.HTTP_404_NOT_FOUND)

#     try:
#         video_path = video.file.path
#         output_directory = f'media/video_images/{video_id}'
#         os.makedirs(output_directory, exist_ok=True)

#         cap = cv2.VideoCapture(video_path)
#         if not cap.isOpened():
#             return Response({'error': 'Error opening video file'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         fps = cap.get(cv2.CAP_PROP_FPS)
#         frame_count = 0
#         success, image = cap.read()

#         while success:
#             if frame_count % int(fps) == 0:
#                 image_path = os.path.join(output_directory, f'frame_{frame_count}.png')

#                 # Resize image to 2:1 aspect ratio (adjust dimensions as needed)
#                 height, width, _ = image.shape
#                 new_width = int(height * 2)
#                 resized_image = cv2.resize(image, (new_width, height))

#                 # Save resized image as PNG
#                 cv2.imwrite(image_path, resized_image)

#                 VideoFrame.objects.create(
#                     video=video,
#                     frame_number=frame_count,
#                     image=image_path,
#                     timestamp=timezone.now(),
#                     plan=video.plan,
#                     json=json
#                 )

#             success, image = cap.read()
#             frame_count += 1

#         cap.release()

#         return Response({'message': 'Video processed successfully'}, status=status.HTTP_200_OK)
#     except Exception as e:
#         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def video_processing(request):
    video_id = request.query_params.get('video_id')
    if not video_id:
        return Response({'error': 'Video ID is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Fetch the video record
        video = VideoUpload.objects.get(id=video_id)
    except VideoUpload.DoesNotExist:
        return Response({'error': 'Video not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        # Extract the JSON data associated with the video
        json_data = None
        if video.json:
            json_data = video.json.data  # Assuming `SaveJson.data` is a JSONField containing JSON data

        # Define output directory for frames
        video_path = video.file.path
        output_directory = f'media/video_images/{video_id}'
        os.makedirs(output_directory, exist_ok=True)

        # Open video and process frames
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return Response({'error': 'Error opening video file'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = 0
        success, image = cap.read()

        while success:
            if frame_count % int(fps) == 0:  # Save one frame per second
                image_path = os.path.join(output_directory, f'frame_{frame_count}.png')

                # Resize image to 2:1 aspect ratio
                height, width, _ = image.shape
                new_width = int(height * 2)
                resized_image = cv2.resize(image, (new_width, height))

                # Save resized image as PNG
                cv2.imwrite(image_path, resized_image)

                # Save the frame and associated JSON to the database
                VideoFrame.objects.create(
                    video=video,
                    frame_number=frame_count,
                    image=image_path,
                    timestamp=timezone.now(),
                    plan=video.plan,
                    json=video.json  # Save the associated JSON object here
                )

            success, image = cap.read()
            frame_count += 1

        cap.release()

        return Response({'message': 'Video processed successfully'}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


from django.http import JsonResponse
from .models import VideoFrame


def get_video_frames(request, video_id):
    try:
        frames = VideoFrame.objects.filter(video_id=video_id).order_by('frame_number')
        frame_data = [{'frame_number': frame.frame_number, 'image_url': request.build_absolute_uri(frame.image.url)} for
                      frame in frames]
        return JsonResponse({'video_id': video_id, 'frames': frame_data}, status=200)
    except VideoFrame.DoesNotExist:
        return JsonResponse({'error': 'Video frames not found'}, status=404)


def video_images(request):
    upload_date = request.GET.get('upload_date')
    video_id = request.GET.get('video_id')

    if upload_date:
        return handle_upload_date(upload_date, request)

    if video_id:
        return handle_video_id(video_id, request)

    return render(request, 'manik.html', {'error': 'Video ID is required'})


def handle_upload_date(upload_date, request):
    try:
        # Assuming the upload_date is passed in a suitable format
        parsed_date = datetime.strptime(upload_date, '%B %d, %Y, %I:%M %p')
        video = VideoUpload.objects.filter(upload_date=parsed_date).first()

        if video:
            return get_frames_response(video, request)
        return JsonResponse({'error': 'No videos found for the selected date'}, status=404)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def handle_video_id(video_id, request):
    try:
        video = VideoUpload.objects.get(id=video_id)
        return get_frames_response(video, request)
    except VideoUpload.DoesNotExist:
        return render(request, 'manik.html', {'error': 'Video not found'})


def get_frames_response(video, request):
    frames = VideoFrame.objects.filter(video=video)
    frame_data = [{'url': frame.image.url, 'timestamp': frame.video_id} for frame in frames]

    # Send email notification
    send_video_images_email(request)

    all_upload_dates = list(VideoUpload.objects.values_list('id', flat=True))
    return render(request, 'manik.html', {'frames': frame_data, 'all_upload_dates': all_upload_dates})


def send_video_images_email(request):
    subject = 'Video Images Notification'
    message = f'The video images are ready for viewing. Click the link below to access them:\n{request.build_absolute_uri()}'
    recipient_list = ['recipient@example.com']  # Update with recipient's email

    send_mail(
        subject,
        message,
        from_email='manikvasu778899@gmail.com',
        recipient_list=recipient_list,
        html_message=None
    )


@api_view(['POST'])
def send_email_notification(request):
    email = request.data.get('email')
    image_url = request.data.get('image_url')

    if email and image_url:
        subject = '360-Degree Image Notification'
        message = f'Here is the link to the image: {image_url}'
        sender_email = 'manikvasu2000@gmail.com'  # Update with your email
        send_mail(subject, message, sender_email, [email])
        return Response({'success': True})

    return Response({'success': False, 'error': 'Missing email or image URL'}, status=400)


@api_view(['GET'])
def get_floor_plan(request, plan_id):
    plan = get_object_or_404(Plan, id=plan_id)
    if plan.image:
        return Response({'floor_plan': plan.image.url}, status=status.HTTP_200_OK)

    return Response({'error': 'Floor plan not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def upload_floor_plan(request):
    project_id = request.data.get('project_id')
    floor_id = request.data.get('floor_id')
    floor_or_name = request.data.get('floor_or_name')
    image = request.FILES.get('image')

    if all([project_id, floor_id, image]):
        plan = Plan.objects.create(
            project_id=project_id,
            floor_id=floor_id,
            floor_or_name=floor_or_name,
            image=image
        )
        return Response({'message': 'Floor plan uploaded successfully', 'plan_id': plan.id},
                        status=status.HTTP_201_CREATED)

    return Response({'error': 'Missing data'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def add_location(request):
    plan_id = request.data.get('plan_id')
    latitude = request.data.get('latitude')
    longitude = request.data.get('longitude')

    if all([plan_id, latitude, longitude]):
        plan = get_object_or_404(Plan, id=plan_id)
        Location.objects.create(plan=plan, latitude=latitude, longitude=longitude)
        return Response({'message': 'Location added successfully'}, status=status.HTTP_201_CREATED)

    return Response({'error': 'Missing data'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def calculate_distance_and_steps(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
        sensor_data_list = data.get('results')

        if not isinstance(sensor_data_list, list):
            return JsonResponse({'error': 'sensor_data should be a list of dictionaries.'}, status=400)

        results, total_distance, total_steps, total_seconds, all_step_distances, all_peak_times = process_sensor_data(
            sensor_data_list)

        return JsonResponse({
            'results': results,
            'total_distance_meters': float(total_distance),
            'total_steps': int(total_steps),
            'total_seconds': float(total_seconds),
            'all_step_distances': all_step_distances,
            'all_peak_times': all_peak_times
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def process_sensor_data(sensor_data_list):
    total_distance = 0.0
    total_steps = 0
    total_seconds = 0.0
    all_step_distances = []
    all_peak_times = []
    results = []

    for entry in sensor_data_list:
        sensor_data = entry.get('sensor_data')
        if not sensor_data:
            results.append({'sensor_data': sensor_data, 'error': 'sensor_data is missing.'})
            continue

        distance, steps, step_distances, peak_times = calculate_distance_and_steps_from_sensor_data(sensor_data)

        total_distance += float(distance)
        total_steps += int(steps)
        total_seconds += float(sensor_data['time'][-1]) - float(sensor_data['time'][0])
        all_step_distances.extend([float(d) for d in step_distances])
        all_peak_times.extend([float(t) for t in peak_times])

        results.append({
            'sensor_data': sensor_data,
            'distance': float(distance),
            'steps': int(steps),
            'step_distances': [float(d) for d in step_distances],
            'peak_times': [float(t) for t in peak_times]
        })

    return results, total_distance, total_steps, total_seconds, all_step_distances, all_peak_times


# Email sending utility function
def send_email_with_url(subject, message, recipient_list, url):
    try:
        message += f'\n\nURL: {url}'
        send_mail(subject, message, EMAIL_HOST_USER, recipient_list)
        return True
    except Exception as e:
        print(f"Email sending error: {e}")
        return False


# View for location tracker
def location_tracker_view(request):
    return render(request, 'location_tracker.html')


# View for plan images
def plan_image_view(request):
    plans = Plan.objects.all()
    return render(request, 'plan_images.html', {'plans': plans})


# View for editing plans
@api_view(['GET', 'POST'])
def plan_edit_view(request, plan_id):
    plan = get_object_or_404(Plan, id=plan_id)
    if request.method == 'POST':
        form = PlanForm(request.POST, request.FILES, instance=plan)
        if form.is_valid():
            form.save()
            update_markers(plan, request.POST)
            return redirect('plan_edit_view', plan_id=plan.id)
    else:
        form = PlanForm(instance=plan)
    return render(request, 'plan_edit.html', {'plan': plan, 'form': form})


def update_markers(plan, post_data):
    Marker.objects.filter(plan=plan).delete()  # Clear existing markers
    markers_x = post_data.getlist('markers_x')
    markers_y = post_data.getlist('markers_y')
    markers_distance = post_data.getlist('markers_distance')

    for x, y, distance in zip(markers_x, markers_y, markers_distance):
        Marker.objects.create(plan=plan, x=int(x), y=int(y), distance=float(distance) if distance else None)


# View to get video frames
@api_view(['GET'])
def get_video_frames(request, video_id):
    video = get_object_or_404(VideoUpload, id=video_id)
    frames = VideoFrame.objects.filter(video=video)
    frame_data = VideoFrameSerializer(frames, many=True).data

    plan_image_url = video.plan.image.url if video.plan and video.plan.image else None
    response_data = {
        'video_id': video.id,
        'video_description': video.description,
        'frames': frame_data,
        'video_url': video.file.url,
        'plan_image_url': plan_image_url
    }
    return Response(response_data, status=status.HTTP_200_OK)


# View to get markers
@api_view(['GET'])
def get_markers(request):
    markers = Marker.objects.all()
    serializer = MarkerSerializer(markers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# View to get all video details
@api_view(['GET'])
def get_all_details(request):
    video_id = request.query_params.get('id')
    if video_id:
        return get_video_details(video_id)

    return get_all_video_details()


def get_video_details(video_id):
    video = get_object_or_404(VideoUpload, id=video_id)
    frames = VideoFrame.objects.filter(video=video)
    frame_data = VideoFrameSerializer(frames, many=True).data

    plan_image_url = video.plan.image.url if video.plan and video.plan.image else None
    markers = Marker.objects.filter(plan=video.plan)
    marker_data = MarkerSerializer(markers, many=True).data

    video_details = {
        'video_id': video.id,
        'video_description': video.description,
        'video_url': video.file.url if video.file else None,
        'frames': frame_data,
        'plan_image_url': plan_image_url,
        'markers': marker_data
    }

    return Response(video_details, status=status.HTTP_200_OK)


def get_all_video_details():
    video_uploads = VideoUpload.objects.all()
    filtered_data = []

    for video in video_uploads:
        frames = VideoFrame.objects.filter(video=video)
        frame_data = VideoFrameSerializer(frames, many=True).data

        plan_image_url = video.plan.image.url if video.plan and video.plan.image else None
        markers = Marker.objects.filter(plan=video.plan)
        marker_data = MarkerSerializer(markers, many=True).data

        video_details = {
            'video_id': video.id,
            'video_description': video.description,
            'video_url': video.file.url if video.file else None,
            'frames': frame_data,
            'plan_image_url': plan_image_url,
            'markers': marker_data
        }
        filtered_data.append(video_details)

    return Response(filtered_data, status=status.HTTP_200_OK)


# Get plans by project ID
@api_view(['GET'])
def get_plans_by_project_id(request, project_id):
    plans = Plan.objects.filter(project_id=project_id)
    if not plans.exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = PlanSerializer(plans, many=True)
    return Response(serializer.data)


# Create a new customer
@api_view(['POST'])
def create_customer(request):
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Get all video frames
@api_view(['GET'])
def get_all_video_frames(request):
    frames = VideoFrame.objects.all()
    serializer = VideoFrameSerializer(frames, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Get video frames by plan and video ID
@api_view(['GET'])
def get_video_frames_by_plan_and_video(request, plan_id, video_id):
    video = get_object_or_404(VideoUpload, id=video_id)
    plan = get_object_or_404(Plan, id=plan_id)
    frames = VideoFrame.objects.filter(video=video, plan=plan)

    if not frames.exists():
        return Response({'error': 'No frames found for the given plan and video ID.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = VideoFrameSerializer(frames, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Get video frames by plan ID
@api_view(['GET'])
def get_video_frames_by_plan(request, plan_id):
    frames = VideoFrame.objects.filter(plan_id=plan_id)
    if not frames.exists():
        return Response({'error': 'No frames found for the given plan ID.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = VideoFrameSerializer(frames, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Get video uploads by plan ID
@api_view(['GET'])
def get_video_uploads(request, plan_id):
    plan = get_object_or_404(Plan, id=plan_id)
    video_uploads = VideoUpload.objects.filter(plan_id=plan_id)

    if not video_uploads.exists():
        return Response({'error': 'No video uploads found for the given plan ID.'}, status=status.HTTP_404_NOT_FOUND)

    plan_serializer = PlanSerializer(plan)
    frame_serializer = VideoUploadSerializer(video_uploads, many=True)

    response_data = {
        'plan': plan_serializer.data,
        'video_uploads': frame_serializer.data
    }

    return Response(response_data, status=status.HTTP_200_OK)


# Get video upload date by video ID
@api_view(['GET'])
def get_video_upload_date(request, video_id):
    video = get_object_or_404(VideoUpload, id=video_id)
    data = {
        'upload_date': video.upload_date,
    }
    return Response(data, status=status.HTTP_200_OK)
