from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
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
    premium_amount= request.data.get('premium_amount') 

    if not name or not password:
        return JsonResponse({'error': 'Name and password are required'}, status=400)

    if UserDetails.objects.filter(name=name).exists():
        return JsonResponse({'error': 'Username already exists'}, status=400)

    # Set membership to gold if subscribed
    if subscribed and premium_amount ==20000:
        membership = 'gold'
    elif subscribed and premium_amount ==50000:
        membership = 'platinum'

    # Prepare data for serializer
    request.data['membership'] = membership  # Update membership in request data

    serializer = UserDetailsSerializer(data=request.data)
    if serializer.is_valid():
        # Hash the password before saving
        serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
        user = UserDetails.objects.create(**serializer.validated_data)
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def Emp_login(request):
    try:
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user = Employee.objects.get(username=username)
        except Employee.DoesNotExist:
            return JsonResponse({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        if check_password(password, user.password):
            # Change success to True if password is matched
            return JsonResponse({
                'Message': 'Login successfully',
                'success': True,  # Set success to True
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
