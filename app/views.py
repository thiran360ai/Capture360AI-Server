from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from geopy.distance import geodesic
from .models import  *
from .serializers import *

# # User Registration
# @api_view(['POST', 'GET'])
# @permission_classes([AllowAny])
# def register_user(request):
#     if request.method == 'POST':
#         data = request.data
#         data['password'] = make_password(data['password'])
#         serializer = UserSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'GET':
#         users = User.objects.all()
#         serializer = UserSerializer(users, many=True)
#         return Response(serializer.data)



from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

User = get_user_model()
@api_view(['GET', 'POST'])
def register_user(request):
    if request.method == 'GET':
        users = User.objects.filter(is_employee=False).values('id', 'email', 'username', 'mobile_number', 'latitude', 'longitude', 'address')
        return Response(users, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        data = request.data  # Accepts both single and bulk requests

        if isinstance(data, list):  # Bulk Registration
            users = []
            for user_data in data:
                user = User.objects.create_user(
                    email=user_data['email'],
                    username=user_data['username'],
                    mobile_number=user_data['mobile_number'],
                    password=user_data['password'],
                    latitude=user_data.get('latitude', None),
                    longitude=user_data.get('longitude', None),
                    address=user_data.get('address', "")
                )
                users.append({"email": user.email, "message": "User registered successfully"})
            return Response(users, status=status.HTTP_201_CREATED)

        elif isinstance(data, dict):  # Single User Registration
            user = User.objects.create_user(
                email=data['email'],
                username=data['username'],
                mobile_number=data['mobile_number'],
                password=data['password'],
                latitude=data.get('latitude', None),
                longitude=data.get('longitude', None),
                address=data.get('address', "")
            )
            return Response({"email": user.email, "message": "User registered successfully"}, status=status.HTTP_201_CREATED)

        return Response({"error": "Invalid data format"}, status=status.HTTP_400_BAD_REQUEST)

# # Employee Registration
# @api_view(['POST', 'GET'])
# @permission_classes([AllowAny])
# def register_employee(request):
#     if request.method == 'POST':
#         data = request.data
#         data['is_employee'] = True
#         data['password'] = make_password(data['password'])
#         serializer = UserSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'message': 'Employee registered successfully'}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'GET':
#         employees = User.objects.filter(is_employee=True)
#         serializer = UserSerializer(employees, many=True)
#         return Response(serializer.data)


@api_view(['GET', 'POST'])
def register_employee(request):
    if request.method == 'GET':
        employees = User.objects.filter(is_employee=True).values('id', 'email', 'username', 'mobile_number', 'latitude', 'longitude', 'address')
        return Response(employees, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        data = request.data  # Accepts both single and bulk requests

        if isinstance(data, list):  # Bulk Registration
            employees = []
            for emp_data in data:
                employee = User.objects.create_user(
                    email=emp_data['email'],
                    username=emp_data['username'],
                    mobile_number=emp_data['mobile_number'],
                    password=emp_data['password'],
                    is_employee=True,
                    latitude=emp_data.get('latitude', None),
                    longitude=emp_data.get('longitude', None),
                    address=emp_data.get('address', "")
                )
                employees.append({"email": employee.email, "message": "Employee registered successfully"})
            return Response(employees, status=status.HTTP_201_CREATED)

        elif isinstance(data, dict):  # Single Employee Registration
            employee = User.objects.create_user(
                email=data['email'],
                username=data['username'],
                mobile_number=data['mobile_number'],
                password=data['password'],
                is_employee=True,
                latitude=data.get('latitude', None),
                longitude=data.get('longitude', None),
                address=data.get('address', "")
            )
            return Response({"email": employee.email, "message": "Employee registered successfully"}, status=status.HTTP_201_CREATED)

        return Response({"error": "Invalid data format"}, status=status.HTTP_400_BAD_REQUEST)


# Category CRUD
# @api_view(['POST', 'GET'])
# def category_list_create(request):
#      if request.method == 'POST':
#          serializer = CategorySerializer(data=request.data)
#          if serializer.is_valid():
#              serializer.save()
#              return Response(serializer.data, status=status.HTTP_201_CREATED)
#          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#      elif request.method == 'GET':
#          categories = Category.objects.all()
#          serializer = CategorySerializer(categories, many=True)
#          return Response(serializer.data)


# @api_view(['POST', 'GET'])
# def category_list_create(request):
#     if request.method == 'POST':
#         # Check if request.data is a list (multiple categories) or a dictionary (single category)
#         is_many = isinstance(request.data, list)
        
#         serializer = CategorySerializer(data=request.data, many=is_many)
        
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
        
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     elif request.method == 'GET':
#         categories = Category.objects.all()
#         serializer = CategorySerializer(categories, many=True)
#         return Response(serializer.data)


# @api_view(['POST', 'GET'])
# @permission_classes([IsAuthenticated])  # Requires authentication
# def category_list_create(request):
#     if request.method == 'POST':
#         # Only allow employees (shopkeepers) to add categories
#         if not request.user.is_employee:
#             return Response(
#                 {"error": "Only shopkeepers (employees) can add categories."},
#                 status=status.HTTP_403_FORBIDDEN
#             )

#         # Check if request.data is a list (multiple categories) or a dictionary (single category)
#         is_many = isinstance(request.data, list)
#         serializer = CategorySerializer(data=request.data, many=is_many)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'GET':
#         categories = Category.objects.all()
#         serializer = CategorySerializer(categories, many=True)
#         return Response(serializer.data)

@api_view(['POST', 'GET'])
def category_list_create(request):
    if request.method == 'POST':
        # Require authentication for POST requests
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

        # Only employees (shopkeepers) can add categories
        if not request.user.is_employee:
            return Response(
                {"error": "Only shopkeepers (employees) can add categories."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Check if request.data is a list (multiple categories) or a dictionary (single category)
        is_many = isinstance(request.data, list)
        serializer = CategorySerializer(data=request.data, many=is_many)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        # Allow anyone to fetch categories
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
# # Profile CRUD
# @api_view(['POST', 'GET'])
# # @permission_classes([IsAuthenticated])
# @permission_classes([AllowAny])
# def profile_list_create(request):
#     if request.method == 'POST':
#         serializer = ProfileSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'message': 'Profile created successfully'}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'GET':
#         profiles = Profile.objects.all()
#         serializer = ProfileSerializer(profiles, many=True)
#         return Response(serializer.data)

# # Product CRUD
# @api_view(['POST', 'GET'])
# # @permission_classes([IsAuthenticated])
# @permission_classes([AllowAny])
# def product_list_create(request):
#     if request.method == 'POST':
#         serializer = ProductSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'message': 'Product added successfully'}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'GET':
#         products = Product.objects.all()
#         serializer = ProductSerializer(products, many=True)
#         return Response(serializer.data)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import Profile, Product, ProductVariation
# from .serializers import ProfileSerializer, ProductSerializer, ProductVariationSerializer

# -------------------- Profile Views --------------------

@api_view(['POST', 'GET'])
# @permission_classes([IsAuthenticated])  # Authentication required for POST
def profile_list_create(request):
    if request.method == 'POST':
        # Only shopkeepers (employees) can create profiles
        if not request.user.is_employee:
            return Response(
                {"error": "Only shopkeepers can create a profile."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # serializer = ProfileSerializer(data=request.data)
          # Check if request contains multiple profiles (list) or a single profile (dict)
        is_many = isinstance(request.data, list)

        serializer = ProfileSerializer(data=request.data, many=is_many)
        if serializer.is_valid():
            serializer.save(employee=request.user)  # Assign logged-in user as employee
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)


# -------------------- Product Views --------------------

@api_view(['POST', 'GET'])
# @permission_classes([IsAuthenticated])  # Authentication required for POST
def product_list_create(request):
    if request.method == 'POST':
        # Only shopkeepers can add products
        if not request.user.is_employee:
            return Response(
                {"error": "Only shopkeepers can add products."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


# -------------------- Product Variation Views --------------------

@api_view(['POST', 'GET'])
# @permission_classes([IsAuthenticated])  # Authentication required for POST
def product_variation_list_create(request):
    if request.method == 'POST':
        # Only shopkeepers can add product variations
        if not request.user.is_employee:
            return Response(
                {"error": "Only shopkeepers can add product variations."},
                status=status.HTTP_403_FORBIDDEN
            )


        serializer = ProductVariationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        variations = ProductVariation.objects.all()
        serializer = ProductVariationSerializer(variations, many=True)
        return Response(serializer.data)


from .tasks import assign_order  # Import the Celery task

@api_view(['POST', 'GET'])
@permission_classes([AllowAny])
def order_list_create(request):
    if request.method == 'POST':
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            
            # ✅ Trigger Celery task to auto-forward the order if not accepted in 1 min
            assign_order.apply_async(args=[order.id], countdown=60)  
            
            return Response({'message': 'Order placed successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'GET':
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


from django.db.models import F
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from geopy.distance import geodesic
from .models import Product, Order, Profile
from .serializers import ProductSerializer, OrderSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

# ✅ Nearest Product Search API
@api_view(['GET'])
def search_nearest_products(request):
    try:
        user_lat = float(request.query_params.get('latitude'))
        user_long = float(request.query_params.get('longitude'))
        product_name = request.query_params.get('product')

        if not product_name:
            return Response({'error': 'Product name is required'}, status=400)

        products = Product.objects.filter(name__icontains=product_name)
        product_list = []
        for product in products:
            shop = product.profile
            shop_location = (shop.latitude, shop.longitude)
            user_location = (user_lat, user_long)
            distance = geodesic(user_location, shop_location).km
            delivery_time = int(distance * 2)  # Assuming 5 mins/km

            product_list.append({
                'product': ProductSerializer(product).data,
                # 'distance_km': round(distance, 2),
                'delivery_time_min': delivery_time
            })

        product_list.sort(key=lambda x: x['delivery_time_min'])  # Sort by delivery time
        return Response(product_list[:5])  # Return 5 nearest shops
    except Exception as e:
        return Response({'error': str(e)}, status=400)

# ✅ Order Tracking (WebSockets)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def track_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
        return Response({'order_id': order.id, 'status': order.status, 'delivery_time': order.delivery_time})
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=404)

# ✅ Real-Time Order Updates
# def send_order_update(order_id, status):
#     channel_layer = get_channel_layer()
#     async_to_sync(channel_layer.group_send)(
#         f"order_{order_id}",
#         {
#             "type": "order_update",
#             "message": json.dumps({"order_id": order_id, "status": status}),
#         },
#     )
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

def send_order_update(order_id, status):
    channel_layer = get_channel_layer()

    if channel_layer is None:
        print("Error: channel_layer is None. Check ASGI settings.")
        return  # Prevent crash

    async_to_sync(channel_layer.group_send)(
        f"order_{order_id}",
        {
            "type": "order_update",
            "message": json.dumps({"order_id": order_id, "status": status}),
        },
    )

# # Takes user's latitude, longitude, and product name as query params.
# # Filters products by name (icontains for partial match).
# # Finds the nearest shop using geopy.distance.geodesic().
# # Calculates estimated delivery time (5 mins per km assumption).
# # Returns the 5 closest results, sorted by delivery time
# GET http://127.0.0.1:8000/search/?latitude=12.9716&longitude=77.5946&product=soap
# [
#     {
#         "product": { "name": "Soap", "price": 30, "offer_price": 25 },
#         "distance_km": 1.2,
#         "delivery_time_min": 6
#     },
#     {
#         "product": { "name": "Soap", "price": 28, "offer_price": 22 },
#         "distance_km": 2.5,
#         "delivery_time_min": 12
#     }
# ]

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class OrderTrackingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.order_id = self.scope["url_route"]["kwargs"]["order_id"]
        self.room_group_name = f"order_{self.order_id}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def order_update(self, event):
        await self.send(text_data=event["message"])



from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')

    # user = authenticate(username=email, password=password)
    user = authenticate(request, email=email, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'email': user.email,
                'is_employee': user.is_employee
            }
        }, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
