from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Device, GPSData
from .serializers import CustomUserSerializer, DeviceSerializer, GPSDataSerializer

User = get_user_model()

@api_view(["POST"])
def create_user(request):
    """
    API to register a new user.
    """
    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def create_device(request):
    """
    API to register a device for a user.
    """
    serializer = DeviceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Device registered successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def create_gps_data(request):
    """
    API to store GPS data for a device.
    """
    serializer = GPSDataSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "GPS Data stored successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from django.utils.dateparse import parse_datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Device, GPSData
from .serializers import GPSDataSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils.dateparse import parse_datetime
from .models import GPSData, Device
from .serializers import GPSDataSerializer

@api_view(["GET"])
def get_gps_data(request, device_id):
    """
    API to get all GPS data for a specific device within an optional time range.
    If start_timestamp and end_timestamp are provided, filters data in that range.
    """
    try:
        device = Device.objects.get(device=device_id)  # Ensure device exists

        # Get query parameters
        start_timestamp = request.GET.get("start_timestamp")  # Example: "2025-03-27T12:00:00Z"
        end_timestamp = request.GET.get("end_timestamp")  # Example: "2025-03-27T18:00:00Z"

        # Convert timestamps to datetime objects
        if start_timestamp:
            start_timestamp = parse_datetime(start_timestamp)
        if end_timestamp:
            end_timestamp = parse_datetime(end_timestamp)

        # Filter GPS data based on time range
        gps_data = GPSData.objects.filter(device=device)
        if start_timestamp and end_timestamp:
            gps_data = gps_data.filter(timestamp__range=(start_timestamp, end_timestamp))
        elif start_timestamp:
            gps_data = gps_data.filter(timestamp__gte=start_timestamp)
        elif end_timestamp:
            gps_data = gps_data.filter(timestamp__lte=end_timestamp)

        # Serialize and return response
        serializer = GPSDataSerializer(gps_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Device.DoesNotExist:
        return Response({"error": "Device not found"}, status=status.HTTP_404_NOT_FOUND)

from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework import status
from .models import CustomUser, Device
from rest_framework.authtoken.models import Token  # ✅ Correct import

# @api_view(["POST"])
# def login_view(request):
#     """
#     Login API using only username and password authentication.
#     """
#     username = request.data.get("username")
#     password = request.data.get("password")

#     user = authenticate(username=username, password=password)

#     if user:
#         # Generate or retrieve authentication token
#         token, _ = Token.objects.get_or_create(user=user)

#         return Response({
#             "message": "Login successful",
#             "token": token.key,
#             "user": {
#                 "id": user.id,
#                 "username": user.username,
#                 "email": user.email
#             }
#         }, status=status.HTTP_200_OK)
    
#     return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

from django.contrib.auth import authenticate, get_user_model
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework import status
from .models import Device

User = get_user_model()

@api_view(["POST", "GET"])
# def login_or_fetch_devices(request):
def login_view(request):
    """
    Handles:
    - **POST**: Login using username or email.
    - **GET**: Fetch all linked device IDs using email.
    """
    if request.method == "GET":
        email = request.GET.get("email")
        if not email:
            return Response({"error": "Email parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.filter(email=email).first()
        if user:
            devices = list(Device.objects.filter(user=user).values_list("device", flat=True))
            return Response({"email": email, "devices": devices}, status=status.HTTP_200_OK)
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
    elif request.method == "POST":
        identifier = request.data.get("identifier")  # Can be username or email
        password = request.data.get("password")

        if not identifier or not password:
            return Response({"error": "Both identifier and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=identifier).first() if "@" in identifier else User.objects.filter(username=identifier).first()
        if user and user.check_password(password):
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "message": "Login successful",
                "token": token.key,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                }
            }, status=status.HTTP_200_OK)

        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
