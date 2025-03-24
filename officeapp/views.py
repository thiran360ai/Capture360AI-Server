from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from .models import Employee, Organization
from .serializers import EmployeeSerializer

# USER CREATION FUNCTION (POST)
@api_view(['POST'])
def create_user(request):
    try:
        data = request.data

        # Ensure organization exists
        try:
            organization = Organization.objects.get(key=data.get('organization_key'))
        except Organization.DoesNotExist:
            return Response({"error": "Invalid organization key"}, status=status.HTTP_400_BAD_REQUEST)

        # Create Employee
        employee = Employee.objects.create(
            email=data.get('email'),
            username=data.get('username'),
            password=make_password(data.get('password')),
            device_id=data.get('device_id'),
            role=data.get('role', 'member'),  # Default role = 'member'
            organization=organization,
            employee_id=data.get('employee_id'),
            name=data.get('name')
        )

        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


from django.contrib.auth import authenticate, get_user_model
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework import status

User = get_user_model()

@api_view(['POST'])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        user = Employee.objects.get(email=email)
        if user.check_password(password):
            # token, created = Token.objects.get_or_create(user=user)
            return Response({
                'message': 'Login successful!',
                # 'token': token.key,
                
                'user_id': user.id,
                'email': user.email,
                'role': user.role,
                'organization': user.organization.name,
                'device_id': user.device_id
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    except User.DoesNotExist:
        return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)




from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
from .models import Employee, Device

# Login API - POST Method
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
from .models import Employee, Device, Organization
from django.views.decorators.csrf import csrf_exempt
# Create Employee and Device API - POST Method
import json
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import Employee, Organization, Device

@method_decorator(csrf_exempt, name='dispatch')
class CreateEmployeeView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            email = data.get('email')
            username = data.get('username')
            employee_id = data.get('employee_id')
            organization_keys = data.get('organizations', [])  # Expecting a list
            password = data.get('password')
            device_id = data.get('device_id')
            name = data.get('name')

            if not all([email, employee_id, organization_keys, password, device_id, name, username]):
                return JsonResponse({"error": "All fields are required"}, status=400)

            # Ensure at least one valid organization exists
            organizations = Organization.objects.filter(key__in=organization_keys)
            if not organizations.exists():
                return JsonResponse({"error": "Invalid organization keys provided"}, status=404)

            # Create Employee
            employee = Employee.objects.create(
                email=email,
                employee_id=employee_id,
                name=name,
                username=username,
                device_id=device_id,
                is_active=False  # Default to inactive
            )
            employee.organizations.set(organizations)  # Assign multiple organizations
            employee.set_password(password)  # Hash the password
            employee.save()

            # Create Device
            Device.objects.create(
                device_id=device_id,
                user=employee,
                is_active=False
            )

            return JsonResponse({"message": "Employee and device created successfully"}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

# Login API - POST Method
@method_decorator(csrf_exempt, name='dispatch')
class InactiveEmployeeListView(View):
    def get(self, request, organization_key):
        try:
            # Filter Organization
            organization = Organization.objects.filter(key=organization_key).first()
            if not organization:
                return JsonResponse({"error": "Invalid organization key"}, status=404)

            # Filter Inactive Employees in the Organization
            inactive_employees = Employee.objects.filter(
                organization=organization,
                is_active=False
            ).values('email', 'employee_id', 'name', 'organization__name')

            if not inactive_employees:
                return JsonResponse({"error": "No inactive employees found"}, status=404)

            return JsonResponse({"inactive_employees": list(inactive_employees)}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class UpdateEmployeeStatusView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            employee_id = data.get('employee_id')
            is_active = data.get('is_active')  # Expecting True or False

            if not employee_id or is_active is None:
                return JsonResponse({"error": "Employee ID and is_active status are required"}, status=400)

            # Find the Employee
            employee = Employee.objects.filter(employee_id=employee_id).first()
            if not employee:
                return JsonResponse({"error": "Employee not found"}, status=404)

            # Update the 'is_active' status
            employee.is_active = bool(is_active)
            employee.save()

            status_message = "activated" if employee.is_active else "deactivated"
            return JsonResponse({"message": f"Employee successfully {status_message}."}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class EmployeeLoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            email = data.get('email')
            employee_id = data.get('employee_id')
            organization_key = data.get('organization')
            password = data.get('password')
            device_id = data.get('device_id')

            if not all([email, employee_id, organization_key, password, device_id]):
                return JsonResponse({"error": "All fields are required"}, status=400)

            # Verify Organization
            organization = Organization.objects.filter(key=organization_key).first()
            if not organization:
                return JsonResponse({"error": "Invalid organization key"}, status=404)

            # Verify Employee
            employee = Employee.objects.filter(
                email=email,
                employee_id=employee_id,
                organization=organization,
                is_active=True
            ).first()

            if not employee:
                return JsonResponse({"error": "Invalid credentials or inactive account"}, status=404)

            # Verify Password with Custom Authentication
            user = authenticate(request, email=email, password=password)
            if user:
                return JsonResponse({
                    "message": "Login successful",
                    "employee_id": employee.employee_id,
                    "name": employee.name,
                    "role": employee.role,
                }, status=200)
            else:
                return JsonResponse({"error": "Invalid password"}, status=401)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils import timezone
from .models import Employee, Attendance

import json
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .models import Attendance, Employee

# Start Attendanceimport json
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .models import Attendance, Employee

# Start Attendanceimport json
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .models import Attendance, Employee

# Start Attendance
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Attendance, Employee

# Start Attendance
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Attendance, Employee
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Start Attendance
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Attendance, Employee, Device

# import json
# from django.utils import timezone
# from django.http import JsonResponse
# from django.contrib.gis.geos import Point
# from math import radians, cos, sin, sqrt, atan2
# from rest_framework.decorators import api_view
# from .models import Device, Attendance, Organization

# def haversine(lat1, lon1, lat2, lon2):
#     """
#     Calculate the great-circle distance between two points using the Haversine formula.
#     """
#     R = 6371000  # Radius of the Earth in meters
#     lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

#     dlat = lat2 - lat1
#     dlon = lon2 - lon1

#     a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
#     c = 2 * atan2(sqrt(a), sqrt(1 - a))

#     return R * c  # Distance in meters

# @api_view(['POST'])
# def start_attendance(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             device_id = data.get('device_id')
#             user_latitude = float(data.get('latitude', 0))
#             user_longitude = float(data.get('longitude', 0))

#             # ✅ Check if the device exists
#             device = Device.objects.get(device_id=device_id)
#             employee = device.user

#             # ✅ Get Organization's location
#             organization = getattr(employee, 'organization', None)  # Handle missing relationship safely
#             if not organization:
#                 return JsonResponse({"error": "Organization not found for the employee"}, status=404)

#             org_latitude = organization.latitude
#             org_longitude = organization.longitude

#             # ✅ Validate organization coordinates
#             if org_latitude is None or org_longitude is None:
#                 return JsonResponse({"error": "Organization location is missing"}, status=400)

#             # ✅ Calculate distance
#             distance = haversine(user_latitude, user_longitude, org_latitude, org_longitude)

#             print(f"Distance from organization: {distance} meters")  # Debugging

#             if distance > 100:
#                 return JsonResponse({"error": "You are too far from the organization to start attendance."}, status=400)

#             # ✅ Start Attendance
#             today_attendance, created = Attendance.objects.get_or_create(
#                 employee=employee,
#                 date=timezone.now().date(),
#                 defaults={'logs': json.dumps([]), 'total_hours': 0}
#             )

#             logs = json.loads(today_attendance.logs)
#             logs.append({"action": "start", "time": str(timezone.now())})

#             today_attendance.logs = json.dumps(logs)
#             today_attendance.save()

#             return JsonResponse({"message": "Attendance started successfully"}, status=200)

#         except Device.DoesNotExist:
#             return JsonResponse({"error": "Device not found"}, status=404)

#         except ValueError:
#             return JsonResponse({"error": "Invalid latitude or longitude values"}, status=400)

#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)
import json
from django.utils import timezone
from django.http import JsonResponse
from math import radians, cos, sin, sqrt, atan2
from rest_framework.decorators import api_view
from .models import Device, Attendance, Organization

from math import radians, cos, sin, sqrt, atan2

import json
from django.utils import timezone
from django.http import JsonResponse
from math import radians, cos, sin, sqrt, atan2
from rest_framework.decorators import api_view
from .models import Device, Attendance, Organization

import json
from django.utils import timezone
from django.http import JsonResponse
from math import radians, cos, sin, sqrt, atan2
from rest_framework.decorators import api_view
from .models import Device, Attendance, Organization

def haversine(lat1, lon1, lat2, lon2):
    """Calculate distance between two lat/lon points using the Haversine formula."""
    R = 6371000  # Radius of the Earth in meters
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c  # Distance in meters

@api_view(['POST'])
def start_attendance(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            device_id = data.get('device_id')
            user_latitude = float(data.get('latitude'))
            user_longitude = float(data.get('longitude'))

            # ✅ Check if the device exists
            device = Device.objects.get(device_id=device_id)
            employee = device.user  # Assuming 'user' field is linked to Employee

            # ✅ Ensure the user is linked to at least one organization
            if not employee.organizations.exists():
                return JsonResponse({"error": "User is not linked to any Organization."}, status=400)

            # ✅ Loop through all organizations and check distance
            for organization in employee.organizations.all():
                if organization.latitude and organization.longitude:
                    distance = haversine(user_latitude, user_longitude, organization.latitude, organization.longitude)
                    print(f"Distance from {organization.name}: {distance} meters")  # Debugging

                    if distance <= 100:  # ✅ Allow attendance if within 100m of ANY organization
                        # ✅ Start Attendance
                        today_attendance, created = Attendance.objects.get_or_create(
                            employee=employee,
                            date=timezone.now().date(),
                            defaults={'logs': json.dumps([]), 'total_hours': 0}
                        )

                        logs = json.loads(today_attendance.logs)
                        logs.append({"action": "start", "time": str(timezone.now())})

                        today_attendance.logs = json.dumps(logs)
                        today_attendance.save()

                        return JsonResponse({"message": "Attendance started successfully"}, status=200)

            return JsonResponse({"error": "You are too far from all assigned organizations."}, status=400)

        except Device.DoesNotExist:
            return JsonResponse({"error": "Device not found"}, status=404)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


# @api_view(['POST'])
# def start_attendance(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             device_id = data.get('device_id')

#             device = Device.objects.get(device_id=device_id)
#             employee = device.user

#             today_attendance, created = Attendance.objects.get_or_create(
#                 employee=employee,
#                 date=timezone.now().date(),
#                 defaults={'logs': json.dumps([]), 'total_hours': 0}
#             )

#             logs = json.loads(today_attendance.logs)
#             logs.append({"action": "start", "time": str(timezone.now())})

#             today_attendance.logs = json.dumps(logs)
#             today_attendance.save()

#             return JsonResponse({"message": "Attendance started successfully"}, status=200)

#         except Device.DoesNotExist:
#             return JsonResponse({"error": "Device not found"}, status=404)

# Pause Attendance
import json
from django.utils import timezone
from django.http import JsonResponse
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from .models import Attendance

# Pause Attendance
@api_view(['POST'])
def pause_attendance(request):
    try:
        data = json.loads(request.body)
        device_id = data.get('device_id')

        attendance = Attendance.objects.get(
            employee__device__device_id=device_id,
            date=timezone.now().date()
        )

        logs = json.loads(attendance.logs)
        logs.append({"action": "pause", "time": str(timezone.now())})

        attendance.logs = json.dumps(logs)
        attendance.save()

        return JsonResponse({"message": "Attendance paused successfully"}, status=200)

    except Attendance.DoesNotExist:
        return JsonResponse({"error": "No active attendance found"}, status=400)

# Resume Attendance
@api_view(['POST'])
def resume_attendance(request):
    try:
        data = json.loads(request.body)
        device_id = data.get('device_id')

        attendance = Attendance.objects.get(
            employee__device__device_id=device_id,
            date=timezone.now().date()
        )

        logs = json.loads(attendance.logs)
        logs.append({"action": "resume", "time": str(timezone.now())})

        attendance.logs = json.dumps(logs)
        attendance.save()

        return JsonResponse({"message": "Attendance resumed successfully"}, status=200)

    except Attendance.DoesNotExist:
        return JsonResponse({"error": "No paused attendance found"}, status=400)

# Stop Attendance
@api_view(['POST'])
def stop_attendance(request):
    try:
        data = json.loads(request.body)
        device_id = data.get('device_id')

        attendance = Attendance.objects.get(
            employee__device__device_id=device_id,
            date=timezone.now().date()
        )

        logs = json.loads(attendance.logs)
        logs.append({"action": "stop", "time": str(timezone.now())})

        # ✅ Calculate total hours
        total_duration = 0
        last_start = None

        for log in logs:
            try:
                action = log['action']
                log_time = timezone.datetime.fromisoformat(log['time'].replace("Z", "+00:00"))  # ✅ Fixed ISO format issue

                if action in ['start', 'resume']:
                    last_start = log_time
                elif action in ['pause', 'stop'] and last_start:
                    total_duration += (log_time - last_start).total_seconds() / 3600
                    last_start = None

            except Exception as e:
                print(f"Error processing log: {log}, Error: {e}")  # Debugging
                continue

        attendance.logs = json.dumps(logs)
        attendance.total_hours = round(total_duration, 2)
        attendance.save()

        return JsonResponse({
            "message": "Attendance stopped successfully",
            "total_hours": attendance.total_hours
        }, status=200)

    except Attendance.DoesNotExist:
        return JsonResponse({"error": "No active attendance found"}, status=400)
