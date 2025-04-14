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
                # 'organization': user.organization.name,
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
class InactiveEmployeesView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            organization_keys = data.get('organizations', [])

            if not organization_keys:
                return JsonResponse({"error": "At least one organization key is required"}, status=400)

            # Get Organizations
            organizations = Organization.objects.filter(key__in=organization_keys)
            if not organizations.exists():
                return JsonResponse({"error": "No matching organizations found"}, status=404)

            # Get Inactive Employees in these Organizations
            inactive_employees = Employee.objects.filter(
                organizations__in=organizations, 
                is_active=False
            ).distinct()

            # Prepare Response
            employees_data = [
                {
                    "id":emp.id,
                    "employee_id": emp.employee_id,
                    "name": emp.name,
                    "email": emp.email,
                    "role": emp.role,
                    "organizations": list(emp.organizations.values_list("name", flat=True))
                }
                for emp in inactive_employees
            ]

            return JsonResponse({"inactive_employees": employees_data}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
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
            password = data.get('password')

            if not email or not password:
                return JsonResponse({"error": "Email and password are required"}, status=400)

            # Verify Employee
            employee = Employee.objects.filter(email=email, is_active=True).first()
            if not employee:
                return JsonResponse({"error": "Invalid credentials or inactive account"}, status=404)

            # Verify Password
            from django.contrib.auth.hashers import check_password
            if check_password(password, employee.password):
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

from django.http import JsonResponse
from django.utils import timezone
import json
from django.utils.timezone import now
import json
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import Attendance, Device
from .utils import haversine  # Assuming you have a haversine function

from datetime import datetime
from django.utils.timezone import now
import json
from django.http import JsonResponse
from rest_framework.decorators import api_view
from officeapp.models import Attendance, Device  # Update with your actual app name

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

            # ✅ Ensure the device is active
            if not device.is_active:
                return JsonResponse({"error": "Device is inactive. Attendance cannot be started."}, status=403)

            employee = device.user  # Assuming 'user' field is linked to Employee

            # ✅ Ensure the employee is active
            if not employee.is_active:
                return JsonResponse({"error": "Employee is inactive. Attendance cannot be started."}, status=403)

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
                            date=now().date(),
                            defaults={'logs': json.dumps([]), 'total_hours': 0}
                        )

                        logs = json.loads(today_attendance.logs)
                        current_time = now().strftime("%Y-%m-%d %H:%M:%S")  # ✅ Include seconds
                        logs.append({"action": "start", "time": current_time})

                        today_attendance.logs = json.dumps(logs)
                        today_attendance.save()

                        return JsonResponse({
                            "message": "Attendance started successfully"
                        }, status=200)

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
# @api_view(['POST'])
# def pause_attendance(request):
#     try:
#         data = json.loads(request.body)
#         device_id = data.get('device_id')

#         attendance = Attendance.objects.get(
#             employee__device__device_id=device_id,
#             date=timezone.now().date()
#         )

#         logs = json.loads(attendance.logs)
#         logs.append({"action": "pause", "time": str(timezone.now())})

#         attendance.logs = json.dumps(logs)
#         attendance.save()

#         return JsonResponse({"message": "Attendance paused successfully"}, status=200)

#     except Attendance.DoesNotExist:
#         return JsonResponse({"error": "No active attendance found"}, status=400)
from django.utils.timezone import now
import json
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import Attendance

@api_view(['POST'])
def pause_attendance(request):
    try:
        data = json.loads(request.body)
        device_id = data.get('device_id')

        attendance = Attendance.objects.get(
            employee__device__device_id=device_id,
            date=now().date()
        )

        logs = json.loads(attendance.logs)
        logs.append({"action": "pause", "time": now().strftime("%Y-%m-%d %H:%M:%S")})  # Including seconds

        attendance.logs = json.dumps(logs)
        attendance.save()

        return JsonResponse({"message": "Attendance paused successfully", "timestamp": now().strftime("%Y-%m-%d %H:%M:%S")}, status=200)

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
from django.utils import timezone
import json
from django.http import JsonResponse
from rest_framework.decorators import api_view
# from your_app.models import Attendance  # Update with your actual app name

@api_view(['POST'])
def stop_attendance(request):
    try:
        data = json.loads(request.body)
        device_id = data.get('device_id')

        # Get today's attendance
        attendance = Attendance.objects.get(
            employee__device__device_id=device_id,
            date=timezone.now().date()
        )

        logs = json.loads(attendance.logs)
        filtered_logs = []
        last_start = None
        total_duration = 0

        for log in logs:
            action = log['action']
            
            # ✅ Convert log time to a timezone-aware datetime
            log_time = timezone.make_aware(
                timezone.datetime.fromisoformat(log['time'].replace("Z", "+00:00"))
            ) if timezone.is_naive(timezone.datetime.fromisoformat(log['time'].replace("Z", "+00:00"))) else timezone.datetime.fromisoformat(log['time'].replace("Z", "+00:00"))

            if action in ['start', 'resume']:
                last_start = log_time
                filtered_logs.append(log)

            elif action in ['pause', 'stop']:
                if last_start:  # Only pair valid start-stop times
                    total_duration += (log_time - last_start).total_seconds() / 3600
                    last_start = None

                # ✅ Keep only the latest "stop" log
                if action == 'stop':
                    filtered_logs = [log for log in filtered_logs if log['action'] != 'stop']
                
                filtered_logs.append(log)

        # ✅ Append new "stop" action with timezone-aware datetime
        stop_log = {"action": "stop", "time": str(timezone.now())}
        filtered_logs.append(stop_log)

        # ✅ Save the updated logs and total hours
        attendance.logs = json.dumps(filtered_logs)
        attendance.total_hours = round(total_duration, 2)
        attendance.save()

        return JsonResponse({
            "message": "Attendance stopped successfully",
            "total_hours": attendance.total_hours
        }, status=200)

    except Attendance.DoesNotExist:
        return JsonResponse({"error": "No active attendance found"}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class ActiveDevicesView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            organization_keys = data.get('organizations', [])
            is_active = data.get('is_active', True)  # Default: Active devices only

            if not organization_keys:
                return JsonResponse({"error": "At least one organization key is required"}, status=400)

            # Get Organizations
            organizations = Organization.objects.filter(key__in=organization_keys)
            if not organizations.exists():
                return JsonResponse({"error": "No matching organizations found"}, status=404)

            # Get Employees in these Organizations
            employees = Employee.objects.filter(organizations__in=organizations).distinct()

            # Get Devices linked to these Employees and Filter by is_active
            devices = Device.objects.filter(user__in=employees, is_active=is_active)

            # Prepare Response
            devices_data = [
                {
                    
                    
                    
                    "device_id": device.device_id,
                    "user": device.user.id,
                    "email": device.user.email,
                    "organization": list(device.user.organizations.values_list("name", flat=True)),
                    "is_active": device.is_active
                }
                for device in devices
            ]

            return JsonResponse({"devices": devices_data}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Employee

@method_decorator(csrf_exempt, name='dispatch')
class CheckUserActiveStatusView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')

            if not user_id:
                return JsonResponse({"error": "User ID is required"}, status=400)

            # Check if the user exists
            employee = Employee.objects.filter(id=user_id).first()

            if not employee:
                return JsonResponse({"error": "User not found"}, status=404)

            # Return active status
            return JsonResponse({
                "user_id": employee.id,
                "name": employee.name,
                "email": employee.email,
                "is_active": employee.is_active
            }, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Employee

@method_decorator(csrf_exempt, name='dispatch')
class UpdateUserActiveStatusView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            is_active = data.get('is_active')

            if user_id is None or is_active is None:
                return JsonResponse({"error": "User ID and is_active field are required"}, status=400)

            # Find user
            employee = Employee.objects.filter(id=user_id).first()

            if not employee:
                return JsonResponse({"error": "User not found"}, status=404)

            # Update is_active status
            employee.is_active = is_active
            employee.save()

            return JsonResponse({
                "message": "User active status updated successfully",
                "user_id": employee.id,
                "name": employee.name,
                "is_active": employee.is_active
            }, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Device, Employee

@method_decorator(csrf_exempt, name='dispatch')
class UpdateDeviceActiveStatusView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            device_id = data.get('device_id')
            is_active = data.get('is_active')

            if not all([user_id, device_id, is_active is not None]):
                return JsonResponse({"error": "user_id, device_id, and is_active field are required"}, status=400)

            # Check if the user exists
            employee = Employee.objects.filter(id=user_id).first()
            if not employee:
                return JsonResponse({"error": "User not found"}, status=404)

            # Check if the device exists for the given user
            device = Device.objects.filter(device_id=device_id, user=employee).first()
            if not device:
                return JsonResponse({"error": "Device not found for this user"}, status=404)

            # Update is_active status
            device.is_active = is_active
            device.save()

            return JsonResponse({
                "message": "Device active status updated successfully",
                "device_id": device.device_id,
                "user_id": employee.id,
                "user_name": employee.name,
                "is_active": device.is_active
            }, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Employee

@method_decorator(csrf_exempt, name='dispatch')
class CheckEmployeeStatusView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            email = data.get('email')

            if not email:
                return JsonResponse({"error": "Email is required"}, status=400)

            # Check if the employee exists
            employee = Employee.objects.filter(email=email).first()
            if not employee:
                return JsonResponse({"error": "User not found"}, status=404)

            return JsonResponse({
                "email": employee.email,
                "name": employee.name,
                "is_active": employee.is_active
            }, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Device

@method_decorator(csrf_exempt, name='dispatch')
class CheckDeviceStatusView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            device_id = data.get('device_id')

            if not device_id:
                return JsonResponse({"error": "Device ID is required"}, status=400)

            # Check if the device exists
            device = Device.objects.filter(device_id=device_id).first()
            if not device:
                return JsonResponse({"error": "Device not found"}, status=404)

            return JsonResponse({
                "device_id": device.device_id,
                "user_id": device.user.id,
                "user_name": device.user.name,
                "user_email": device.user.email,
                "is_active": device.is_active
            }, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
from .models import Employee, Attendance

@method_decorator(csrf_exempt, name='dispatch')
class GetTotalHoursView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            email = data.get('email')
            from_date = data.get('from_date')
            end_date = data.get('end_date')

            if not email or not from_date or not end_date:
                return JsonResponse({"error": "Email, from_date, and end_date are required"}, status=400)

            # Convert string dates to datetime objects
            try:
                from_date = datetime.strptime(from_date, "%Y-%m-%d").date()
                end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
            except ValueError:
                return JsonResponse({"error": "Invalid date format. Use YYYY-MM-DD"}, status=400)

            # Verify Employee
            employee = Employee.objects.filter(email=email).first()
            if not employee:
                return JsonResponse({"error": "Employee not found"}, status=404)

            # Fetch attendance records within date range
            attendance_records = Attendance.objects.filter(
                employee=employee, 
                date__range=[from_date, end_date]
            )

            total_hours = sum(record.total_hours for record in attendance_records)

            return JsonResponse({
                "employee_id": employee.id,
                "employee_name": employee.name,
                "email": employee.email,
                "total_hours": total_hours
            }, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils.dateparse import parse_date
from .models import Employee, Attendance


@api_view(['POST'])
def get_daily_attendance(request):
    email = request.data.get('email')
    date_str = request.data.get('date')  # Expected format: 'YYYY-MM-DD'

    if not email or not date_str:
        return Response({"error": "email and date are required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        date = parse_date(date_str)
        employee = Employee.objects.get(email=email)
    except Employee.DoesNotExist:
        return Response({"error": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    try:
        attendance = Attendance.objects.get(employee=employee, date=date)
        return Response({
            "email": email,
            "date": attendance.date,
            "logs": attendance.logs,
            "total_hours": attendance.total_hours
        }, status=status.HTTP_200_OK)
    except Attendance.DoesNotExist:
        return Response({"message": "No attendance found for this date."}, status=status.HTTP_204_NO_CONTENT)


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils.dateparse import parse_date
from .models import Employee, Attendance, Organization


@api_view(['POST'])
def organization_daily_attendance(request):
    organization_id = request.data.get('organization_id')
    date_str = request.data.get('date')

    if not organization_id or not date_str:
        return Response({"error": "organization_id and date are required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        date = parse_date(date_str)
        organization = Organization.objects.get(id=organization_id)
    except Organization.DoesNotExist:
        return Response({"error": "Organization not found."}, status=status.HTTP_404_NOT_FOUND)

    employees = Employee.objects.filter(organizations=organization)

    total_hours = 0
    attendance_data = []

    for emp in employees:
        try:
            attendance = Attendance.objects.get(employee=emp, date=date)
            total_hours += attendance.total_hours
            attendance_data.append({
                "employee_name": emp.name,
                "email": emp.email,
                "total_hours": attendance.total_hours,
                "logs": attendance.logs
            })
        except Attendance.DoesNotExist:
            continue  # No attendance for that day

    return Response({
        "organization": organization.name,
        "date": date,
        "total_employees": len(attendance_data),
        "total_hours": total_hours,
        "attendance_details": attendance_data
    }, status=status.HTTP_200_OK)
