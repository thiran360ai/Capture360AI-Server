from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer
from django.shortcuts import redirect, render
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from .models import * 
from .serializers import *
from.views import *
from rest_framework.decorators import api_view
from rest_framework import status

# class UserRegistration(APIView):
#     print('APkvknfvjbvjkdbjsdfIView')
#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         print(serializer)
#         if serializer.is_valid():
#             user = serializer.save()
#             token = Token.objects.create(user=user)
#             return Response({'token': token.key}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .serializers import UserSerializer

# @api_view(['POST', 'GET'])
# def CreateUser(request):
#     if request.method == 'GET':
#         users = CustomUser.objects.all()
#         serializer = UserSerializer(users, many=True)
#         return Response(serializer.data)
    
#     if request.method == 'POST':
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             user = CustomUser.objects.create_user(**serializer.validated_data)
#             return Response("User created successfully")
#         return Response(serializer.errors, status=400)

# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from django.contrib.auth import authenticate
# from rest_framework.authtoken.models import Token
# from .serializers import UserSerializer

# @api_view(['POST'])
# def register_and_login(request):
#     if request.method == 'POST':
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             # Save the user
#             user = serializer.save()

#             # Authenticate the user
#             username = serializer.validated_data['username']
#             password = serializer.validated_data['password']
#             user = authenticate(request=request, username=username, password=password)

#             if user is not None:
#                 # If user is authenticated, generate token
#                 token, _ = Token.objects.get_or_create(user=user)
#                 return Response({'token': token.key})
#             else:
#                 return Response({'error': 'Failed to authenticate user'}, status=400)
#         else:
#             return Response(serializer.errors, status=400)
  
    
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from django.contrib.auth import authenticate
# from rest_framework.authtoken.models import Token
# from .models import CustomUser  # Import your CustomUser model

# from django.contrib.auth.hashers import check_password

# @api_view(['POST'])
# def login(request):
#     if request.method == 'POST':
#         username = request.data.get('username')
#         password = request.data.get('password')

#         # Debugging: Print received username and password
#         print("Received username:", username)
#         print("Received password:", password)

#         try:
#             # Filter user by username
#             user = CustomUser.objects.get(username=username)
#             print("Retrieved user:", user)
#         except CustomUser.DoesNotExist:
#             # If user is not found, return error response
#             print("User not found")
#             return Response({'error': 'Invalid credentials'}, status=400)

#         # Check if password matches
#         if check_password(password, user.password):
#             # If password matches, generate token
#             print("Password matched")
#             # token, _ = Token.objects.get_or_create(user=user)
#             return Response({'token': 'login successfully', 'user_id': user.id}, status=200)
#         else:
#             # If password does not match, return error response
#             print("Password did not match")
#             return Response({'error': 'Invalid credentials'}, status=400)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from .models import CustomUser
from .serializers import UserSerializer

@api_view(['POST', 'GET'])
def CreateUser(request):
    if request.method == 'GET':
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # Hash the password before saving
            serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
            user = CustomUser.objects.create(**serializer.validated_data)
            return Response({'message': 'User created successfully', 'user': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        # Debugging: Print received username and password
        print("Received username:", username)
        print("Received password:", password)

        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            print("User not found")
            return Response({'login': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        if check_password(password, user.password):
            print("Password matched")
            return Response({'Success': 'login successfully', 'user_id': user.id,'result':user.role}, status=status.HTTP_200_OK)
        else:
            print("Password did not match")
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def total_users(request):
    users = CustomUser.objects.all()
    serializer = TotalUserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Post
from .serializers import PostSerializer

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

@api_view(['POST'])
def CreatePost(request):
    if request.method == 'POST':
        
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # If the request method is not POST, return a method not allowed response
    return Response({'error': 'Method not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



@api_view(['GET'])
def Total_Post(request):
    project=Post.objects.all()
    serlizer=PostSerializer(project,many=True)
    return Response(serlizer.data, status=status.HTTP_200_OK)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import ItemList
from .serializers import ItemListSerializer

@api_view(['POST'])
def create_item_list(request):
    if request.method == 'POST':
        serializer = ItemListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'Method not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import ItemList
from .serializers import ItemListSerializer

@api_view(['GET', 'POST'])
def item_list(request):
    if request.method == 'GET':
        item_lists = ItemList.objects.all()
        serializer = ItemListSerializer(item_lists, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ItemListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({'error': 'Method not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Plan
from .serializers import PlanSerializer

@api_view(['GET', 'POST'])
def plan_list(request):
    if request.method == 'GET':
        plans = Plan.objects.all()
        serializer = PlanSerializer(plans, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PlanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response({'error': 'Method not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
