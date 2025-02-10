import datetime
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.utils.dateparse import parse_date
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.decorators import api_view
from Kovais.seriallizers import *
import traceback

@api_view(['GET'])
def users(request):
    if request.method == 'GET':
        users = UserDetails.objects.all()
        serializer = UserDetailsSerializer(users, many=True)
        return Response(serializer.data)
    


@api_view(['POST', 'GET'])
def create_Employee(request):
    if request.method == 'POST':
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            # Hash the password before saving
            serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
            user = Employee.objects.create(**serializer.validated_data)
            return Response({'message': 'User created successfully', 'user': serializer.data['username']}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'GET':
        # Return a response for GET request if needed
        # Example: Return a list of employees (or whatever data makes sense for your app)
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # In case a request method other than POST or GET is sent, you could return a method not allowed response.
    return Response({'message': 'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



@api_view(['POST'])
def Customer_login(request):
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
    orders = SaloonOrder.objects.all()
    serializer = SaloonOrdersSerializer(orders, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# @csrf_exempt
@api_view(['POST'])
def post_saloon_orders(request):
    if request.method == 'POST':
        serializer = SaloonOrdersSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()  # Save the validated data

            return Response({'message': 'Order success', 'order': serializer.data}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def post_gym_orders(request):
    if request.method == 'POST':
        serializer = GymOrderSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()  # Save the validated data

            return Response({'message': 'Order success', 'order': serializer.data}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def get_gym_orders(request):
    orders = GymOrder.objects.all()
    serializer = GymOrderSerializer(orders, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)




@api_view(['POST'])
def post_spa_orders(request):
    if request.method == 'POST':
        serializer = SpaOrdersSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()  # Save the validated data

            return Response({'message': 'Order success', 'order': serializer.data}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def get_spa_orders(request):
    orders = SpaOrder.objects.all()
    serializer = SpaOrdersSerializer(orders, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['POST'])
def post_hotel_orders(request):
    if request.method == 'POST':
        serializer = HotelOrdersSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()  # Save the validated data

            return Response({'message': 'Hotel Booking success', 'order': serializer.data}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def get_hotel_orders(request):
    orders = HotelOrder.objects.all()
    serializer = HotelOrdersSerializer(orders, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


from django.utils import timezone


@api_view(['GET'])
def filter_by_status_and_user(request, user_id):
    # Get the current date (timezone-aware)
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

import datetime

#Attendance
from datetime import datetime  # Correct import

@api_view(['POST'])
def create_attendance(request):
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
    attendance = Attendance.objects.all()
    serializer = AttendanceSerializer(attendance, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_present(request):
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