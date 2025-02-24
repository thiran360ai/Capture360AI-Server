from datetime import datetime
import traceback
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from django.utils.timezone import now
from rest_framework.decorators import api_view
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *


def get_current_date():
    return now().date()


class AttendanceAPIView(APIView):
    def post(self, request, action):
        serializer = AttendanceSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        print(action)
        device_id = serializer.validated_data['device_id']

        if action == 'start':
            previous_attendance = Attendance.objects.filter(
                device_id=device_id, stop_time__isnull=True, pause_time__isnull=True
            ).first()

            if previous_attendance:
                return Response({'error': 'Session already active. Cannot start again.'},
                                status=status.HTTP_400_BAD_REQUEST)

            last_stopped_attendance = Attendance.objects.filter(
                device_id=device_id, stop_time__isnull=False
            ).order_by('-stop_time').first()

            if last_stopped_attendance and last_stopped_attendance.stop_time.date() == timezone.now().date():
                return Response({'error': 'Session already completed today. Cannot start again.'},
                                status=status.HTTP_400_BAD_REQUEST)

            attendance, created = Attendance.objects.get_or_create(
                device_id=device_id,
                defaults={'start_time': timezone.now(), 'total_hours': timedelta(0)}
            )

            # Reserialize after saving
            formatted_serializer = AttendanceSerializer(attendance)

            if not created and attendance.pause_time:
                attendance.total_hours += timezone.now() - attendance.pause_time
                attendance.start_time = timezone.now()
                attendance.pause_time = None
                attendance.save()
                formatted_serializer = AttendanceSerializer(attendance)  # Reserialize after update

                return Response({
                    'message': 'Tracking resumed',
                    'start_time': formatted_serializer.data['start_time']  # ✅ Formatted time
                }, status=status.HTTP_200_OK)

            return Response({
                'message': 'Tracking started',
                'start_time': formatted_serializer.data['start_time']  # ✅ Formatted time
            }, status=status.HTTP_200_OK)

        elif action == 'pause':
            try:
                attendance = Attendance.objects.get(device_id=device_id, stop_time__isnull=True)

                if attendance.start_time is None:
                    return Response({'error': 'Start time not found'}, status=status.HTTP_400_BAD_REQUEST)

                if attendance.pause_time:
                    return Response({'error': 'Already paused. Resume before pausing again.'},
                                    status=status.HTTP_400_BAD_REQUEST)

                attendance.pause_time = timezone.now()
                time_spent = attendance.pause_time - attendance.start_time
                attendance.total_hours += time_spent
                attendance.save()

                formatted_serializer = AttendanceSerializer(attendance)

                return Response({
                    'message': 'Tracking paused',
                    'pause_time': formatted_serializer.data['pause_time'],  # ✅ Formatted time
                    'total_hours': str(attendance.total_hours)
                }, status=status.HTTP_200_OK)

            except Attendance.DoesNotExist:
                return Response({'error': 'No active session found'}, status=status.HTTP_400_BAD_REQUEST)

        elif action == 'stop':
            try:
                attendance = Attendance.objects.get(device_id=device_id, stop_time__isnull=True)

                if attendance.start_time is None:
                    return Response({'error': 'Start time not found'}, status=status.HTTP_400_BAD_REQUEST)

                if attendance.total_hours is None:
                    attendance.total_hours = timedelta(0)

                attendance.stop_time = timezone.now()

                if attendance.pause_time:
                    time_spent = attendance.pause_time - attendance.start_time
                else:
                    time_spent = attendance.stop_time - attendance.start_time

                attendance.total_hours += time_spent
                attendance.save()

                formatted_serializer = AttendanceSerializer(attendance)

                formatted_total_hours = str(attendance.total_hours).split('.')[0]
                return Response({
                    'message': 'Tracking stopped',
                    'stop_time': formatted_serializer.data['stop_time'],  # ✅ Formatted time
                    'total_hours': formatted_total_hours
                }, status=status.HTTP_200_OK)

            except Attendance.DoesNotExist:
                return Response({'error': 'No active session found'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_attendance_by_user_device_and_date_range(request):
    try:
        # ✅ Extract parameters from request
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')
        device_id = request.query_params.get('device_id')
        user_id = request.query_params.get('user_id')
        # ✅ Validate required parameters
        if not all([start_date_str, end_date_str, device_id]):
            return Response({"error": "Missing required parameters: start_date, end_date,or device_id"},
                            status=status.HTTP_400_BAD_REQUEST)

        # ✅ Convert string dates to datetime objects
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d') + timedelta(days=1)
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        # ✅ Ensure start_date is before or equal to end_date
        if start_date > end_date:
            return Response({"error": "start_date cannot be after end_date."}, status=status.HTTP_400_BAD_REQUEST)

        # ✅ Fetch attendance records
        attendance_records = Attendance.objects.filter(
            user_id=user_id, device_id=device_id, start_time__date__range=[start_date, end_date]
        )
        print(attendance_records)
        if not attendance_records.exists():
            return Response({"message": "No attendance records found."}, status=status.HTTP_404_NOT_FOUND)

        # ✅ Serialize and return attendance records
        serializer = AttendanceSerializer(attendance_records, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# payload=http://127.0.0.1:8000/myapp/attendance/?device_id=4&start_date=2025-02-01&end_date=2025-02-28


@api_view(['GET'])
def get_users_present_on_date(request):
    try:
        # ✅ Extract date parameter from request
        date_str = request.query_params.get('date')

        # ✅ Validate if date is provided
        if not date_str:
            return Response({"error": "Missing required parameter: date"}, status=status.HTTP_400_BAD_REQUEST)

        # ✅ Convert string date to datetime object
        try:
            selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        # ✅ Fetch all users who have a start_time on the given date
        attendance_records = Attendance.objects.filter(start_time__date=selected_date)

        if not attendance_records.exists():
            return Response({"message": "No users were present on this date."}, status=status.HTTP_404_NOT_FOUND)

        # ✅ Serialize and return attendance records
        serializer = AttendanceSerializer(attendance_records, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST', 'GET'])
def create_user(request):
    """
    API endpoint to create a new employee.

    Accepts the following parameters in the request body:
    - username: The username of the employee.
    - password: The password of the employee.
    - mobile: The mobile number of the employee.
    - email: The email of the employee.
    - role: The role of the employee.
    - location: The location of the employee.

    Returns a JSON object with the newly created employee details if the creation is successful.
    Returns a JSON object with an error message if the creation fails.

    Also handles GET requests and returns a list of all employees if a GET request is sent.
    """
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # Hash the password before saving
            serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
            serializer.validated_data['success'] = True
            user = User.objects.create(**serializer.validated_data)
            return Response(
                {'message': 'User created successfully', "user_id": user.id, 'user': serializer.data['username'],
                 'success': serializer.data['success']}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        # Return a response for GET request if needed
        # Example: Return a list of employees (or whatever data makes sense for your app)
        employees = User.objects.all()
        serializer = UserSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # In case a request method other than POST or GET is sent, you could return a method not allowed response.
    return Response({'message': 'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def Emp_login(request):
    """
    API endpoint for employee login.

    Accepts the following parameters in the request body:
    - email: The email of the employee attempting to login.
    - password: The password of the employee.

    Returns a JSON response containing a message and employee details if the login is successful.
    Returns a JSON object with an error message if the login fails.

    Returns:
    - 200 OK: A JSON object with a success message, employee ID, username, and role if credentials are valid.
    - 400 Bad Request: A JSON object with an error message if credentials are invalid.
    - 500 Internal Server Error: A JSON object with an error message if an unexpected error occurs.
    """

    try:
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        if check_password(password, user.password):
            # Change success to True if password is matched
            return JsonResponse({
                'Message': 'Login successfully',
                'success': True,  # Set success to True
                'id': user.id,
                'username': user.username,
                'role': user.role
            }, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'error': 'Invalid credentials', 'success': False}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        # Print the full traceback to debug the issue
        traceback.print_exc()
        return JsonResponse({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
