import datetime
from django.db import connection
from django.db.models.functions import TruncDate
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

from django.utils.dateparse import parse_date
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.decorators import api_view
from .serializers import *
from .models import *
import traceback
from asgiref.sync import sync_to_async
from rest_framework.decorators import APIView


class AsyncUserList(APIView):
    async def get(self, request):
        users = await sync_to_async(lambda: list(UserDetails.objects.all()))()
        serializer = await sync_to_async(lambda: UserDetailsSerializer(users, many=True).data)()
        return Response(serializer)


@api_view(['GET'])
def users(request):
    """
    API endpoint to retrieve all users.

    - `GET /users/`

    Returns a JSON object with a list of all users if the request is successful.

    Returns:
    - A JSON object with the list of all users.
    - 200 OK: If the retrieval is successful.
    """
    if request.method == 'GET':
        users = UserDetails.objects.all()
        serializer = UserDetailsSerializer(users, many=True)
        return Response(serializer.data)


@api_view(['POST'])
def create_Employee(request):
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
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            # Hash the password before saving
            serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
            serializer.validated_data['success'] = True
            user = Employee.objects.create(**serializer.validated_data)
            return Response({'message': 'User created successfully', 'user': serializer.data['username'],
                             'success': serializer.data['success']}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

    # In case a request method other than POST or GET is sent, you could return a method not allowed response.
    return Response({'message': 'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['PUT'])
def update_employee(request):
    """
    API endpoint to update an existing employee.

    Accepts the following parameters in the request query parameters:
    - employee_id: The id of the employee to update.

    Accepts the following parameters in the request body:
    - username: The username of the employee.
    - password: The password of the employee.
    - mobile: The mobile number of the employee.
    - email: The email of the employee.
    - role: The role of the employee.
    - location: The location of the employee.

    Returns a JSON object with the updated employee details if the update is successful.
    Returns a JSON object with an error message if the update fails.
    """
    employee_id = request.query_params.get('employee_id')

    if not employee_id or not employee_id.isdigit():
        return Response({'error': 'Valid user_id is required'}, status=status.HTTP_400_BAD_REQUEST)

    user = get_object_or_404(Employee, id=int(employee_id))
    serializer = EmployeeSerializer(user, data=request.data, partial=True)

    if serializer.is_valid():
        if 'password' in serializer.validated_data:
            serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_employee(request):
    try:
        employee_id = request.query_params.get('employee_id')

        if not employee_id or not employee_id.isdigit():
            return Response({'error': 'Valid user_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        employee = Employee.objects.get(id=employee_id)
        employee.delete()
        return Response({'message': 'User deleted successfully'}, status=status.HTTP_200_OK)
    except Employee.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def total_employees(request):
    """
    API endpoint to retrieve all employees.

    This function handles GET requests to retrieve a list of all employees.
    It serializes the employee data and returns it as a JSON response.

    Returns:
    - 200 OK: A JSON object containing a list of all employees with their details.
    """

    users = Employee.objects.all()
    serializer = TotalEmployeeSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_user_details(request):
    name = request.data.get('name')
    membership = request.data.get('membership', 'silver')
    password = request.data.get('password')
    subscribed = request.data.get('subscribed', False)
    premium_amount = request.data.get('premium_amount')

    if not name or not password:
        return JsonResponse({'error': 'Name and password are required'}, status=400)

    if UserDetails.objects.filter(name=name).exists():
        return JsonResponse({'error': 'Username already exists'}, status=400)

    # Convert premium_amount to integer
    try:
        premium_amount = int(premium_amount) if premium_amount else 0
    except ValueError:
        return JsonResponse({'error': 'Invalid premium_amount'}, status=400)

    # # Set membership based on subscription and premium amount
    # if subscribed and premium_amount == 20000:
    #     membership = 'gold'
    # elif subscribed and premium_amount == 50000:
    #     membership = 'platinum'

    # Get emblem URL based on membership type
    emblem_url = UserDetails.EMBLEM_URLS.get(membership, '')

    # Create user
    data = request.data.copy()
    data['membership'] = membership
    data['emblem_url'] = emblem_url
    data['points'] = 200  # Start with 0 points

    serializer = UserDetailsSerializer(data=data)
    if serializer.is_valid():
        serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
        serializer.save()
        return Response({'message': 'User created successfully', 'user': serializer.data},
                        status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth.hashers import check_password
from asgiref.sync import sync_to_async
import traceback


# Assuming you have this defined
# from .models import Employee  # Replace with your actual model import


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
            user = Employee.objects.get(email=email)
        except Employee.DoesNotExist:
            return JsonResponse({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        if check_password(password, user.password):
            # Change success to True if password is matched
            return JsonResponse({
                'Message': 'Login successfully',
                'success': True,  # Set success to True
                'user_id': user.id,
                'username': user.username,
                'role': user.role
            }, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'error': 'Invalid credentials', 'success': False}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        # Print the full traceback to debug the issue
        traceback.print_exc()
        return JsonResponse({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
import traceback
from django.contrib.auth.hashers import check_password
from django.utils.timezone import now
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from .models import Employee

@api_view(['POST'])
def customer_login(request):
    try:
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return JsonResponse({'error': 'username and password are required', 'success': False}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UserDetails.objects.get(name=username)
        except UserDetails.DoesNotExist:
            return JsonResponse({'error': 'Invalid credentials', 'success': False}, status=status.HTTP_400_BAD_REQUEST)

        if check_password(password, user.password):
            # ✅ Give 200 bonus points on login
            # user.points += 200
            user.save()

            # # ✅ Get emblem URL based on membership
            # EMBLEM_URLS = {
            #     'silver': 'https://postimg.cc/bsn3qPq7',
            #     'gold': 'https://yourwebsite.com/images/gold.png',
            #     'platinum': 'https://yourwebsite.com/images/platinum.png',
            # }
            # emblem_url = EMBLEM_URLS.get(user.membership, '')

            # # ✅ Check if Aadhar is present
            # has_aadhar = bool(user.aadhar and hasattr(user.aadhar, 'url'))

            # ✅ Emblem URLs
            EMBLEM_URLS = UserDetails.EMBLEM_URLS
            emblem_url = EMBLEM_URLS.get(user.membership, '')

            # ✅ Check if aadhar image exists
            has_aadhar = bool(user.aadhar and hasattr(user.aadhar, 'url'))


            # ✅ Return the correct response
            response_data = {
                'Message': 'Login successful',
                'success': True,
                'user_id': user.id,
                'username': user.name,
                'aadhar': has_aadhar,
                'emblem_url': emblem_url,
                'points':user.points
            }

            print(f"Response Data: {response_data}")  # Debug print
            return JsonResponse(response_data, status=status.HTTP_200_OK)

        else:
            return JsonResponse({'error': 'Invalid credentials', 'success': False}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'error': 'Internal server error', 'success': False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_saloon_orders(request):
    """
    API endpoint to retrieve all saloon orders.

    Returns a JSON response containing a list of all saloon orders
    with their details if the retrieval is successful.

    Returns:
    - 200 OK: A JSON object with the list of all saloon orders.
    """
    orders = SaloonOrder.objects.all()
    serializer = SaloonOrdersSerializer(orders, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# @csrf_exempt
@api_view(['POST'])
def post_saloon_orders(request):
    """
    API endpoint to create a new saloon order.

    Accepts the following parameters in the request body:
    - username: The username of the customer making the request.
    - order_type: The type of the order.
    - category: The category of the order.
    - services: The services selected for the order.
    - date: The date of the order.
    - time: The time of the order.

    Returns a JSON response containing a message and the created order details if the creation is successful.
    Returns a JSON object with an error message if the creation fails.

    Returns:
    - 201 Created: A JSON object with the created order details.
    - 400 Bad Request: A JSON object with an error message.
    """
    if request.method == 'POST':
        serializer = SaloonOrdersSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()  # Save the validated data
            print('saved')
            return Response({'message': 'Order success', 'order': serializer.data}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def post_gym_orders(request):
    """
    API endpoint to create a new gym order.

    Accepts the following parameters in the request body:
    - username: The username of the customer making the request.
    - order_type: The type of the order.
    - category: The category of the order.
    - services: The services selected for the order.
    - date: The date of the order.
    - time: The time of the order.

    Returns a JSON response containing a message and the created order details if the creation is successful.
    Returns a JSON object with an error message if the creation fails.

    Returns:
    - 201 Created: A JSON object with the created order details.
    - 400 Bad Request: A JSON object with an error message.
    """
    if request.method == 'POST':
        serializer = GymOrderSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()  # Save the validated data

            return Response({'message': 'Order success', 'order': serializer.data}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_gym_orders(request):
    try:
        customer_param = request.query_params.get('customer_id')
        order_param = request.query_params.get('order_id')
        # Fetch the specific hotel order record by customer_id and order_id
        gym = GymOrder.objects.get(customer_id=customer_param, id=order_param)
        print(gym)  # Debug: Print the fetched hotel order
    except GymOrder.DoesNotExist:
        return Response({'error': 'Hotel order record not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Use the existing hotel order instance for updating
    serializer = GymOrderSerializer(gym, data=request.data, partial=True)

    if serializer.is_valid():
        # Check for the status and update accordingly

        if request.data.get('payment_status') == 'paid':
            serializer.validated_data['payment_status'] = 'Completed'

        # Save the updated hotel order
        gym_order = serializer.save()

        # Retrieve the username from the associated UserDetails model
        customer_username = gym_order.customer_id.name if gym_order.customer_id else None

        # Return success response with the username
        return Response({
            'message': 'Gym Order updated successfully',
            'order': serializer.data,
            'username': customer_username
        }, status=status.HTTP_200_OK)

    # If the serializer is invalid, return errors
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_gym_orders(request):
    """
    API endpoint to retrieve all gym orders.

    Returns a JSON response containing a list of all gym orders
    with their details if the retrieval is successful.

    Returns:
    - 200 OK: A JSON object with the list of all gym orders.
    """
    orders = GymOrder.objects.all()
    serializer = GymOrderSerializer(orders, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def post_spa_orders(request):
    """
    API endpoint to create a new spa order.

    Accepts the following parameters in the request body:
    - username: The username of the customer making the request.
    - order_type: The type of the order.
    - category: The category of the order.
    - services: The services selected for the order.
    - date: The date of the order.
    - time: The time of the order.

    Returns a JSON response containing a message and the created order details if the creation is successful.
    Returns a JSON object with an error message if the creation fails.

    Returns:
    - 201 Created: A JSON object with the created order details.
    - 400 Bad Request: A JSON object with an error message.
    """
    if request.method == 'POST':
        serializer = SpaOrdersSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data['status'] == "" or "booked":
                serializer.validated_data['status'] = "Booked"
            # if serializer.validated_data['payment_type'] == "Credit Card" or "Credit Card":
            #     serializer.validated_data['payment_type'] = "paid"
            hotel_order = serializer.save()  # Save the validated data
            customer_username = hotel_order.customer_id.name if hotel_order.customer_id else None

            return Response({'message': 'Spa Booking success', 'username': customer_username, 'order': serializer.data},
                            status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_spa_orders(request):
    """
    API endpoint to retrieve all spa orders.

    Returns a JSON response containing a list of all spa orders
    with their details if the retrieval is successful.

    Returns:
    - 200 OK: A JSON object with the list of all spa orders.
    """
    orders = SpaOrder.objects.all()
    serializer = SpaOrdersSerializer(orders, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
def update_spa_orders(request):
    try:
        customer_param = request.query_params.get('customer_id')
        order_param = request.query_params.get('order_id')
        # Fetch the specific hotel order record by customer_id and order_id
        spa = SpaOrder.objects.get(customer_id=customer_param, id=order_param)
        print(spa)  # Debug: Print the fetched hotel order
    except SpaOrder.DoesNotExist:
        return Response({'error': 'Hotel order record not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Use the existing hotel order instance for updating
    serializer = SpaOrdersSerializer(spa, data=request.data, partial=True)

    if serializer.is_valid():
        # Check for the status and update accordingly

        if request.data.get('payment_status') == 'paid':
            serializer.validated_data['payment_status'] = 'Completed'

        # Save the updated hotel order
        spa_order = serializer.save()

        # Retrieve the username from the associated UserDetails model
        customer_username = spa_order.customer_id.name if spa_order.customer_id else None

        # Return success response with the username
        return Response({
            'message': 'Spa Order updated successfully',
            'order': serializer.data,
            'username': customer_username
        }, status=status.HTTP_200_OK)

    # If the serializer is invalid, return errors
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_spa_order_status(request):
    """
    API endpoint to fetch all spa orders based on their status.

    Accepts the following parameter in the request query string:
    - status: The status of the orders to fetch. Accepted values are 'Booked', 'checked_in', 'checked_out'.

    Returns a JSON object with the list of hotel orders if the fetch is successful.
    Returns a JSON object with an error message if the fetch fails.
    """
    status_param = request.query_params.get('status', None)

    try:
        print(status)
        order = SpaOrder.objects.filter(status=status_param).all()

        if not order.exists():
            return Response({'message': 'No spa orders found for the given status.'},
                            status=status.HTTP_404_NOT_FOUND)
        serializer = SpaOrdersSerializer(order, many=True)
        return Response({
            'orders': serializer.data,

        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_spa_payment_status(request):
    """
    API endpoint to update the payment status of a spa order.

    - `GET /payment-status?customer_id=<int:customer_id>&order_id=<int:order_id>&status=<str:status>`

    Parameters:
    - `customer_id`: The id of the customer (Employee) to filter orders by.
    - `order_id`: The id of the order to update the payment status for.
    - `status`: The status to update the order record with. Accepted values are 'paid' and 'unpaid'.

    Returns a JSON object with the updated order record details if the update is successful.
    Returns a JSON object with an error message if the update fails.

    Raises:
    - `404`: If the hotel order record is not found.
    """

    try:
        payment_param = request.query_params.get('payment_status')
        payment_param = payment_param.lower()
        if not payment_param:
            return Response({'error': 'Payment status parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)

        spa_orders = SpaOrder.objects.filter(payment_status=payment_param)

        if not spa_orders.exists():
            return Response({'error': 'No spa orders found with the given payment status.'},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = SpaOrdersSerializer(spa_orders, many=True)  # Corrected serialization
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
def update_hotel_orders(request):
    try:
        customer_param = request.query_params.get('customer_id')
        order_param = request.query_params.get('order_id')
        # Fetch the specific hotel order record by customer_id and order_id
        hotel = HotelOrder.objects.get(customer_id=customer_param, id=order_param)
        print(hotel)  # Debug: Print the fetched hotel order
    except HotelOrder.DoesNotExist:
        return Response({'error': 'Hotel order record not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Use the existing hotel order instance for updating
    serializer = HotelOrdersSerializer(hotel, data=request.data, partial=True)

    if serializer.is_valid():
        # Check for the status and update accordingly
        current_status = serializer.validated_data.get('status', None)

        # Check if the status is 'check_in' and the order is not already checked in
        if request.data.get('status') == 'check_in':
            # if current_status == 'checked_in':
            if hotel.check_in:
                return Response({'message': 'The booking is already checked in.'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.validated_data['status'] = 'checked_in'
            check_in_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            serializer.validated_data['check_in'] = check_in_time

        # Check if the status is 'check_out' and update accordingly
        if request.data.get('status') == 'check_out':
            if hotel.check_out:
                return Response({'message': 'The booking is already checked out.'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.validated_data['status'] = 'checked_out'
            check_out_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            serializer.validated_data['check_out'] = check_out_time

        # Release the number of rooms booked
        try:
            num_rooms = int(hotel.room_count)
        except ValueError:
            return Response({'error': 'Invalid room_count value.'}, status=status.HTTP_400_BAD_REQUEST)

        # Get any 'booked' rooms (or 'unavailable') and mark only that many as available
        booked_rooms = Rooms.objects.filter(status__iexact='booked')[:num_rooms]
        for room in booked_rooms:
            room.status = 'available'
            room.save()
            print(f"Room {room.id} marked as available")


        # Ensure check_in is not greater than check_out and not the same time
        if 'check_in' in serializer.validated_data and 'check_out' in serializer.validated_data:
            check_in_dt = datetime.strptime(serializer.validated_data['check_in'], '%Y-%m-%d %H:%M:%S')
            check_out_dt = datetime.strptime(serializer.validated_data['check_out'], '%Y-%m-%d %H:%M:%S')

            if check_in_dt >= check_out_dt:
                return Response({'message': 'Check-in time cannot be greater than or equal to check-out time.'},
                                status=status.HTTP_400_BAD_REQUEST)

        if request.data.get('payment_status') == 'paid':
            serializer.validated_data['payment_status'] = 'paid'

        # Save the updated hotel order
        hotel_order = serializer.save()

        # Retrieve the username from the associated UserDetails model
        customer_username = hotel_order.customer_id.name if hotel_order.customer_id else None

        # Return success response with the username
        return Response({
            'message': 'Hotel Booking updated successfully',
            'order': serializer.data,
            'username': customer_username
        }, status=status.HTTP_200_OK)

    # If the serializer is invalid, return errors
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def get_hotel_orders(request):
    """
    API endpoint to retrieve all hotel orders.

    Returns a JSON response containing a list of all hotel orders
    with their details if the retrieval is successful.

    Returns:
    - 200 OK: A JSON object with the list of all hotel orders.
    """

    try:
        # Fetch data asynchronously
        orders = HotelOrder.objects.all()
        # Serialize the data
        serializer = HotelOrdersSerializer(orders, many=True)
        # Return the serialized data as a response
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        # Handle any errors
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_room_count(request):
    """
    API endpoint to retrieve the count of available rooms.

    Returns a JSON response containing the count of rooms that are
    currently marked as 'Available'.

    Returns:
    - 200 OK: A JSON object with the key 'available_rooms_count' and its value.
    """
    available_rooms_count = Rooms.objects.filter(status='Available').count()
    return Response({'available_rooms_count': available_rooms_count}, status=status.HTTP_200_OK)
    available_rooms_count = Rooms.objects.filter(status='Available').count()
    return Response({'available_rooms_count': available_rooms_count}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_order_by_id_and_date(request):
    employee_id = request.query_params.get('employee_id')
    date_str = request.query_params.get('date')
    role = request.query_params.get('role')

    if not employee_id or not employee_id.isdigit():
        return Response({'error': 'Valid employee_id is required'}, status=status.HTTP_400_BAD_REQUEST)

    if not date_str:
        return Response({'error': 'Date is required in YYYY-MM-DD format'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return Response({'error': 'Invalid date format. Use YYYY-MM-DD'}, status=status.HTTP_400_BAD_REQUEST)

    if not role:
        return Response({'error': 'Role is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        emp_role = Employee.objects.get(id=employee_id, role=role)
    except Employee.DoesNotExist:
        return Response({'error': 'Invalid employee or role'}, status=status.HTTP_400_BAD_REQUEST)

    orders = None  # Initialize orders to avoid unbound error

    try:
        if emp_role.role == "hotel":
            orders = HotelOrder.objects.annotate(created_date=TruncDate('created_at')).filter(employee_id=employee_id,
                                                                                              created_date=date_obj)
        elif emp_role.role == "spa":
            orders = SpaOrder.objects.annotate(created_date=TruncDate('created_at')).filter(employee_id=employee_id,
                                                                                            created_date=date_obj)
        elif emp_role.role == "gym":
            orders = GymOrder.objects.annotate(created_date=TruncDate('created_at')).filter(employee_id=employee_id,
                                                                                            created_date=date_obj)
        elif emp_role.role == "saloon":  # Fix: changed to emp_role.role
            orders = SaloonOrder.objects.annotate(created_date=TruncDate('created_at')).filter(employee_id=employee_id,
                                                                                               created_date=date_obj)
        else:
            return Response({'error': 'Invalid role specified'}, status=status.HTTP_400_BAD_REQUEST)  # Fallback case

        if not orders or not orders.exists():  # Check for None and empty QuerySet
            return Response({'error': 'No orders found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = HotelOrdersSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_hotel_order_status(request):
    """
    API endpoint to fetch all hotel orders based on their status.

    Accepts the following parameter in the request query string:
    - status: The status of the orders to fetch. Accepted values are 'Booked', 'checked_in', 'checked_out'.

    Returns a JSON object with the list of hotel orders if the fetch is successful.
    Returns a JSON object with an error message if the fetch fails.
    """
    status_param = request.query_params.get('status', None)

    try:
        print(status)
        order = HotelOrder.objects.filter(status=status_param).all()
        if not order.exists():
            return Response({'message': 'No hotel orders found for the given status.'},
                            status=status.HTTP_404_NOT_FOUND)
        serializer = HotelOrdersSerializer(order, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


from django.utils import timezone


@api_view(['GET'])
def filter_by_status_and_user(request, user_id):
    # Get the current date (timezone-aware)
    """
    API endpoint to filter SaloonOrders by status, date, and user.

    - `GET /saloon/orders/user/<int:user_id>`

    Returns a JSON object with the list of completed orders for the given user on the current date
    if there are orders, or a message if there are no orders.

    Parameters:
    - `user_id`: The id of the user (Employee) to filter orders by.

    Returns:
    - A JSON object with a list of orders if there are completed orders for the given user on the current date.
    - A JSON object with a message if there are no completed orders for the given user on the current date.

    Raises:
    - `404`: If the user is not found.
    """

    today = timezone.now().date()

    try:
        # Get the employee (user) by user_id
        # user = Employee.objects.get(id=user_id)
        user_instance = get_object_or_404(Employee, id=user_id)
        # Filter SaloonOrders by status, date, and user
        orders = SaloonOrder.objects.filter(
            username=user_instance,
            payment_status="completed",
            date=today
        )

        # If there are orders, return them; otherwise, return a message
        if orders.exists():
            # Format the orders into a list of dictionaries
            return Response({'orders': SaloonOrdersSerializer.data}, status=200)
        else:
            return Response({'message': 'No completed orders for today for this user.'}, status=404)
    except Employee.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)


# Attendance
from datetime import datetime  # Correct import


@api_view(['POST'])
def create_attendance(request):
    """
    API endpoint to create a new attendance record or update an existing one based on the provided status.

    Accepts the following parameters in the request body:
    - employee_attendance: The id of the employee (Employee) to create an attendance record for.
    - status: The status of the attendance record to create or update. Accepted values are 'check in' and 'check out'.

    Returns a JSON object with the created or updated attendance record details if the request is successful.
    Returns a JSON object with an error message if the request fails.

    Raises:
    - 400: If the request body is invalid or if the employee has already checked in or out.
    """
    employee = request.data.get('employee_attendance')
    status = request.data.get('status')

    if not status or not employee:
        return JsonResponse({'error': 'Employee and status required'}, status=400)

    # Normalize status input
    normalized_status = status.strip().lower()
    print(employee)
    print(status)
    print(normalized_status)

    # Handle check-in
    if normalized_status == "check in":
        check_in_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Check if the employee has already checked in
        if Attendance.objects.filter(employee_attendance_id=employee, status='check in').exists():
            return JsonResponse({'error': 'Already checked in'}, status=400)

        # Create a new attendance record with check-in time
        attendance_data = {
            'employee_attendance': employee,
            'check_in': check_in_time,
            'status': 'check in'
        }

        serializer = AttendanceSerializer(data=attendance_data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Checked in successfully', 'user': serializer.data}, status=201)

        return Response(serializer.errors, status=400)

    # Handle check-out
    elif normalized_status == "check out":
        # Find the latest check-in record for the employee
        attendance_record = Attendance.objects.filter(employee_attendance_id=employee, status='check in').first()

        if not attendance_record:
            return JsonResponse({'error': 'No check-in record found'}, status=400)

        check_out_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Update the existing record with check-out time
        attendance_record.check_out = check_out_time
        attendance_record.status = 'check out'
        attendance_record.save()

        # Update the attendance status based on check-out
        if attendance_record.status == "check out" and check_out_time:
            attendance_record.status = 'Present'
        else:
            attendance_record.status = 'Absent'
        attendance_record.save()

        return Response({'message': 'Checked out successfully', 'user': AttendanceSerializer(attendance_record).data},
                        status=200)

    else:
        return JsonResponse({'error': 'Invalid status'}, status=400)


@api_view(['GET'])
def get_attendance_id(request):
    """
    API endpoint to get attendance record by employee ID.

    - `GET /attendance/id?employee_id=<int:employee_id>`

    Parameters:
    - `employee_id`: The id of the employee (Employee) to filter attendance records by.

    Returns:
    - A JSON object with the attendance record details if the record is found.
    - A JSON object with an error message if the record is not found.

    Raises:
    - `400`: If the employee ID is not provided.
    - `404`: If the attendance record is not found.
    """

    employee_id = request.query_params.get('employee_id')

    if not employee_id:
        return Response({'error': 'Employee ID is required'}, status=status.HTTP_400_BAD_REQUEST)

    # Fetch the attendance record for the given employee ID
    attendance_record = Attendance.objects.filter(employee_attendance_id=employee_id).first()

    if not attendance_record:
        return Response({'error': 'Attendance record not found'}, status=status.HTTP_404_NOT_FOUND)

    # Serialize the attendance record
    serializer = AttendanceSerializer(attendance_record)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_all_attendance(request):
    """
    API endpoint to retrieve all attendance records.

    - `GET /all-attendance/`

    Returns a JSON object with a list of all attendance records if the request is successful.

    Returns:
    - A JSON object with the list of all attendance records.
    - 200 OK: If the retrieval is successful.
    """

    attendance = Attendance.objects.all()
    serializer = AttendanceSerializer(attendance, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_present(request):
    """
    API endpoint to get a list of employees who are present on a given date or for all dates if no date is provided.

    - `GET /present?date=<date>`

    Parameters:
    - `date`: The date string in the format 'YYYY-MM-DD' to filter attendance records by.

    Returns:
    - A JSON object with a list of present employees if the request is successful.
    - A JSON object with an error message if the request fails.

    Raises:
    - `400`: If the date format is invalid.
    """

    date_str = request.query_params.get('date', None)
    if date_str:
        date = parse_date(date_str)
        if date is None:
            return Response({'error': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)
        present = Attendance.objects.filter(status='Present', date=date)  # Adjust 'date' to your date field name
    else:
        present = Attendance.objects.filter(status='Present')

    serializer = PresentSerializer(present, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_payment_status(request):
    """
    API endpoint to update the payment status of a hotel order.

    - `GET /payment-status?customer_id=<int:customer_id>&order_id=<int:order_id>&status=<str:status>`

    Parameters:
    - `customer_id`: The id of the customer (Employee) to filter orders by.
    - `order_id`: The id of the order to update the payment status for.
    - `status`: The status to update the order record with. Accepted values are 'paid' and 'unpaid'.

    Returns a JSON object with the updated order record details if the update is successful.
    Returns a JSON object with an error message if the update fails.

    Raises:
    - `404`: If the hotel order record is not found.
    """

    try:
        param = request.query_params.get('customer_id')
        # status_param = request.query_params.get('status', None).lower()
        order_param = request.query_params.get('order_id')
        hotel = HotelOrder.objects.get(customer_id=param,
                                       id=order_param)  # Fetch the specific hotel order record by primary key
    except HotelOrder.DoesNotExist:
        return Response({'error': 'Hotel order record not found.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = HotelOrder(hotel, data=request.data, partial=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def post_hotel_orders(request):
    if request.method == 'POST':
        serializer = HotelOrdersSerializer(data=request.data)

        if serializer.is_valid():
            room_count = int(serializer.validated_data['room_count'])  # Get room count from request

            # Fetch available rooms
            available_rooms = Rooms.objects.filter(status='Available')[:room_count]
            print(available_rooms)
            if len(available_rooms) < room_count:
                return Response({'error': 'Not enough available rooms'}, status=status.HTTP_400_BAD_REQUEST)

            # Book the rooms
            for room in available_rooms:
                room.status = 'Booked'
                room.save()

            # Save the hotel order with room count
            serializer.validated_data['status'] = "Booked"
            hotel_order = serializer.save()

            return Response(
                {'message': 'Hotel Booking success', 'username': hotel_order.customer_id.name,
                 'order': serializer.data},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_saloon_order_status(request):
    """
    API endpoint to fetch all saloon orders based on their status.

    Accepts the following parameter in the request query string:
    - status: The status of the orders to fetch. Accepted values are 'Booked', 'checked_in', 'checked_out'.

    Returns a JSON object with the list of hotel orders if the fetch is successful.
    Returns a JSON object with an error message if the fetch fails.
    """
    status_param = request.query_params.get('status', None)

    try:
        print(status)
        order = SaloonOrder.objects.filter(status=status_param).all()
        if not order.exists():
            return Response({'message': 'No saloon orders found for the given status.'},
                            status=status.HTTP_404_NOT_FOUND)
        serializer = SaloonOrdersSerializer(order, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_saloon_payment_status(request):
    """
    API endpoint to update the payment status of a spa order.

    - `GET /payment-status?customer_id=<int:customer_id>&order_id=<int:order_id>&status=<str:status>`

    Parameters:
    - `customer_id`: The id of the customer (Employee) to filter orders by.
    - `order_id`: The id of the order to update the payment status for.
    - `status`: The status to update the order record with. Accepted values are 'paid' and 'unpaid'.

    Returns a JSON object with the updated order record details if the update is successful.
    Returns a JSON object with an error message if the update fails.

    Raises:
    - `404`: If the hotel order record is not found.
    """

    try:
        payment_param = request.query_params.get('payment_status')
        payment_param = payment_param.lower()
        if not payment_param:
            return Response({'error': 'Payment status parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)

        saloon_orders = SaloonOrder.objects.filter(payment_status=payment_param)

        if not saloon_orders.exists():
            return Response({'error': 'No saloon orders found with the given payment status.'},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = SaloonOrdersSerializer(saloon_orders, many=True)  # Corrected serialization
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_gym_order_status(request):
    """
    API endpoint to fetch all gym orders based on their status.

    Accepts the following parameter in the request query string:
    - status: The status of the orders to fetch. Accepted values are 'Booked', 'checked_in', 'checked_out'.

    Returns a JSON object with the list of hotel orders if the fetch is successful.
    Returns a JSON object with an error message if the fetch fails.
    """
    status_param = request.query_params.get('status', None)

    try:
        print(status)
        order = GymOrder.objects.filter(status=status_param).all()
        if not order.exists():
            return Response({'message': 'No gym orders found for the given status.'},
                            status=status.HTTP_404_NOT_FOUND)
        serializer = GymOrderSerializer(order, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_gym_payment_status(request):
    """
    API endpoint to update the payment status of a spa order.

    - `GET /payment-status?customer_id=<int:customer_id>&order_id=<int:order_id>&status=<str:status>`

    Parameters:
    - `customer_id`: The id of the customer (Employee) to filter orders by.
    - `order_id`: The id of the order to update the payment status for.
    - `status`: The status to update the order record with. Accepted values are 'paid' and 'unpaid'.

    Returns a JSON object with the updated order record details if the update is successful.
    Returns a JSON object with an error message if the update fails.

    Raises:
    - `404`: If the hotel order record is not found.
    """

    try:
        payment_param = request.query_params.get('payment_status')
        payment_param = payment_param.lower()
        if not payment_param:
            return Response({'error': 'Payment status parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)

        gym_orders = GymOrder.objects.filter(payment_status=payment_param)

        if not gym_orders.exists():
            return Response({'error': 'No gym orders found with the given payment status.'},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = GymOrderSerializer(gym_orders, many=True)  # Corrected serialization
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
def update_saloon_orders(request):
    try:
        customer_param = request.query_params.get('customer_id')
        order_param = request.query_params.get('order_id')
        # Fetch the specific hotel order record by customer_id and order_id
        saloon = SaloonOrder.objects.get(customer_id=customer_param, id=order_param)
        print(saloon)  # Debug: Print the fetched hotel order
    except SaloonOrder.DoesNotExist:
        return Response({'error': 'Hotel order record not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Use the existing hotel order instance for updating
    serializer = SaloonOrdersSerializer(saloon, data=request.data, partial=True)

    if serializer.is_valid():
        # Check for the status and update accordingly

        if request.data.get('payment_status') == 'paid':
            serializer.validated_data['payment_status'] = 'Completed'

        # Save the updated hotel order
        saloon_order = serializer.save()

        # Retrieve the username from the associated UserDetails model
        customer_username = saloon_order.customer_id.name if saloon_order.customer_id else None

        # Return success response with the username
        return Response({
            'message': 'Saloon Order updated successfully',
            'order': serializer.data,
            'username': customer_username
        }, status=status.HTTP_200_OK)

    # If the serializer is invalid, return errors
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_task(request):
    if request.method == 'POST':
        task = TaskSerializer(data=request.data)
        if task.is_valid():
            assigned_to_username = request.data.get('assigned_to')  # ✅ Extract from request.data
            if not assigned_to_username:
                return Response({'error': 'assigned_to is required'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                employee_instance = Employee.objects.get(username=assigned_to_username)
                task.validated_data['employee'] = employee_instance  # ✅ Assign the employee object
            except Employee.DoesNotExist:
                return Response({'error': 'Employee not found.'}, status=status.HTTP_404_NOT_FOUND)

            task.save()
            return Response(task.data, status=status.HTTP_201_CREATED)

        return Response(task.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_all_task(request):
    try:
        task = Task.objects.all()
        serializer = TaskSerializer(task, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_task(request):
    try:
        task_id = request.query_params.get('task_id')
        # Fetch the specific hotel order record by customer_id and order_id
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response({'error': 'Task record not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Use the existing hotel order instance for updating
    serializer = TaskSerializer(task, data=request.data, partial=True)

    if serializer.is_valid():
        # Check for the status and update accordingly

        if request.data.get('status') == 'completed':
            serializer.validated_data['status'] = 'Completed'
        elif request.data.get('status') == 'verified':
            serializer.validated_data['status'] = 'Verified'

        # Save the updated hotel order
        task = serializer.save()

        # Retrieve the username from the associated UserDetails model
        employee_name = task.employee.username if task.employee else None

        # Return success response with the username
        return Response({
            'message': 'Task updated successfully',
            'order': serializer.data,
            'username': employee_name
        }, status=status.HTTP_200_OK)

    # If the serializer is invalid, return errors
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def orders_by_user_id(request):
    try:
        user_param = request.query_params.get('user_id')
        status_param = request.query_params.get('status')

        if not user_param or not status_param:
            return Response({'error': 'Both user_id and status parameters are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch data from different models
        hotel_orders = HotelOrder.objects.filter(customer_id=user_param, status=status_param)
        gym_orders = GymOrder.objects.filter(customer_id=user_param, status=status_param)
        spa_orders = SpaOrder.objects.filter(customer_id=user_param, status=status_param)
        saloon_orders = SaloonOrder.objects.filter(customer_id=user_param, status=status_param)

        # Serialize the data
        hotel_data = HotelOrdersSerializer(hotel_orders, many=True).data
        gym_data = GymOrderSerializer(gym_orders, many=True).data
        spa_data = SpaOrdersSerializer(spa_orders, many=True).data
        saloon_data = SaloonOrdersSerializer(saloon_orders, many=True).data

        # Return response
        return Response({
            "hotel_orders": hotel_data,
            "gym_orders": gym_data,
            "spa_orders": spa_data,
            "saloon_orders": saloon_data
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def submit_review(request):
    serializer = ReviewSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Review submitted successfully!", "data": serializer.data}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['DELETE'])
def delete_booking(request):
    booking_id =request.query_params.get('booking_id')
    user_id =request.query_params.get('user_id')
    role = request.query_params.get('role')
    if not booking_id or not user_id:
        return Response({'error': 'Both booking_id and user_id are required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        if role == "hotel":
            booking = HotelOrder.objects.get(id=booking_id, customer_id=user_id)
        elif role == "spa":
            booking = SpaOrder.objects.get(id=booking_id, customer_id=user_id)
        elif role == "gym":
            booking = GymOrder.objects.get(id=booking_id, customer_id=user_id)
        elif role == "saloon":
            booking = SaloonOrder.objects.get(id=booking_id, customer_id=user_id)
        else:
            return Response({'error': 'Invalid role specified'}, status=status.HTTP_400_BAD_REQUEST)

        booking.delete()
        return Response({'message': 'Booking deleted successfully.'}, status=status.HTTP_200_OK)
    except (HotelOrder.DoesNotExist, SpaOrder.DoesNotExist, GymOrder.DoesNotExist, SaloonOrder.DoesNotExist):
        return Response({'error': 'Booking not found.'}, status=status.HTTP_404_NOT_FOUND)


import subprocess
import getpass
import os

def sync_db_from_remote():
    # === CONFIGURATION ===
    REMOTE_USER = "sadmin"
    REMOTE_HOST = "192.168.1.100"
    REMOTE_DB_NAME = "building"
    REMOTE_DB_USER = "root"
    REMOTE_DB_PASS = ""
    REMOTE_DB_PORT = 3306

    LOCAL_DB_NAME = "building"
    LOCAL_DB_USER = "root"
    LOCAL_DB_PASS = "2001"
    LOCAL_DB_PORT =3306

    DUMP_FILE = "db_dump.sql"

    # === STEP 1: Dump Remote DB over SSH ===
    print("📦 Dumping remote DB...")
    dump_cmd = (
        f'ssh {REMOTE_USER}@{REMOTE_HOST} "mysqldump -u{REMOTE_DB_USER} -p{REMOTE_DB_PASS} {REMOTE_DB_NAME}" > {DUMP_FILE}'
    )
    subprocess.run(dump_cmd, shell=True, check=True)
    print("✅ Dumped remote DB to local file")

    # === STEP 2: Import into Local DB ===
    print("📥 Importing into local DB...")
    load_cmd = (
        f'mysql -u{LOCAL_DB_USER} -p{LOCAL_DB_PASS} {LOCAL_DB_NAME} < {DUMP_FILE}'
    )
    subprocess.run(load_cmd, shell=True, check=True)
    print("✅ Loaded data into local DB")

    # === STEP 3: Clean Up ===
    os.remove(DUMP_FILE)
    print("🧹 Cleaned up dump file")


# ✅ Only run on demand, not at import
def trigger_db_sync(request):
    try:
        sync_db_from_remote()
        return JsonResponse({"status": "success"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})