from django.contrib.auth import get_user_model, authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from ecomapp.models import *
from ecomapp.serializers import *


# User = get_user_model()

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])  # Allow public access
def register_user(request):
    if request.method == 'GET':
        role = request.query_params.get('role', 'customer')
        users = Customer.objects.filter(role=role).values(
            'id', 'email', 'username', 'mobile_number', 'latitude', 'longitude', 'user_address'
        )
        return Response(users, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        data = request.data
        if not isinstance(data, dict):
            return Response({"error": "Invalid data format, expected a dictionary"}, status=status.HTTP_400_BAD_REQUEST)

        mobile_number = data.get('mobile_number')
        password = data.get('password')
        role = data.get('role', 'customer')

        if not mobile_number or not password:
            return Response({"error": "Phone number and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if phone number already exists
        if Customer.objects.filter(mobile_number=mobile_number).exists():
            return Response({"message": "Phone number already registered. Please log in."}, status=status.HTTP_409_CONFLICT)

        # Auto-generate username and email if not provided
        generated_username = f"user_{mobile_number}"
        generated_email = f"{mobile_number}@example.com"

        user = Customer(
            username=generated_username,
            email=generated_email,
            mobile_number=mobile_number,
            role=role,
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            user_address=data.get('user_address', "")
        )
        user.set_password(password)
        user.save()

        return Response({
            "message": f"{role.capitalize()} registered successfully",
            "mobile_number": user.mobile_number,
            "user_id": user.id
        }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    mobile_number = request.data.get('mobile_number')
    password = request.data.get('password')

    if not mobile_number or not password:
        return Response({'error': 'Mobile number and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = Customer.objects.get(mobile_number=mobile_number)
    except Customer.DoesNotExist:
        return Response({'error': 'Invalid mobile number or password'}, status=status.HTTP_401_UNAUTHORIZED)

    if not user.check_password(password):
        return Response({'error': 'Invalid mobile number or password'}, status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(user)
    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': {
            'id': user.id,
            'username': user.username,
            'mobile_number': user.mobile_number,
            'role': user.role
        }
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    # Simply respond with success, as we don't need to store tokens
    return Response({"message": "Logout successful"}, status=200)

from rest_framework_simplejwt.views import TokenRefreshView

@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    refresh = request.data.get("refresh")
    
    if not refresh:
        return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        token = RefreshToken(refresh)
        return Response({
            "access": str(token.access_token),
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": "Invalid or expired refresh token"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def manage_banners(request):
    if request.method == 'GET':
        shopkeeper_id = request.query_params.get('shopkeeper_id')
        if shopkeeper_id:
            banners = Banner.objects.filter(shopkeeper_id=shopkeeper_id, is_active=True)
        else:
            banners = Banner.objects.filter(is_active=True)
        
        banner_data = [
            {
                'id': banner.id,
                'shopkeeper': banner.shopkeeper.username,
                'title': banner.title,
                'image': banner.image.url if banner.image else None,
                'description': banner.description,
                'prize_offer': banner.prize_offer,
                'start_date': banner.start_date,
                'end_date': banner.end_date,
                'is_active': banner.is_active,
            }
            for banner in banners
        ]
        return Response(banner_data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        if not hasattr(request.user, 'role'):
            return Response({'error': 'User authentication issue'}, status=status.HTTP_401_UNAUTHORIZED)

        # if request.user.role != 'Shopkeeper':
        if request.user.role.lower() != 'shopkeeper':

            print(f"User: {request.user}, Role: {request.user.role}")

            return Response({'error': 'Only shopkeepers can create banners'}, status=status.HTTP_403_FORBIDDEN)
        
        data = request.data
        try:
            banner = Banner.objects.create(
                shopkeeper=request.user,
                title=data['title'],
                image=data.get('image', None),
                description=data.get('description', ""),
                prize_offer=data['prize_offer'],
                start_date=data['start_date'],
                end_date=data['end_date'],
                is_active=data.get('is_active', True)
            )
            return Response({'message': 'Banner created successfully', 'id': banner.id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])  # No authentication required
def manage_categories(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        data = request.data

        # Handle both single object and list of objects
        if isinstance(data, dict):
            data = [data]

        serializer = CategorySerializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'POST'])
@permission_classes([AllowAny])  # 🔓 Anyone can access
def manage_subcategories(request):
    if request.method == 'GET':
        category_id = request.query_params.get('category_id')
        subcategories = Subcategory.objects.filter(category_id=category_id) if category_id else Subcategory.objects.all()
        serializer = SubcategorySerializer(subcategories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        data = request.data

        # If a single subcategory object is passed, wrap it in a list
        if isinstance(data, dict):
            data = [data]

        serializer = SubcategorySerializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])  # Allow anyone to GET; POST will be restricted in code
def profile_list_create(request):
    if request.method == 'GET':
        # Allow any user to view the list of profiles
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny])
def profile_create(request):
    if request.method == 'POST':
        # Ensure the email is provided in the request data
        email = request.data.get("email")
        
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Try to retrieve the Customer instance based on the provided email
            user = Customer.objects.get(email=email)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found with the provided email"}, status=status.HTTP_404_NOT_FOUND)

        # Ensure the user has a role attribute and it is 'shopkeeper'
        if not hasattr(user, 'role') or user.role != 'shopkeeper':
            return Response({"error": "Only shopkeepers can create profiles"}, status=status.HTTP_403_FORBIDDEN)

        # Create a profile for the authenticated shopkeeper
        data = request.data.copy()  # Make a copy of the incoming request data
        serializer = ProfileSerializer(data=data, context={'request': request})
        
        if serializer.is_valid():
            # Save the profile and associate the shopkeeper as the employee
            serializer.save(employee=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET', 'POST'])
# @permission_classes([AllowAny])  # Allow anyone to GET; POST will be restricted in code
# def profile_list_create(request):
#     if request.method == 'GET':
#         profiles = Profile.objects.all()
#         serializer = ProfileSerializer(profiles, many=True)
#         return Response(serializer.data)

#     if not request.user.is_authenticated:
#         return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

#     if not hasattr(request.user, 'role') or request.user.role != 'shopkeeper':
#         return Response({"error": "Only shopkeepers can create profiles"}, status=status.HTTP_403_FORBIDDEN)

#     data = request.data.copy()

#     # Don't manually set employee ID, use request.user directly
#     serializer = ProfileSerializer(data=data, context={'request': request})
#     if serializer.is_valid():
#         serializer.save(employee=request.user)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])  # ✅ Only authenticated users can modify/delete
def profile_detail(request, pk):
    try:
        profile = Profile.objects.get(pk=pk)
    except Profile.DoesNotExist:
        return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

    # ✅ Only shopkeepers can modify/delete
    if not hasattr(request.user, 'role') or request.user.role.lower() != "shopkeeper":
        return Response({"error": "Only shopkeepers can modify profiles"}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'PUT':
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        profile.delete()
        return Response({"message": "Profile deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Allow only logged-in users
def upload_product_images(request, product_id):
    """Allows uploading multiple images for a product."""
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

    images = request.FILES.getlist('images')  # Form-data: images[]=file1&images[]=file2...

    if not images:
        return Response({"error": "No images uploaded"}, status=status.HTTP_400_BAD_REQUEST)

    image_instances = []
    for image in images:
        image_instance = ProductImage.objects.create(product=product, image=image)
        image_instances.append(image_instance)

    serializer = ProductImageSerializer(image_instances, many=True)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_product_images(request, product_id):
    """Fetch all images for a given product."""
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

    images = ProductImage.objects.filter(product=product)
    serializer = ProductImageSerializer(images, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])  # Only shopkeepers can delete images
def delete_product_image(request, image_id):
    """Delete a specific product image by ID."""
    try:
        image = ProductImage.objects.get(id=image_id)
    except ProductImage.DoesNotExist:
        return Response({"error": "Image not found"}, status=status.HTTP_404_NOT_FOUND)

    # Ensure only the product owner can delete the image
    if image.product.shop.email != request.user.email:
        return Response({"error": "You can only delete images for your own products"},
                        status=status.HTTP_403_FORBIDDEN)

    image.delete()
    return Response({"message": "Image deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])  # ✅ Allows anyone (even anonymous users)
def product_list_create(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # ✅ No user or profile linking required
            serializer.save()  # ✅ No user or profile linking required
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    


# ✅ Retrieve, Update, Delete a product (Only Shopkeepers can modify, GET is public)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])  # Allow everyone, but restrict in logic for PUT/DELETE
def product_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

    # ✅ Public GET
    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # ❌ Authenticated shopkeeper check for PUT and DELETE
    if not request.user.is_authenticated or getattr(request.user, 'role', None) != "shopkeeper":
        return Response({"error": "Only shopkeepers can modify products"}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        product.delete()
        return Response({"message": "Product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def product_variation_list_create(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        variations = ProductVariation.objects.filter(product=product)
        serializer = ProductVariationSerializer(variations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        # 🔥 Pass `product` in the context
        serializer = ProductVariationSerializer(data=request.data, context={'product': product})
        if serializer.is_valid():
            serializer.save()  # product is assigned in serializer.create()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from django.shortcuts import render
from django.http import JsonResponse
from geopy.distance import geodesic  # To calculate distance between two locations
from .models import Product, ProductVariation

def search_product(request):
    query = request.GET.get('query', '')
    lat = float(request.GET.get('lat', 0))
    lon = float(request.GET.get('lon', 0))

    # Fetch product variations matching the query
    product_variations = ProductVariation.objects.filter(
        product__name__icontains=query
    )

    results = []
    for variation in product_variations:
        product = variation.product
        shop = product.shop  # Access the Profile (shop) through the ForeignKey

        if not shop:
            continue  # Skip this product if there is no associated shop

        # Calculate the distance from the user to the shop's location
        shop_location = (shop.latitude, shop.longitude)
        user_location = (lat, lon)
        distance_km = geodesic(user_location, shop_location).kilometers
        delivery_time = round(distance_km * 10)  # Example delivery time logic: 10 minutes per km

        results.append({
            "product_name": variation.product.name,
            "variation_name": variation.value,  # Assuming value contains the variation (like '500g')
            "price": variation.price,
            "offer_price": variation.offer_price,
            "shop_name": shop.shop_name,  # Shop name from Profile model
            # # "shop_location": {
            #     "latitude": shop.latitude,
            #     "longitude": shop.longitude
            # },
            "distance_km": round(distance_km, 2),
            "delivery_time": f"{delivery_time} min"
        })

    return JsonResponse(results, safe=False)




@api_view(['GET'])
def get_cart(request):
    cart = request.session.get('cart', {})

    cart_items = []
    for variation_id, quantity in cart.items():
        try:
            variation = ProductVariation.objects.get(id=variation_id)
            item_data = ProductVariationSerializer(variation).data
            item_data['quantity'] = quantity
            cart_items.append(item_data)
        except ProductVariation.DoesNotExist:
            continue  # Skip invalid items

    return Response({"cart": cart_items}, status=status.HTTP_200_OK)

@api_view(['POST'])
def add_to_cart(request):
    cart = request.session.get('cart', {})

    product_variation_id = str(request.data.get("product_variation"))
    quantity = int(request.data.get("quantity", 1))

    try:
        product_variation = ProductVariation.objects.get(id=product_variation_id)
    except ProductVariation.DoesNotExist:
        return Response({"error": "Invalid product variation"}, status=status.HTTP_400_BAD_REQUEST)

    if product_variation_id in cart:
        cart[product_variation_id] += quantity
    else:
        cart[product_variation_id] = quantity

    request.session['cart'] = cart  # Save cart back to session

    return Response({"message": "Item added to cart successfully"}, status=status.HTTP_201_CREATED)



# ✅ Remove Item from Cart
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_cart(request, item_id):
    try:
        cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
        cart_item.delete()
        return Response({"message": "Item removed from cart"}, status=status.HTTP_200_OK)
    except CartItem.DoesNotExist:
        return Response({"error": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND)

# ✅ Clear Cart
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def clear_cart(request):
    cart = Cart.objects.filter(user=request.user).first()
    if cart:
        cart.items.all().delete()
        return Response({"message": "Cart cleared"}, status=status.HTTP_200_OK)
    return Response({"error": "No cart found"}, status=status.HTTP_404_NOT_FOUND)


import threading
import time

# 📌 ORDER FROM CART
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def order_from_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user).first()

    if not cart or not cart.items.exists():
        return Response({"error": "Your cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

    total_price = 0
    order = Order.objects.create(user=user, total_price=0, status='pending')

    for cart_item in cart.items.all():
        price = cart_item.product_variation.price * cart_item.quantity
        OrderItem.objects.create(
            order=order,
            product_variation=cart_item.product_variation,
            quantity=cart_item.quantity,
            price=price
        )
        total_price += price

    order.total_price = total_price
    order.save()

    # Clear the cart after ordering
    cart.items.all().delete()

    # Start auto-forwarding check
    thread = threading.Thread(target=auto_forward_order, args=(order.id,))
    thread.start()

    return Response({"message": "Order placed from cart successfully", "order_id": order.id}, status=status.HTTP_201_CREATED)


from django.db import transaction
# @api_view(['POST'])
# # @permission_classes([IsAuthenticated])
# def place_order_direct(request):
#     user = request.user

#     order_items = request.data.get('items', [])
#     address = request.data.get('address')         # 🔥 extra
#     pincode = request.data.get('pincode')         # 🔥 extra
#     latitude = request.data.get('latitude')       # 🔥 extra
#     longitude = request.data.get('longitude')     # 🔥 extra

#     if not order_items:
#         return Response({"error": "No items provided"}, status=status.HTTP_400_BAD_REQUEST)

#     # 💡 You can print, log or process these here
#     print("Received Address:", address)
#     print("Pincode:", pincode)
#     print("Lat/Long:", latitude, longitude)

#     total_price = 0
#     order = Order.objects.create(user=user, total_price=0, status='pending')  # no model change

#     for item in order_items:
#         try:
#             product_variation = ProductVariation.objects.get(id=item['product_variation'])
#             quantity = int(item['quantity'])
#             price = product_variation.price * quantity

#             OrderItem.objects.create(
#                 order=order,
#                 product_variation=product_variation,
#                 quantity=quantity,
#                 price=price
#             )
#             total_price += price
#         except ProductVariation.DoesNotExist:
#             return Response(
#                 {"error": f"Invalid product variation ID: {item['product_variation']}"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#     order.total_price = total_price
#     order.save()

#     return Response({
#         "message": "Order placed successfully (address received but not saved)",
#         "order_id": order.id,
#         "total_price": str(order.total_price),
#         "address": address,
#         "pincode": pincode,
#         "latitude": latitude,
#         "longitude": longitude
#     }, status=status.HTTP_201_CREATED)
@api_view(['POST'])
def place_order_direct(request):
    user_id = request.data.get('user_id')
    order_items = request.data.get('items', [])
    address = request.data.get('address')
    pincode = request.data.get('pincode')
    latitude = request.data.get('latitude')
    longitude = request.data.get('longitude')

    if not user_id:
        return Response({"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = Customer.objects.get(id=user_id)
    except Customer.DoesNotExist:
        return Response({"error": "Invalid user_id"}, status=status.HTTP_400_BAD_REQUEST)

    if not order_items:
        return Response({"error": "No items provided"}, status=status.HTTP_400_BAD_REQUEST)

    print("Received Address:", address)
    print("Pincode:", pincode)
    print("Lat/Long:", latitude, longitude)

    total_price = 0

    with transaction.atomic():
        order = Order.objects.create(user=user, total_price=0, status='pending')

        for item in order_items:
            try:
                product_variation = ProductVariation.objects.get(id=item['product_variation'])
                quantity = int(item['quantity'])
                price = product_variation.price * quantity

                OrderItem.objects.create(
                    order=order,
                    product_variation=product_variation,
                    quantity=quantity,
                    price=price
                )
                total_price += price
            except ProductVariation.DoesNotExist:
                transaction.set_rollback(True)
                return Response(
                    {"error": f"Invalid product variation ID: {item['product_variation']}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        order.total_price = total_price
        order.save()

    return Response({
        "message": "Order placed successfully (address received but not saved)",
        "order_id": order.id,
        "total_price": str(order.total_price),
        "address": address,
        "pincode": pincode,
        "latitude": latitude,
        "longitude": longitude
    }, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_order_details(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)


    # Start auto-forwarding check
    thread = threading.Thread(target=auto_forward_order, args=(order.id,))
    thread.start()

    return Response({"message": "Order placed successfully", "order_id": order.id}, status=status.HTTP_201_CREATED)


# 📌 AUTO-FORWARD ORDER IF NOT ACCEPTED IN 1 MINUTE
def auto_forward_order(order_id):
    time.sleep(60)  # Wait for 1 minute

    try:
        order = Order.objects.get(id=order_id)
        if order.status == "pending":
            # Find the next nearest shop (implement logic here)
            order.status = "forwarded"
            order.save()
            print(f"Order {order_id} was not accepted in time and has been forwarded to the next shop.")
    except Order.DoesNotExist:
        print(f"Order {order_id} not found for forwarding.")


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id)

        if order.status != "pending":
            return Response({"error": "Order is already processed"}, status=status.HTTP_400_BAD_REQUEST)

        # Assuming shopkeeper is the user accepting the order
        order.status = "accepted"
        order.save()

        return Response({"message": "Order accepted successfully", "order_id": order.id}, status=status.HTTP_200_OK)

    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)


# 📌 ADD PRODUCT TO WISHLIST
@api_view(['POST'])
def add_to_wishlist(request):
    user_id = request.data.get('user_id')
    product_id = request.data.get('product_id')

    if not user_id or not product_id:
        return Response({"error": "user_id and product_id are required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = Customer.objects.get(id=user_id)
        product = Product.objects.get(id=product_id)
    except Customer.DoesNotExist:
        return Response({"error": "Invalid user ID"}, status=status.HTTP_400_BAD_REQUEST)
    except Product.DoesNotExist:
        return Response({"error": "Invalid product ID"}, status=status.HTTP_400_BAD_REQUEST)

    Wishlist.objects.get_or_create(user=user, product=product)
    return Response({"message": "Product added to wishlist"}, status=status.HTTP_201_CREATED)


# # 📌 GET USER WISHLIST
# @api_view(['GET'])
# def get_wishlist(request):
#     wishlist = request.session.get('wishlist', [])
#     products = Product.objects.filter(id__in=wishlist)
#     serializer = ProductSerializer(products, many=True)
#     return Response(serializer.data)

@api_view(['GET'])
def get_wishlist(request):
    user_id = request.query_params.get('user_id')

    if not user_id:
        return Response({"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user_id = int(user_id.strip('/'))  # ✅ Strip trailing slash and convert to int
        user = Customer.objects.get(id=user_id)
    except (ValueError, Customer.DoesNotExist):
        return Response({"error": "Invalid user ID"}, status=status.HTTP_400_BAD_REQUEST)

    wishlist_items = Wishlist.objects.filter(user=user)
    products = [item.product for item in wishlist_items]
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)




# 📌 REMOVE PRODUCT FROM WISHLIST
@api_view(['DELETE'])
def remove_from_wishlist(request, product_id):
    wishlist = request.session.get('wishlist', [])

    if str(product_id) in wishlist:
        wishlist.remove(str(product_id))
        request.session['wishlist'] = wishlist
        return Response({"message": "Product removed from wishlist"}, status=status.HTTP_200_OK)

    return Response({"error": "Product not in wishlist"}, status=status.HTTP_400_BAD_REQUEST)


# 📌 ADD REVIEW
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_review(request):
    user = request.user
    product_id = request.data.get('product_id')
    rating = request.data.get('rating')
    comment = request.data.get('comment', '')

    try:
        product = Product.objects.get(id=product_id)
        review, created = Review.objects.update_or_create(
            user=user, product=product,
            defaults={"rating": rating, "comment": comment}
        )
        return Response({"message": "Review added successfully"}, status=status.HTTP_201_CREATED)
    except Product.DoesNotExist:
        return Response({"error": "Invalid product ID"}, status=status.HTTP_400_BAD_REQUEST)


# 📌 GET ALL REVIEWS FOR A PRODUCT
@api_view(['GET'])
def get_product_reviews(request, product_id):
    reviews = Review.objects.filter(product_id=product_id)
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)


# 📌 UPDATE REVIEW
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_review(request, review_id):
    try:
        review = Review.objects.get(id=review_id, user=request.user)
        review.rating = request.data.get('rating', review.rating)
        review.comment = request.data.get('comment', review.comment)
        review.save()
        return Response({"message": "Review updated successfully"}, status=status.HTTP_200_OK)
    except Review.DoesNotExist:
        return Response({"error": "Review not found"}, status=status.HTTP_404_NOT_FOUND)


# 📌 DELETE REVIEW
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_review(request, review_id):
    try:
        review = Review.objects.get(id=review_id, user=request.user)
        review.delete()
        return Response({"message": "Review deleted successfully"}, status=status.HTTP_200_OK)
    except Review.DoesNotExist:
        return Response({"error": "Review not found"}, status=status.HTTP_404_NOT_FOUND)


# 📌 ADD ADDRESS
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def add_address(request):
#     serializer = AddressSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save(user=request.user)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# # 📌 GET USER ADDRESSES
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_addresses(request):
#     addresses = Address.objects.filter(user=request.user)
#     serializer = AddressSerializer(addresses, many=True)
#     return Response(serializer.data)


# # 📌 UPDATE ADDRESS
# @api_view(['PUT'])
# @permission_classes([IsAuthenticated])
# def update_address(request, address_id):
#     try:
#         address = Address.objects.get(id=address_id, user=request.user)
#         serializer = AddressSerializer(address, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     except Address.DoesNotExist:
#         return Response({"error": "Address not found"}, status=status.HTTP_404_NOT_FOUND)


# # 📌 DELETE ADDRESS
# @api_view(['DELETE'])
# @permission_classes([IsAuthenticated])
# def delete_address(request, address_id):
#     try:
#         address = Address.objects.get(id=address_id, user=request.user)
#         address.delete()
#         return Response({"message": "Address deleted successfully"}, status=status.HTTP_200_OK)
#     except Address.DoesNotExist:
#         return Response({"error": "Address not found"}, status=status.HTTP_404_NOT_FOUND)
# 📌 ADD ADDRESS (no auth)
@api_view(['POST'])
@permission_classes([AllowAny])
def add_address(request):
    user_id = request.data.get('user_id')
    try:
        user = Customer.objects.get(id=user_id)
    except Customer.DoesNotExist:
        return Response({"error": "Invalid user_id"}, status=status.HTTP_400_BAD_REQUEST)

    serializer = AddressSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=user)  # ✅ set user manually here
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





# 📌 GET USER ADDRESSES (no auth)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_addresses(request, user_id):
    try:
        user = Customer.objects.get(id=user_id)
    except Customer.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    addresses = Address.objects.filter(user=user)
    serializer = AddressSerializer(addresses, many=True)
    return Response(serializer.data)



# 📌 UPDATE ADDRESS (no auth)
@api_view(['PUT'])
@permission_classes([AllowAny])
def update_address(request, address_id):
    user_id = request.data.get('user_id')
    try:
        user = Customer.objects.get(id=user_id)
        address = Address.objects.get(id=address_id, user=user)
    except (Customer.DoesNotExist, Address.DoesNotExist):
        return Response({"error": "Address not found or invalid user"}, status=status.HTTP_404_NOT_FOUND)

    serializer = AddressSerializer(address, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# 📌 DELETE ADDRESS (no auth)
@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_address(request, address_id):
    user_id = request.data.get('user_id')
    try:
        user = Customer.objects.get(id=user_id)
        address = Address.objects.get(id=address_id, user=user)
        address.delete()
        return Response({"message": "Address deleted successfully"}, status=status.HTTP_200_OK)
    except (Customer.DoesNotExist, Address.DoesNotExist):
        return Response({"error": "Address not found or invalid user"}, status=status.HTTP_404_NOT_FOUND)


# 📌 CREATE PAYMENT
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_payment(request):
    serializer = PaymentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 📌 GET USER PAYMENTS
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_payments(request):
    payments = Payment.objects.filter(user=request.user)
    serializer = PaymentSerializer(payments, many=True)
    return Response(serializer.data)


# 📌 UPDATE PAYMENT STATUS
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_payment(request, payment_id):
    try:
        payment = Payment.objects.get(id=payment_id, user=request.user)
        payment.status = request.data.get('status', payment.status)
        payment.save()
        return Response({"message": "Payment updated successfully"}, status=status.HTTP_200_OK)
    except Payment.DoesNotExist:
        return Response({"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)


# 📌 DELETE PAYMENT
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_payment(request, payment_id):
    try:
        payment = Payment.objects.get(id=payment_id, user=request.user)
        payment.delete()
        return Response({"message": "Payment deleted successfully"}, status=status.HTTP_200_OK)
    except Payment.DoesNotExist:
        return Response({"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)
   

# 📌 ADD DELIVERY PARTNER
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_delivery_partner(request):
    serializer = DeliveryPartnerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 📌 GET ALL AVAILABLE DELIVERY PARTNERS
@api_view(['GET'])
def get_delivery_partners(request):
    partners = DeliveryPartner.objects.filter(is_available=True)
    serializer = DeliveryPartnerSerializer(partners, many=True)
    return Response(serializer.data)


# 📌 UPDATE DELIVERY PARTNER AVAILABILITY
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_delivery_partner(request, partner_id):
    try:
        partner = DeliveryPartner.objects.get(id=partner_id, user=request.user)
        partner.is_available = request.data.get('is_available', partner.is_available)
        partner.save()
        return Response({"message": "Delivery partner updated successfully"}, status=status.HTTP_200_OK)
    except DeliveryPartner.DoesNotExist:
        return Response({"error": "Delivery partner not found"}, status=status.HTTP_404_NOT_FOUND)


# 📌 DELETE DELIVERY PARTNER
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_delivery_partner(request, partner_id):
    try:
        partner = DeliveryPartner.objects.get(id=partner_id, user=request.user)
        partner.delete()
        return Response({"message": "Delivery partner deleted successfully"}, status=status.HTTP_200_OK)
    except DeliveryPartner.DoesNotExist:
        return Response({"error": "Delivery partner not found"}, status=status.HTTP_404_NOT_FOUND)


# 📌 ADD ORDER TRACKING STATUS
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_order_tracking(request):
    serializer = OrderTrackingSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 📌 GET ORDER TRACKING STATUS
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order_tracking(request, order_id):
    tracking = OrderTracking.objects.filter(order_id=order_id)
    serializer = OrderTrackingSerializer(tracking, many=True)
    return Response(serializer.data)


# 📌 UPDATE ORDER STATUS
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_order_tracking(request, tracking_id):
    try:
        tracking = OrderTracking.objects.get(id=tracking_id)
        tracking.status = request.data.get('status', tracking.status)
        tracking.save()
        return Response({"message": "Order status updated successfully"}, status=status.HTTP_200_OK)
    except OrderTracking.DoesNotExist:
        return Response({"error": "Tracking record not found"}, status=status.HTTP_404_NOT_FOUND)


# 📌 DELETE ORDER TRACKING ENTRY
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_order_tracking(request, tracking_id):
    try:
        tracking = OrderTracking.objects.get(id=tracking_id)
        tracking.delete()
        return Response({"message": "Order tracking entry deleted successfully"}, status=status.HTTP_200_OK)
    except OrderTracking.DoesNotExist:
        return Response({"error": "Tracking entry not found"}, status=status.HTTP_404_NOT_FOUND)


# 📌 CREATE NOTIFICATION
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_notification(request):
    serializer = NotificationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 📌 GET USER NOTIFICATIONS
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_notifications(request):
    notifications = Notification.objects.filter(user=request.user)
    serializer = NotificationSerializer(notifications, many=True)
    return Response(serializer.data)


# 📌 MARK NOTIFICATION AS READ
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def mark_notification_read(request, notification_id):
    try:
        notification = Notification.objects.get(id=notification_id, user=request.user)
        notification.is_read = True
        notification.save()
        return Response({"message": "Notification marked as read"}, status=status.HTTP_200_OK)
    except Notification.DoesNotExist:
        return Response({"error": "Notification not found"}, status=status.HTTP_404_NOT_FOUND)


# 📌 DELETE NOTIFICATION
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_notification(request, notification_id):
    try:
        notification = Notification.objects.get(id=notification_id, user=request.user)
        notification.delete()
        return Response({"message": "Notification deleted successfully"}, status=status.HTTP_200_OK)
    except Notification.DoesNotExist:
        return Response({"error": "Notification not found"}, status=status.HTTP_404_NOT_FOUND)


from django.db.models import Q
from django.http import JsonResponse
from geopy.distance import geodesic
from .models import Product, Profile
from .serializers import ProductSerializer

def search_productss(request):
    query = request.GET.get("q", "").strip().lower()  # User search input (e.g., "hamam soap")
    
    if not query:
        return JsonResponse({"error": "Search query is required"}, status=400)

    # **Step 1: Get Customer Location**
    customer_lat = float(request.GET.get("latitude", 0))
    customer_lon = float(request.GET.get("longitude", 0))

    # **Step 2: Find the Exact Product Variants**
    exact_products = Product.objects.filter(name__icontains=query)

    # **Step 3: Find Similar Products from the Same Category**
    similar_products = Product.objects.filter(
        Q(category__name__icontains=query) | Q(name__icontains=query.split()[0])
    ).exclude(name__icontains=query)  # Exclude exact product matches

    # **Step 4: Calculate Distance and Delivery Time**
    def get_profile_data(products):
        profile_data = {}
        for product in products:
            profile = product.profile  # Use Profile instead of Shop
            if profile.id not in profile_data:
                profile_data[profile.id] = {
                    "profile_name": profile.name,  # Profile Name
                    "distance_km": None,
                    "delivery_time": None,
                    "products": []
                }
            profile_data[profile.id]["products"].append(ProductSerializer(product).data)

        # Calculate Distance and Delivery Time
        for profile_id, profile_info in profile_data.items():
            profile_obj = Profile.objects.get(id=profile_id)
            distance_km = round(
                geodesic((customer_lat, customer_lon), (profile_obj.latitude, profile_obj.longitude)).km, 2
            )
            delivery_time = int(distance_km * 5)  # 10 minutes per km (adjust as needed)

            profile_info["distance_km"] = distance_km
            profile_info["delivery_time"] = f"{delivery_time} min"

        return sorted(profile_data.values(), key=lambda x: x["distance_km"])

    # **Step 5: Return Data in Proper Order**
    response_data = {}

    if exact_products.exists():
        response_data["heading"] = f"Showing {query.title()} Variants First"
        response_data["profiles"] = get_profile_data(exact_products)

    if similar_products.exists():
        response_data["suggestions_heading"] = f"Other {query.title()} Variants"
        response_data["suggestions"] = get_profile_data(similar_products)

    if not exact_products.exists() and not similar_products.exists():
        return JsonResponse({"message": f"No {query} or similar products found nearby."})

    return JsonResponse(response_data)

# GET /search/?q=colgate+toothpaste&latitude=12.9716&longitude=77.5946
