from datetime import timedelta
from time import timezone
from tokenize import Token
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
        # refresh = refresh_token.for_user(user)
        # access_token = str(refresh.access_token)
        # refresh_token = str(refresh)

        # Serialize user data
        serializer = CustomUserSerializer(user)

        # Return response
        response_data = {
            # "access": access_token,
            # "refresh": refresh_token,
            "success": "Login successful",
            "user_id": user.id,
            "user": serializer.data,  # Include user data
            "status": "success"
        }
        print(response_data)
        return Response(response_data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {"error": "Internal server error", "detail": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )




@api_view(['GET'])
def get_devices(request):
    device = GPSData.objects.all()
    serializer = GPSDataSerializer(device, many=True)
    return Response(serializer.data, status = status.HTTP_200_OK)



@api_view(['POST'])
def save_gps_data(request):
    device_id = request.data.get('device_id')
    latitude = request.data.get('latitude')
    longitude = request.data.get('longitude')
    speed = request.data.get('speed_kmh', 0)
    engine_status = request.data.get('engine_status', 0)

    if not all([device_id, latitude, longitude]):
        return Response({"error": "device_id, latitude and longitude are required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        device = Device.objects.get(id=device_id)
    except Device.DoesNotExist:
        return Response({"error": "Device not found"}, status=status.HTTP_404_NOT_FOUND)

    now = timezone.now()
    timestamp_str = now.strftime('%Y-%m-%d %H:%M:%S')
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)

    gps_entry = GPSData.objects.filter(device=device, date__range=(today_start, today_end)).first()

    if gps_entry:
        gps_entry.latitude.append(latitude)
        gps_entry.longitude.append(longitude)
        gps_entry.speed_kmh.append(speed)
        gps_entry.engine_status.append(engine_status)
        gps_entry.timestamps.append(timestamp_str)
        gps_entry.save()
    else:
        gps_entry = GPSData.objects.create(
            device=device,
            latitude=[latitude],
            longitude=[longitude],
            speed_kmh=[speed],
            engine_status=[engine_status],
            timestamps=[timestamp_str]
        )

    return Response({"message": "GPS data saved successfully"}, status=status.HTTP_201_CREATED)



@api_view(['GET'])
def get_device_gps_data(request):
    device_id = request.query_params.get('device_id')
    try:
        device = Device.objects.get(id=device_id)
    except Device.DoesNotExist:
        return Response({"error": "Device not found"}, status=status.HTTP_404_NOT_FOUND)

    # Fetch GPSData for this device, ordered by date descending
    gps_data_entries = GPSData.objects.filter(device=device).order_by('-date')

    result = []
    for entry in gps_data_entries:
        result.append({
            "latitude": entry.latitude,
            "longitude": entry.longitude,
            "speed_kmh": entry.speed_kmh,
            "engine_status": entry.engine_status,
            "max_speed": entry.max_speed,
            "battery_level": entry.battery_level,
            "ignition_on": entry.ignition_on,
            "timestamp": entry.date,
        })

    return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_user_gps_data(request, user_id):
    try:
        # Get all devices linked to this user
        devices = Device.objects.filter(user_id=user_id)
        if not devices.exists():
            return Response({"message": "No devices found for this user"}, status=status.HTTP_404_NOT_FOUND)

        # Get GPS data for those devices, sorted by date descending
        gps_data_entries = GPSData.objects.filter(device__in=devices).order_by('-date')

        if not gps_data_entries.exists():
            return Response({"message": "No GPS data found for this user"}, status=status.HTTP_404_NOT_FOUND)

        result = []
        for entry in gps_data_entries:
            # Check if timestamps array is not empty
            if entry.timestamps and len(entry.timestamps) > 0:
                # Zip all arrays together with timestamp as the primary sort key
                data_points = list(zip(
                    entry.timestamps,
                    entry.latitude,
                    entry.longitude,
                    entry.speed_kmh,
                    entry.engine_status
                ))

                # Sort by timestamp descending
                data_points.sort(key=lambda x: x[0], reverse=True)

                # Unzip sorted data
                sorted_timestamps, sorted_latitude, sorted_longitude, sorted_speed, sorted_engine = zip(*data_points) if data_points else ([], [], [], [], [])

                result.append({
                    "device_id": entry.device.id,
                    "coordinates": list(zip(sorted_latitude, sorted_longitude)),
                    "speed_kmh": list(sorted_speed),
                    "engine_status": list(sorted_engine),
                    "timestamps": list(sorted_timestamps),
                    "max_speed": entry.max_speed,
                    "battery_level": entry.battery_level,
                    "ignition_on": entry.ignition_on,
                    "timestamp": entry.date.strftime('%Y-%m-%d %H:%M:%S'),
                })
            else:
                # Handle case where timestamps array is empty
                result.append({
                    "device_id": entry.device.id,
                    "coordinates": [],
                    "speed_kmh": [],
                    "engine_status": [],
                    "timestamps": [],
                    "max_speed": entry.max_speed,
                    "battery_level": entry.battery_level,
                    "ignition_on": entry.ignition_on,
                    "timestamp": entry.date.strftime('%Y-%m-%d %H:%M:%S'),
                })

        if not result:
            return Response({"message": "No valid GPS data found for this user."}, status=status.HTTP_404_NOT_FOUND)

        return Response(result, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


from django.utils.dateparse import parse_date
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import GPSData, Device

from django.utils.dateparse import parse_datetime
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import GPSData, Device

@api_view(['POST'])
def update_gps_data(request):
    data = request.data
    device_id = data.get('id')
    name = data.get('name')  # TN 23 DS 2233

    device, created = Device.objects.get_or_create(device=device_id)

    # Update name if not set or changed
    if name and (not device.name or device.name != name):
        device.name = name
        device.save()

    gps_data, _ = GPSData.objects.get_or_create(device=device)

    gps_data.latitude.append(float(data.get('latitude')))
    gps_data.longitude.append(float(data.get('longitude')))
    gps_data.battery_level.append(data.get('battery_level'))
    gps_data.ignition_on.append(data.get('ignition_on'))
    gps_data.speed_kmh.append(data.get('speed_kmh'))
    gps_data.max_speed.append(data.get('max_speed'))

    gps_data.save()

    return Response({'status': 'GPS data updated successfully'})


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import GPSData
from .serializers import GPSDataSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import GPSData, Device
from datetime import date
from django.utils.timezone import now

@api_view(['POST'])
def post_gps_data(request):
    data = request.data

    device_id = data.get('device')
    if not device_id:
        return Response({'error': 'Device ID is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        device = Device.objects.get(id=device_id)
    except Device.DoesNotExist:
        return Response({'error': 'Device not found'}, status=status.HTTP_404_NOT_FOUND)

    # Get today's GPSData entry if exists
    today = date.today()
    gps_data = GPSData.objects.filter(device=device, date__date=today).first()

    if not gps_data:
        gps_data = GPSData.objects.create(device=device)

    # Append data to existing JSON fields
    gps_data.latitude.extend(data.get('latitude', []))
    gps_data.longitude.extend(data.get('longitude', []))
    gps_data.engine_status.extend(data.get('engine_status', []))
    gps_data.speed_kmh.extend(data.get('speed_kmh', []))
    gps_data.max_speed.extend(data.get('max_speed', []))
    gps_data.battery_level.extend(data.get('battery_level', []))
    gps_data.ignition_on.extend(data.get('ignition_on', []))

    gps_data.save()

    return Response({'message': 'GPS data updated for today', 'device': device_id})


from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import GPSData, Device
from .serializers import GPSDataSerializer
@api_view(['POST'])
def get_filtered_gps_data(request):
    data = request.data
    device_id = data.get('device')
    name = data.get('name')

    if not device_id or not name:
        return Response({'error': 'Both device and name are required in the payload'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Get device by ID and name
        device = Device.objects.get(id=device_id, name=name)

        # Get latest GPSData record
        latest_gps_data = GPSData.objects.filter(device=device).order_by('-date').first()

        if latest_gps_data:
            # Extract last values safely
            response_data = {
                "device": device.id,
                "latitude": latest_gps_data.latitude[-1] if latest_gps_data.latitude else None,
                "longitude": latest_gps_data.longitude[-1] if latest_gps_data.longitude else None,
                "engine_status": latest_gps_data.engine_status[-1] if latest_gps_data.engine_status else None,
                "speed_kmh": latest_gps_data.speed_kmh[-1] if latest_gps_data.speed_kmh else None,
                "max_speed": latest_gps_data.max_speed[-1] if latest_gps_data.max_speed else None,
                "battery_level": latest_gps_data.battery_level[-1] if latest_gps_data.battery_level else None,
                "ignition_on": latest_gps_data.ignition_on[-1] if latest_gps_data.ignition_on else None,
                "date": latest_gps_data.date,
            }
            return Response(response_data)

        else:
            return Response({'error': 'No GPS data found for the specified device and name'}, status=status.HTTP_404_NOT_FOUND)

    except Device.DoesNotExist:
        return Response({'error': 'Device not found with the provided ID and name'}, status=status.HTTP_404_NOT_FOUND)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Device
from .serializers import DeviceSerializer

@api_view(['GET'])
def devices_by_user(request, user_id):
    devices = Device.objects.filter(user_id=user_id)
    serializer = DeviceSerializer(devices, many=True)
    return Response(serializer.data)
