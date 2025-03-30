from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Device, GPSData,CustomUser
from .serializers import CustomUserSerializer, DeviceSerializer, GPSDataSerializer
from django.contrib.auth.hashers import make_password, check_password


@api_view(["POST"])
def create_user(request):
    """
    API to register a new user.
    """
    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.validated_data['password'] = make_password(serializer.validated_data['password'])  # Hash the password before saving
        user = CustomUser.objects.create(**serializer.validated_data)
        # serializer.save()
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
        
        user = CustomUser.objects.filter(email=email).first()
        print(user)
        if user:
            devices = list(Device.objects.filter(user=user).values_list("device", flat=True))
            return Response({"email": email, "devices": devices}, status=status.HTTP_200_OK)
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
    elif request.method == "POST":
        identifier = request.data.get("identifier")  # Can be username or email
        password = request.data.get("password")
        print(identifier,password)
        if not identifier or not password:
            return Response({"error": "Both identifier and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        user = CustomUser.objects.filter(email=identifier).first() if "@" in identifier else CustomUser.objects.filter(username=identifier).first()
        print(user)
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

from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes


from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import CustomUserSerializer  # Ensure correct import

# CustomUser = get_user_model()  # Get custom user model dynamically

@permission_classes([AllowAny])
@api_view(['POST'])
def login_user(request):
    try:
        email = request.data.get('email')
        password = request.data.get('password')
        print(email,password)
        if not email or not password:
            return Response({"detail": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Normalize email and fetch user
        user = CustomUser.objects.filter(email__iexact=email).first()
        # user = CustomUser.objects.filter(email=email).first()  # Without `iexact
        print(user)
        if not user:
            return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

        # Check password (Ensure passwords are hashed)
        if not user.check_password(password):
            print('error')
            return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        # Serialize user data
        serializer = CustomUserSerializer(user)

        # Return response
        response_data = {
            "access": access_token,
            "refresh": refresh_token,
            "success": "Login successful",
            "user_id": user.id,
            "user": serializer.data,  # Include user data
            "status": "success"
        }

        return Response(response_data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {"error": "Internal server error", "detail": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
