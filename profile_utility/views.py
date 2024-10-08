from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer
from django.shortcuts import redirect, render
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from .models import * 
from .serializers import *
from.views import *
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from .models import CustomUser
from .serializers import UserSerializer
import os
import cv2
import rawpy
import imageio
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import VideoUpload, VideoFrame
import numpy as np
# import rawpy
# from pydng.core import RPICAM2DNG
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST', 'GET'])
def CreateUser(request):
    if request.method == 'GET':
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # Hash the password before saving
            serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
            user = CustomUser.objects.create(**serializer.validated_data)
            return Response({'message': 'User created successfully', 'user': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth.hashers import check_password
from .models import CustomUser
import traceback

@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        try:
            username = request.data.get('username')
            password = request.data.get('password')

            # Debugging: Print received username and password
            print("Received username:", username)
            print("Received password:", password)

            try:
                user = CustomUser.objects.get(username=username)
            except CustomUser.DoesNotExist:
                print("User not found")
                return JsonResponse({'login': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

            if check_password(password, user.password):
                print("Password matched")
                return JsonResponse({'Success': 'login successfully', 'user_id': user.id,'result':user.role}, status=status.HTTP_200_OK)
            else:
                print("Password did not match")
                return JsonResponse({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Print the full traceback to debug the issue
            traceback.print_exc()
            return JsonResponse({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def total_users(request):
    users = CustomUser.objects.all()
    serializer = TotalUserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Post
from .serializers import PostSerializer

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

@api_view(['POST'])
def CreatePost(request):
    if request.method == 'POST':

        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # If the request method is not POST, return a method not allowed response
    return Response({'error': 'Method not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



@api_view(['GET'])
def Total_Post(request):
    project=Post.objects.all()
    serlizer=PostSerializer(project,many=True)
    return Response(serlizer.data, status=status.HTTP_200_OK)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import ItemList
from .serializers import ItemListSerializer

@api_view(['POST'])
def create_item_list(request):
    if request.method == 'POST':
        serializer = ItemListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'Method not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET', 'POST'])
def item_list(request):
    if request.method == 'GET':
        item_lists = ItemList.objects.all()
        serializer = ItemListSerializer(item_lists, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ItemListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({'error': 'Method not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Plan
from .serializers import PlanSerializer
from rest_framework.parsers import MultiPartParser, FormParser

@api_view(['GET', 'POST'])
def plan_list(request):
    if request.method == 'GET':
        plans = Plan.objects.all()
        serializer = PlanSerializer(plans, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        parser_classes = (MultiPartParser, FormParser)
        serializer = PlanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response({'error': 'Method not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import VideoUpload
from .serializers import VideoUploadSerializer

@api_view(['POST'])
def video_upload(request):
    if request.method == 'POST':
        serializer = VideoUploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            # Get the total number of video uploads
            total_video_uploads = VideoUpload.objects.count()

            # Construct the response data
            response_data = {
                'message': 'Video uploaded successfully',
                'data': serializer.data,
                'total_video_uploads': total_video_uploads
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



from django.shortcuts import render, redirect
from .forms import VideoUploadForm

def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success_page')  # Redirect to a success page after upload
    else:
        form = VideoUploadForm()
    return render(request, 'upload_video.html', {'form': form})

def success_page(request):
    return render(request, 'success_page.html')

from django.urls import reverse
from django.http import HttpResponseRedirect

def some_view(request):
    # Your view logic...
    return HttpResponseRedirect(reverse('success_page'))


from .serializers import JsonSerializer
from .models import SaveJson

@csrf_exempt
@api_view(['POST'])
def save_json(request):
    if request.method == 'POST':
        serializer = JsonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Construct the response data
            response_data = {
                'message': 'Json saved successfully'
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def floorplan_json(request):
    floorplan = SaveJson.objects.all()
    serializer = JsonSerializer(floorplan, many=True)
    return Response(serializer.data)


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import VideoUpload  # Make sure to import your model

@api_view(['GET'])
def get_floorplan_id(request,floor_id):
    floorplans = SaveJson.objects.filter(id=floor_id)
    if not floorplans.exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = JsonSerializer(floorplans, many=True)
    return Response(serializer.data)


import os
import cv2
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import VideoUpload, VideoFrame
from PIL import Image

@api_view(['GET'])
def video_processing(request):
    video_id = request.query_params.get('video_id')
    if not video_id:
        return Response({'error': 'Video ID is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        video = VideoUpload.objects.get(id=video_id)
    except VideoUpload.DoesNotExist:
        return Response({'error': 'Video not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        video_path = video.file.path
        output_directory = f'media/video_images/{video_id}'
        os.makedirs(output_directory, exist_ok=True)

        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return Response({'error': 'Error opening video file'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = 0
        success, image = cap.read()

        while success:
            if frame_count % int(fps) == 0:
                image_path = os.path.join(output_directory, f'frame_{frame_count}.png')

                # Resize image to 2:1 aspect ratio (adjust dimensions as needed)
                height, width, _ = image.shape
                new_width = int(height * 2)
                resized_image = cv2.resize(image, (new_width, height))

                # Save resized image as PNG
                cv2.imwrite(image_path, resized_image)

                VideoFrame.objects.create(
                    video=video,
                    frame_number=frame_count,
                    image=image_path,
                    timestamp=timezone.now(),
                    plan=video.plan
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
        frame_data = [{'frame_number': frame.frame_number, 'image_url': request.build_absolute_uri(frame.image.url)} for frame in frames]
        return JsonResponse({'video_id': video_id, 'frames': frame_data}, status=200)
    except VideoFrame.DoesNotExist:
        return JsonResponse({'error': 'Video frames not found'}, status=404)



# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status
# from .models import VideoFrame
# from django.utils.dateparse import parse_date

# @api_view(['GET'])
# def get_frames_by_date(request):
#     video_id = request.query_params.get('video_id')
#     date_str = request.query_params.get('date')

#     if not video_id or not date_str:
#         return Response({'error': 'Video ID and date are required'}, status=status.HTTP_400_BAD_REQUEST)
    
#     date = parse_date(date_str)
#     if not date:
#         return Response({'error': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)
    
#     frames = VideoFrame.objects.filter(video_id=video_id, timestamp__date=date)
#     frame_data = [{'frame_number': frame.frame_number, 'image': frame.image.url} for frame in frames]
    
#     return Response({'frames': frame_data}, status=status.HTTP_200_OK)


# from django.shortcuts import render
# from .models import VideoUpload, VideoFrame
# from django.core.mail import send_mail
# from django.shortcuts import render
# from .models import VideoUpload, VideoFrame

# def video_images(request):
#     video_id = request.GET.get('video_id')
#     if video_id:
#         try:
#             video = VideoUpload.objects.get(id=video_id)
#             frames = VideoFrame.objects.filter(video=video)
#             frame_data = [{'url': frame.image.url, 'timestamp': frame.timestamp} for frame in frames]
#             print(frame_data)  # Debugging line
            
#             # URL for the video_images view
#             url = request.build_absolute_uri()

#             # Define email subject and message
#             subject = 'Video Images Notification'
#             message = 'The video images are ready for viewing. Click the link below to access them:'
            
#             # Send email with URL to recipient
#             recipient_list = ['recipient@example.com']  # Update with recipient's email
#             send_email_with_url(subject, message, recipient_list, url)

#             return render(request, 'video_images.html', {'frames': frame_data})
#         except VideoUpload.DoesNotExist:
#             return render(request, 'video_images.html', {'error': 'Video not found'})
#     else:
#         return render(request, 'video_images.html', {'error': 'Video ID is required'})
from django.shortcuts import render
from django.core.mail import send_mail
from .models import VideoUpload, VideoFrame
from django.utils import timezone
from django.shortcuts import render
from django.core.mail import send_mail
from .models import VideoUpload, VideoFrame

from django.shortcuts import render
from django.core.mail import send_mail
from .models import VideoUpload, VideoFrame

from django.shortcuts import render
from django.core.mail import send_mail
from .models import VideoUpload, VideoFrame

# def video_images(request):
#     video_id = request.GET.get('video_id')
#     if video_id:
#         try:
#             video = VideoUpload.objects.get(id=video_id)
#             frames = VideoFrame.objects.filter(video=video)
#             frame_data = [{'url': frame.image.url, 'timestamp': frame.timestamp} for frame in frames]
            
#             # Collect all upload_date values
#             all_upload_dates = list(VideoUpload.objects.values_list('upload_date', flat=True))
            
#             # Print upload_date for debugging
#             print("All Upload Dates:", all_upload_dates)
            
#             # URL for the video_images view
#             url = request.build_absolute_uri()
            
#             # Define email subject and message
#             subject = 'Video Images Notification'
#             message = f'The video images are ready for viewing. Click the link below to access them:\n{url}'

#             # Send email with URL to recipient
#             recipient_list = ['']  # Update with recipient's email
#             send_mail(subject, message, from_email='manikvasu778899@gmail.com', recipient_list=recipient_list, html_message=None)

#             return render(request, 'manik.html', {'frames': frame_data, 'all_upload_dates': all_upload_dates})
#         except VideoUpload.DoesNotExist:
#             return render(request, 'manik.html', {'error': 'Video not found'})
#     else:
#         return render(request, 'manik.html', {'error': 'Video ID is required'})

from django.shortcuts import render
from django.core.mail import send_mail
from .models import VideoUpload, VideoFrame

from django.shortcuts import render
from django.core.mail import send_mail
from django.http import JsonResponse
from .models import VideoUpload, VideoFrame

from django.shortcuts import render
from django.core.mail import send_mail
from django.http import JsonResponse
from .models import VideoUpload, VideoFrame
from datetime import datetime

def video_images(request):
    upload_date = request.GET.get('upload_date')
    print(f"Received upload_date: {upload_date}")
    if upload_date:
        try:
            # Parse upload_date to match the format in your database
            # parsed_date = datetime.strptime(upload_date, '%B %d, %Y, %I:%M %p')
            parsed_date = VideoUpload.objects.get(id=video_id)
            print(parsed_date)
            video = VideoUpload.objects.filter(upload_date=parsed_date).first()
            if video:
                frames = VideoFrame.objects.filter(video=video)
                frame_data = [{'url': frame.image.url, 'timestamp': frame.video_id} for frame in frames]
                return JsonResponse({'frames': frame_data})
            else:
                return JsonResponse({'error': 'No videos found for the selected date'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    video_id = request.GET.get('video_id')
    if video_id:
        try:
            video = VideoUpload.objects.get(id=video_id)
            frames = VideoFrame.objects.filter(video=video)
            frame_data = [{'url': frame.image.url, 'timestamp': frame.video_id} for frame in frames]

            all_upload_dates = list(VideoUpload.objects.values_list('id', flat=True))

            # URL for the video_images view
            url = request.build_absolute_uri()

            # Define email subject and message
            subject = 'Video Images Notification'
            message = f'The video images are ready for viewing. Click the link below to access them:\n{url}'

            # Send email with URL to recipient
            recipient_list = ['']  # Update with recipient's email
            send_mail(subject, message, from_email='manikvasu778899@gmail.com', recipient_list=recipient_list, html_message=None)

            return render(request, 'manik.html', {'frames': frame_data, 'all_upload_dates': all_upload_dates})
        except VideoUpload.DoesNotExist:
            return render(request, 'manik.html', {'error': 'Video not found'})
    else:
        return render(request, 'manik.html', {'error': 'Video ID is required'})


# from django.shortcuts import render
# from django.core.mail import send_mail
# from .models import VideoUpload, VideoFrame

# def video_images(request):
#     video_id = request.GET.get('video_id')
#     if video_id:
#         try:
#             video = VideoUpload.objects.get(id=video_id)
#             frames = VideoFrame.objects.filter(video=video)
#             frame_data = [{'url': frame.image.url, 'timestamp': frame.timestamp} for frame in frames]
#             print(frame_data)  # Debugging line
            
#             # URL for the video_images view
#             url = request.build_absolute_uri()

#             # Define email subject and message
#             subject = 'Video Images Notification'
#             message = 'The video images are ready for viewing. Click the link below to access them:'
            
#             # Send email with URL to recipient
#             recipient_list = ['manikvasu2000@gmail.com']  # Update with recipient's email
#             send_mail(subject, message, from_email='manikvasu778899@gmail.com', recipient_list=recipient_list, html_message=None)
#             print(send_mail,'manik')
#             return render(request, 'vasu.html', {'frames': frame_data})
#         except VideoUpload.DoesNotExist:
#             return render(request, 'vasu.html', {'error': 'Video not found'})
#     else:
#         return render(request, 'vasu.html', {'error': 'Video ID is required'})
    
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def send_email_notification(request):
    print('manik')
    if request.method == 'POST':
        email = request.data.get('email')
        image_url = request.data.get('image_url')

        if email and image_url:
            subject = '360-Degree Image Notification'
            message = f'Here is the link to the image: {image_url}'
            sender_email = 'manikvasu2000@gmail.com'  # Update with your email
            send_mail(subject, message, sender_email, [email])
            return Response({'success': True})
        else:
            return Response({'success': False, 'error': 'Missing email or image URL'}, status=400)
    else:
        return Response({'success': False, 'error': 'Invalid request method'}, status=405)





# views.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Plan, Location
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from geopy.distance import geodesic

@api_view(['GET'])
def get_floor_plan(request, plan_id):
    plan = get_object_or_404(Plan, id=plan_id)
    if plan.image:
        image_url = plan.image.url
        return Response({'floor_plan': image_url}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Floor plan not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def upload_floor_plan(request):
    project_id = request.data.get('project_id')
    floor_id = request.data.get('floor_id')
    floor_or_name = request.data.get('floor_or_name')
    image = request.FILES.get('image')

    if project_id and floor_id and image:
        plan = Plan.objects.create(
            project_id=project_id,
            floor_id=floor_id,
            floor_or_name=floor_or_name,
            image=image
        )
        return Response({'message': 'Floor plan uploaded successfully', 'plan_id': plan.id}, status=status.HTTP_201_CREATED)
    else:
        return Response({'error': 'Missing data'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def add_location(request):
    plan_id = request.data.get('plan_id')
    latitude = request.data.get('latitude')
    longitude = request.data.get('longitude')

    if plan_id and latitude and longitude:
        plan = get_object_or_404(Plan, id=plan_id)
        Location.objects.create(plan=plan, latitude=latitude, longitude=longitude)
        return Response({'message': 'Location added successfully'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'error': 'Missing data'}, status=status.HTTP_400_BAD_REQUEST)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .utils import calculate_distance_and_steps_from_sensor_data

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .utils import calculate_distance_and_steps_from_sensor_data

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .utils import calculate_distance_and_steps_from_sensor_data

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .utils import calculate_distance_and_steps_from_sensor_data

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .utils import calculate_distance_and_steps_from_sensor_data

@csrf_exempt
def calculate_distance_and_steps(request):
    if request.method == 'POST':
        try:
            # Extract sensor_data from the request body
            body = request.body.decode('utf-8')
            data = json.loads(body)
            sensor_data_list = data.get('results', None)

            if sensor_data_list is None:
                return JsonResponse({'error': 'sensor_data is None. It should be a list of sensor data dictionaries.'}, status=400)

            if not isinstance(sensor_data_list, list):
                return JsonResponse({'error': 'sensor_data should be a list of sensor data dictionaries.'}, status=400)

            total_distance = 0.0
            total_steps = 0
            total_seconds = 0.0
            all_step_distances = []
            all_peak_times = []
            
            results = []
            for entry in sensor_data_list:
                sensor_data = entry.get('sensor_data', None)
                try:
                    if sensor_data is None:
                        raise ValueError("sensor_data is missing.")
                    # Calculate distance, step count, and time for each sensor data entry
                    distance, steps, step_distances, peak_times = calculate_distance_and_steps_from_sensor_data(sensor_data)
                    # Add to the total distance, step count, and total time
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
                except Exception as e:
                    results.append({'sensor_data': sensor_data, 'error': str(e)})

            # Convert total distance to meters (if not already in meters)
            total_distance_meters = total_distance  # Assuming total_distance is already in meters

            return JsonResponse({
                'results': results,
                'total_distance_meters': float(total_distance_meters),
                'total_steps': int(total_steps),
                'total_seconds': float(total_seconds),
                'all_step_distances': all_step_distances,
                'all_peak_times': all_peak_times
            })

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)








# views.py
from django.shortcuts import render

def location_tracker_view(request):
    return render(request, 'location_tracker.html')



from django.core.mail import send_mail

def send_email_with_url(subject, message, recipient_list, url):
    try:
        # Append the URL to the message
        message += f'\n\nURL: {url}'
        print('dncj,sbcjdbcjbsja')
        send_mail(subject, message, EMAIL_HOST_USER, recipient_list)
        return True
    except Exception as e:
        print(e)  # Print the error for debugging
        return False


def plan_image_view(request):
    plans = Plan.objects.all()
    return render(request, 'plan_images.html', {'plans': plans})

# views.py
# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Plan, Marker
from .forms import PlanForm
from django.http import JsonResponse
from rest_framework.decorators import api_view

@api_view(['GET', 'POST'])
def plan_edit_view(request, plan_id):
    plan = get_object_or_404(Plan, id=plan_id)
    if request.method == 'POST':
        form = PlanForm(request.POST, request.FILES, instance=plan)
        if form.is_valid():
            form.save()
            markers_x = request.POST.getlist('markers_x')
            markers_y = request.POST.getlist('markers_y')
            markers_distance = request.POST.getlist('markers_distance')
            Marker.objects.filter(plan=plan).delete()  # Clear existing markers
            for i in range(len(markers_x)):
                x = int(markers_x[i])
                y = int(markers_y[i])
                distance = float(markers_distance[i]) if markers_distance[i] else None
                Marker.objects.create(plan=plan, x=x, y=y, distance=distance)
            return redirect('plan_edit_view', plan_id=plan.id)
    else:
        form = PlanForm(instance=plan)
    return render(request, 'plan_edit.html', {'plan': plan, 'form': form})




# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import VideoUpload, VideoFrame

@api_view(['GET'])
def get_video_frames(request, video_id):
    try:
        video = VideoUpload.objects.get(id=video_id)
        frames = VideoFrame.objects.filter(video=video)
        frame_data = [
            {
                'frame_number': frame.frame_number,
                'url': frame.image.url,
                'timestamp': frame.timestamp,
                
            }
            for frame in frames
        ]
        
        # Retrieve the associated Plan and its image
        if video.plan:
            plan_image_url = video.plan.image.url
        else:
            plan_image_url = None
        
        response_data = {
            'video_id': video.id,
            'video_description': video.description,
            'frames': frame_data,
            'video_url': video.file.url,
            'plan_image_url': plan_image_url
        }
        return Response(response_data, status=status.HTTP_200_OK)
    except VideoUpload.DoesNotExist:
        return Response({'error': 'Video not found'}, status=status.HTTP_404_NOT_FOUND)


# views.py
# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Marker
from .serializers import MarkerSerializer

@api_view(['GET'])
def get_markers(request):
    try:
        markers = Marker.objects.all()
        serializer = MarkerSerializer(markers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Marker.DoesNotExist:
        return Response({'error': 'Markers not found'}, status=status.HTTP_404_NOT_FOUND)


# views.py

# views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import VideoUpload, VideoFrame, Marker, Plan
from .serializers import VideoUploadSerializer, VideoFrameSerializer, MarkerSerializer, PlanSerializer

# views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import VideoUpload, VideoFrame, Marker, Plan
from .serializers import VideoUploadSerializer, VideoFrameSerializer, MarkerSerializer, PlanSerializer

@api_view(['GET'])
def get_all_details(request):
    try:
        video_id = request.query_params.get('id')  # Get the 'id' parameter from query string

        # Retrieve all video uploads
        video_uploads = VideoUpload.objects.all()

        # Initialize variables to store filtered data
        filtered_data = []

        # If video_id is provided, filter details based on that ID
        if video_id:
            try:
                video = VideoUpload.objects.get(id=video_id)
                frames = VideoFrame.objects.filter(video=video)
                frame_data = VideoFrameSerializer(frames, many=True).data

                plan_image_url = None
                if video.plan and video.plan.image:
                    plan_image_url = video.plan.image.url

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

            except VideoUpload.DoesNotExist:
                return Response({'error': 'Video not found'}, status=status.HTTP_404_NOT_FOUND)

        # If no video_id provided, return details for all videos
        else:
            for video in video_uploads:
                frames = VideoFrame.objects.filter(video=video)
                frame_data = VideoFrameSerializer(frames, many=True).data

                plan_image_url = None
                if video.plan and video.plan.image:
                    plan_image_url = video.plan.image.url

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

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Plan
from .serializers import PlanSerializer


@api_view(['GET'])
def get_plans_by_project_id(request, project_id):
    plans = Plan.objects.filter(project_id=project_id)
    if not plans.exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = PlanSerializer(plans, many=True)
    return Response(serializer.data)

from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .models import Customer
from .serializers import CustomerSerializer

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def create_customer(request):
    if request.method == 'POST':
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response("Invalid request method.", status=status.HTTP_405_METHOD_NOT_ALLOWED)

# @api_view(['POST'])
# def create_customer(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         college_name = request.POST.get('college_name')
#         email_id=request.POST.get('email_id')
#         mobile = request.POST.get('mobile')
#         course= request.POST.get('course')
#         resume = request.POST.get('resume')
#         address = request.POST.get('address')
#         designation = request.POST.get('designation')
        
#         # Create a new patient entry in the database using the Patient model
#         user_details = Customer(
#                 username=username,
#                 designation=designation,
#                 mobile=mobile,
#                 resume=resume,
#                 college_name=college_name,
#                 email_id=email_id,
#                 address=address,
#                 course=course
#             )
#         user_details.save()
#         return Response("Data successfully inserted!")
#     else:
#         return Response("Invalid request method.")

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import VideoFrame
from .serializers import VideoFrameSerializer

@api_view(['GET'])
def get_all_video_frames(request):
    frames = VideoFrame.objects.all()
    serializer = VideoFrameSerializer(frames, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from .models import VideoFrame, VideoUpload, Plan
from .serializers import VideoFrameSerializer
from rest_framework import status

@api_view(['GET'])
def get_video_frames_by_plan_and_video(request, plan_id, video_id):
    try:
        # Ensure the video exists
        video = get_object_or_404(VideoUpload, id=video_id)

        # Ensure the plan exists
        plan = get_object_or_404(Plan, id=plan_id)

        # Filter frames by both plan and video
        frames = VideoFrame.objects.filter(video=video, plan=plan)
        
        # Check if frames exist for the given filters
        if not frames.exists():
            return Response({'error': 'No frames found for the given plan and video ID.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Serialize the frames
        serializer = VideoFrameSerializer(frames, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_video_frames_by_plandetails(request, plan_id):
    try:
        frames = VideoFrame.objects.filter(plan_id=plan_id)
        if not frames.exists():
            return Response({'error': 'No frames found for the given plan ID.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = VideoFrameSerializer(frames, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import VideoUpload
from .serializers import VideoUploadSerializer

# @api_view(['GET'])
# def get_video_uploads(request):
#     video_uploads = VideoUpload.objects.all()
#     serializer = VideoDateSerializer(video_uploads, many=True)
#     return Response(serializer.data)
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from .models import VideoFrame, Plan
from .serializers import VideoFrameSerializer, PlanSerializer
from rest_framework import status

@api_view(['GET'])
def get_video_uploads(request, plan_id):
    try:
        # Get the plan details
        plan = get_object_or_404(Plan, id=plan_id)

        # Get all video frames associated with the plan
        frames = VideoUpload.objects.filter(plan_id=plan_id)
        
        # Serialize both the plan and video frames data
        plan_serializer = PlanSerializer(plan)
        frame_serializer = VideoDateSerializer(frames, many=True)

        # Combine the serialized data into one response
        response_data = {
            'plan': plan_serializer.data,
            'video_frames': frame_serializer.data
        }

        return Response(response_data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import VideoUpload

def get_video_upload_date(request, video_id):
    # Get the video object by ID or return a 404 if not found
    video = get_object_or_404(VideoUpload, id=video_id)
    
    # Prepare the data to be returned in JSON format
    data = {
        'upload_date': video.upload_date,
    }
    
    # Return the data as a JSON response
    return JsonResponse(data)
