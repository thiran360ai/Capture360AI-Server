from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth.hashers import check_password
from asgiref.sync import sync_to_async
import traceback
from django.contrib.auth.hashers import check_password,make_password
from django.utils.timezone import now
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from .serializers import *
# Create your views here.


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
    phone_number = request.data.get('phone_number')
    password = request.data.get('password')


    if not name or not password:
        return JsonResponse({'error': 'Name and password are required'}, status=400)

    if UserDetails.objects.filter(phone_number=phone_number).exists():
        return JsonResponse({'error': 'Username already exists'}, status=400)

    
    serializer = UserDetailsSerializer(data=data)
    if serializer.is_valid():
        serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
        serializer.save()
        return Response({'message': 'User created successfully', 'user': serializer.data},
                        status=status.HTTP_201_CREATED)

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
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')

        try:
            user = Employee.objects.get(phone_number=phone_number)
        except Employee.DoesNotExist:
            return JsonResponse({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        if check_password(password, user.password):
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
        traceback.print_exc()
        return JsonResponse({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def customer_login(request):
    try:
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')

        if not username or not password:
            return JsonResponse({'error': 'phone_number and password are required', 'success': False}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UserDetails.objects.get(phone_number=phone_number)
        except UserDetails.DoesNotExist:
            return JsonResponse({'error': 'Invalid credentials', 'success': False}, status=status.HTTP_400_BAD_REQUEST)

        if check_password(password, user.password):
            user.save()

            # ✅ Return the correct response
            response_data = {
                'Message': 'Login successful',
                'success': True,
                'user_id': user.id,
                'username': user.name
            }
            return JsonResponse(response_data, status=status.HTTP_200_OK)

        else:
            return JsonResponse({'error': 'Invalid credentials', 'success': False}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'error': 'Internal server error', 'success': False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
