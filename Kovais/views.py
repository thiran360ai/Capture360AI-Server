import datetime
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.utils.dateparse import parse_date
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.decorators import api_view
from .seriallizers import *  
from .models import * 
import traceback
import asyncio

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
    


@api_view(['POST', 'GET'])
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
        serializer =  EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            # Hash the password before saving
            serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
            serializer.validated_data['success'] = True
            user = Employee.objects.create(**serializer.validated_data)
            return Response({'message': 'User created successfully', 'user': serializer.data['username'],'success':serializer.data['success']}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    elif request.method == 'GET':
        # Return a response for GET request if needed
        # Example: Return a list of employees (or whatever data makes sense for your app)
        employees =Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # In case a request method other than POST or GET is sent, you could return a method not allowed response.
    return Response({'message': 'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



@api_view(['POST'])
def Customer_login(request):
    """
    API endpoint for customer login.

    Accepts the following parameters in the request body:
    - username: The username of the customer attempting to login.
    - password: The password of the customer.

    Returns a JSON response containing the message "login successfully" and the customer's username and membership if the login is successful.
    Returns a JSON object with an error message if the login fails.

    Returns:
    - 200 OK: A JSON object with a success message, username, and membership if credentials are valid.
    - 400 Bad Request: A JSON object with an error message if credentials are invalid.
    - 500 Internal Server Error: A JSON object with an error message if an unexpected error occurs.
    """
    try:
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user = UserDetails.objects.get(name=username)
        except UserDetails.DoesNotExist:
            
            return JsonResponse({'login': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        if check_password(password, user.password):
            
            return JsonResponse({'Message': 'login successfully', 'username': user.name,'membership':user.membership}, status=status.HTTP_200_OK)
        else:
            
            return JsonResponse({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
            # Print the full traceback to debug the issue
        traceback.print_exc()
        return JsonResponse({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
    """
    Creates a new user with the given details.

    Args:
        request: The POST request containing the user details.

    Returns:
        A JSON response containing the message "User created successfully" if the user is created successfully.
        A JSON response containing error details if user creation fails.

    Raises:
        400: If the required fields are not provided.
        400: If the username already exists.
        400: If the premium_amount is invalid.
    """
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

    # Set membership based on subscription and premium amount
    if subscribed and premium_amount == 20000:
        membership = 'gold'
    elif subscribed and premium_amount == 50000:
        membership = 'platinum'

    # Create a mutable copy of request data
    data = request.data.copy()
    data['membership'] = membership

    serializer = UserDetailsSerializer(data=data)
    if serializer.is_valid():
        serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
        serializer.save()
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
                'id':user.id,
                'username': user.username,
                'role': user.role
            }, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'error': 'Invalid credentials','success': False }, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        # Print the full traceback to debug the issue
        traceback.print_exc()
        return JsonResponse({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
        
        if serializer.is_valid():
            serializer.save()  # Save the validated data

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
            serializer.save()  # Save the validated data

            return Response({'message': 'Order success', 'order': serializer.data}, status=status.HTTP_201_CREATED)
        
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



@api_view(['POST'])
def post_hotel_orders(request):
    """
    API endpoint to create a new hotel order.

    Accepts the following parameters in the request body:
    - username: The username of the customer making the booking.
    - amount: The total amount of the booking.
    - category: The category of the booking (e.g. 'single', 'double', etc.).
    - check_in: The check-in date of the booking in the format 'YYYY-MM-DD'.
    - check_out: The check-out date of the booking in the format 'YYYY-MM-DD'.
    - room_count: The number of rooms booked.
    - guest_count: The number of guests in the booking.

    Returns a JSON object with the newly created order details if the creation is successful.
    Returns a JSON object with an error message if the creation fails.
    """
    if request.method == 'POST':
        serializer = HotelOrdersSerializer(data=request.data)        
        if serializer.is_valid():
            if serializer.validated_data['status'] =="" or "booked":
                serializer.validated_data['status'] = "Booked"
            serializer.save()  # Save the validated data

            return Response({'message': 'Hotel Booking success', 'order': serializer.data}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT'])
def update_hotel_orders(request):
 
    """
    API endpoint to update a specific hotel order record based on customer id.

    Accepts the following parameters in the request body:
    - status: The status to update the order record with. Accepted values are 'check_in' and 'check_out'.
    - customer_id: The id of the customer making the request.

    Returns a JSON object with the updated order record details if the update is successful.
    Returns a JSON object with an error message if the update fails.
    """

    try:
        param = request.query_params.get('customer_id')
        order_param = request.query_params.get('order_id')
        hotel = HotelOrder.objects.get(customer_id =param,id=order_param)  # Fetch the specific hotel order record by primary key
    except HotelOrder.DoesNotExist:
        return Response({'error': 'Hotel order record not found.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = HotelOrdersSerializer(hotel, data=request.data,partial =True)
    if serializer.is_valid():
        if request.data.get('status')=='check_in':
            serializer.validated_data['status']='checked_in'
            serializer.validated_data['check_in'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if request.data.get('status')=='check_out':
            serializer.validated_data['status']='checked_out'
            serializer.validated_data['check_out'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
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

    orders = HotelOrder.objects.all()
    serializer = HotelOrdersSerializer(orders, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_hotel_order_status(request):
    """
    API endpoint to fetch all hotel orders based on their status.

    Accepts the following parameter in the request query string:
    - status: The status of the orders to fetch. Accepted values are 'Booked', 'checked_in', 'checked_out'.

    Returns a JSON object with the list of hotel orders if the fetch is successful.
    Returns a JSON object with an error message if the fetch fails.
    """
    status_param = request.query_params.get('status', None).lower()
    
    try:
        print(status)
        order = HotelOrder.objects.filter(status=status_param)
        if not order.exists():
            return Response({'message': 'No hotel orders found for the given status.'}, status=status.HTTP_404_NOT_FOUND)
        serializer =HotelOrdersSerializer(order,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
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



#Attendance
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

        return Response({'message': 'Checked out successfully', 'user': AttendanceSerializer(attendance_record).data}, status=200)

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
        hotel = HotelOrder.objects.get(customer_id =param,id=order_param)  # Fetch the specific hotel order record by primary key
    except HotelOrder.DoesNotExist:
        return Response({'error': 'Hotel order record not found.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = HotelOrdersSerializer(hotel, data=request.data,partial =True)
    if serializer.is_valid():
        if request.data.get('payment_status')=='paid':
            serializer.validated_data['payment_status']='paid'
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)