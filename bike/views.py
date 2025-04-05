import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import *
from django.core.files.base import ContentFile
from rest_framework import status
from .serializers import *
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth import login, logout
from .serializers import *
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.exceptions import TokenError



# Category crud
class bikeView(APIView):
    
    def get(self,request):
        bike_logo=Category.objects.all()
        bike_serializer=CategorySerializer(bike_logo,many=True).data
        return Response({'category':bike_serializer})
    
    def post(self,request):
        bike_logos=CategorySerializer(data=request.data)
        if bike_logos.is_valid():
            bike_logos.save()
            return Response({"message": "Category created successfully"}, status=status.HTTP_201_CREATED)
        return Response(bike_logos.errors, status=status.HTTP_400_BAD_REQUEST)

class bikeViewById(APIView):
    
    def get(self,request,id):
        try:
            maths=Category.objects.get(id=id)
        except Category.DoesNotExist:
            return Response({"error": "Category not found."}, status=status.HTTP_404_NOT_FOUND)
        single_maths=CategorySerializer(maths).data
        return Response(single_maths)
    
    def patch(self,request,id):
        try:
            science=Category.objects.get(id=id)
        except Category.DoesNotExist:
            return Response({"error": "Category not found."}, status=status.HTTP_404_NOT_FOUND)
        
        issue=CategorySerializer(science,data=request.data,partial=True)
        if issue.is_valid():
            issue.save()
            return Response({"message": "Category updated successfully", "category": issue.data}, status=status.HTTP_200_OK)
        return Response(issue.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,id):
        social=Category.objects.get(id=id)
        social.delete()
        return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
# product crud
    
class ProductListView(APIView):
    permission_classes = [AllowAny]  

    def get(self, request):
        print(f"🔍 Request User: {request.user}")
        print(f"🔑 Is Authenticated: {request.user.is_authenticated}")
        
        products = Products.objects.all()  
        serializer = ProductsSerializer(products, many=True)
        return Response(serializer.data)  
    
    def post(self,request):
        levels=ProductsSerializer(data=request.data)
        if levels.is_valid():
            levels.save()
            return Response({"message": "product created successfully"}, status=status.HTTP_201_CREATED)
        return Response(levels.errors, status=status.HTTP_400_BAD_REQUEST)
    
class productlistViewById(APIView):
    
    def get(self,request,id):
        try:
            line=Products.objects.get(id=id)
        except Products.DoesNotExist:
            return Response({"error":"product not found"},status=status.HTTP_404_NOT_FOUND)
        single_line=ProductsSerializer(line).data
        return Response(single_line)
    
    def patch(self,request,id):
        try:
            double=Products.objects.get(id=id)
        except Products.DoesNotExist:
            return Response({"error": "product not found."}, status=status.HTTP_404_NOT_FOUND)
        
        passin = ProductsSerializer(double,data=request.data,partial=True)
        if passin.is_valid():
            passin.save()
            return Response({"message": "product updated successfully", "category": passin.data}, status=status.HTTP_200_OK)
        return Response(passin.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,id):
        proper=Products.objects.get(id=id)
        proper.delete()
        return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
# Accesories crud

class accesoriesView(APIView):
    def get(self,request):
        high=Accessories.objects.all()
        high_level=AccessoriesSerializer(high,many=True).data
        return Response({'accessory':high_level})
    
    def post(self,request):
        low=AccessoriesSerializer(data=request.data)
        if low.is_valid():
            low.save()
            return Response({"message": "accessory created successfully"}, status=status.HTTP_201_CREATED)
        return Response(low.errors, status=status.HTTP_400_BAD_REQUEST)
    
class accesoriesViewById(APIView):
    
    def get(self,request,id):
        try:
            after=Accessories.objects.get(id=id)
        except Accessories.DoesNotExist:
            return Response({"error":"accessory not found"},status=status.HTTP_404_NOT_FOUND)
        change=AccessoriesSerializer(after).data
        return Response(change)
            
    
    def patch(self,request,id):
        try:
            straight=Accessories.objects.get(id=id)
        except Accessories.DoesNotExist:
            return Response({"error": "accessory not found."}, status=status.HTTP_404_NOT_FOUND)
        
        falin=AccessoriesSerializer(straight,data=request.data,partial=True)
        if falin.is_valid():
            falin.save()
            return Response({"message": "accessory updated successfully", "category": falin.data}, status=status.HTTP_200_OK)
        return Response(falin.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,id):
        prop=Accessories.objects.get(id=id)
        prop.delete()
        return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
# Wish crud

# Retrieve the Wish list
# class WishListView(generics.ListAPIView):
#     serializer_class = WishSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return Wish.objects.filter(user=self.request.user).select_related('item')  # Optimized query
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Wish
from .serializers import WishSerializer
from rest_framework.permissions import AllowAny



from rest_framework.permissions import AllowAny
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Wish

from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404
from .models import Wish, Items
from .serializers import WishSerializer

# ✅ 1️⃣ List Wishlist Items
class WishListView(generics.ListAPIView):
    serializer_class = WishSerializer
    permission_classes = [AllowAny]  # Anyone can view wishlist

    def get_queryset(self):
        return Wish.objects.all().select_related('item')  # Fetch items too

# ✅ 2️⃣ Add Item to Wishlist
class AddToWishView(generics.CreateAPIView):
    serializer_class = WishSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        item_id = request.data.get('item_id')
        item = get_object_or_404(Items, id=item_id)

        wish_item, created = Wish.objects.get_or_create(user=request.user, item=item)

        if not created:
            wish_item.quantity += 1
            wish_item.save()

        return Response({'message': 'Item added to wishlist successfully'}, status=status.HTTP_201_CREATED)

# ✅ 3️⃣ Send Wishlist via Email

from django.conf import settings
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from .models import Wish, Order, UserProfile  

# class SendWishEmailView(generics.CreateAPIView):
#     permission_classes = [AllowAny]

#     def send_wishlist_email(self, name, email, address):
#         wishlist_items = Wish.objects.all()

#         if not wishlist_items.exists():
#             return {"message": "No items in wishlist"}

#         # ✅ Create or Get User
#         user, created = UserProfile.objects.get_or_create(email=email, defaults={"username": name})

#         # ✅ Create Order
#         order_data = {
#             "name": name,
#             "address": address,
#             "wishlist_items": [{"name": w.item.name, "price": str(w.item.price)} for w in wishlist_items],
#             "total_amount": sum(w.total_price() for w in wishlist_items),
#             "user": user,
#         }
#         new_order = Order.objects.create(**order_data)
        
#         # ✅ Send Email
#         email_subject = f"Order Details for {name}"
#         email_body = f"Hello {name},\n\nYour order has been placed successfully!\n\n"
#         email_body += f"📍 Address: {address}\n\n"

#         for item in new_order.wishlist_items:
#             email_body += f"🔹 {item['name']} - ${item['price']}\n"

#         email_body += f"\n💰 Total Order Amount: ${new_order.total_amount}\n"
#         email_body += "\nThank you for using our service!"

#         send_mail(
#             subject=email_subject,
#             message=email_body,
#             from_email=settings.EMAIL_HOST_USER,
#             recipient_list=[email],
#             fail_silently=False,
#         )

#         return {"message": "Order created successfully", "order_id": new_order.id}

#     def post(self, request, *args, **kwargs):
#         name = request.data.get("name")
#         email = request.data.get("email")
#         address = request.data.get("address")

#         if not name or not email or not address:
#             return Response({"error": "Name, email, and address are required"}, status=status.HTTP_400_BAD_REQUEST)

#         email_response = self.send_wishlist_email(name, email, address)
#         return Response(email_response, status=status.HTTP_200_OK)
import logging
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Wish, Order, UserProfile
from .serializers import WishEmailSerializer  # You need a serializer

logger = logging.getLogger(__name__)

class SendWishEmailView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = WishEmailSerializer  # Ensure you have a serializer

    def send_wishlist_email(self, name, email, address):
        try:
            wishlist_items = Wish.objects.all()

            if not wishlist_items.exists():
                return {"message": "No items in wishlist"}

            # ✅ Create or Get User
            user, created = UserProfile.objects.get_or_create(email=email, defaults={"username": name})

            # ✅ Create Order
            total_amount = sum(w.total_price() for w in wishlist_items)
            new_order = Order.objects.create(
                name=name,
                address=address,
                user=user,
                total_amount=total_amount
            )

            # ✅ Send Email
            email_subject = f"Order Details for {name}"
            email_body = f"Hello {name},\n\nYour order has been placed successfully!\n\n"
            email_body += f"📍 Address: {address}\n\n"

            for w in wishlist_items:
                email_body += f"🔹 {w.item.name} - ${w.item.price}\n"

            email_body += f"\n💰 Total Order Amount: ${total_amount}\n"
            email_body += "\nThank you for using our service!"

            send_mail(
                subject=email_subject,
                message=email_body,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )

            return {"message": "Order created successfully", "order_id": new_order.id}

        except Exception as e:
            logger.error(f"Email sending failed: {e}")
            return {"error": str(e)}

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        name = serializer.validated_data["name"]
        email = serializer.validated_data["email"]
        address = serializer.validated_data["address"]

        email_response = self.send_wishlist_email(name, email, address)

        if "error" in email_response:
            return Response(email_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(email_response, status=status.HTTP_200_OK)

# class WishListView(generics.ListAPIView):
#     serializer_class = WishSerializer
#     permission_classes = [AllowAny] 
#     # permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return Wish.objects.filter(user=self.request.user).select_related('item')

#     def send_wishlist_email(self, name, email, user):
#         wishlist_items = Wish.objects.filter(user=user).select_related('item')

#         if not wishlist_items.exists():
#             return {"message": "No items in wishlist"}

#         # Format email content
#         email_subject = f"Wishlist Details for {name}"
#         email_body = f"Hello {name},\n\nHere are your wishlist items:\n\n"

#         for wish in wishlist_items:
#             email_body += f"🔹 {wish.item.name} - ${wish.item.price}\n"

#         email_body += "\nThank you for using our service!"

#         send_mail(
#             subject=email_subject,
#             message=email_body,
#             from_email=settings.EMAIL_HOST_USER,
#             recipient_list=[email],  # Send to entered email
#             fail_silently=False,
#         )
#         return {"message": f"Wishlist sent successfully to {email}"}

#     def post(self, request, *args, **kwargs):
#         name = request.data.get('name')
#         email = request.data.get('email')

#         if not name or not email:
#             return Response({"error": "Name and email are required"}, status=status.HTTP_400_BAD_REQUEST)

#         user = request.user
#         email_response = self.send_wishlist_email(name, email, user)
#         return Response(email_response, status=status.HTTP_200_OK)


# Add an item to Wish or update quantity
# class AddToWishView(generics.CreateAPIView):
#     serializer_class = WishSerializer
#     permission_classes = [IsAuthenticated]

#     def post(self, request, *args, **kwargs):
#         item_id = request.data.get('item_id')
#         item = get_object_or_404(Items, id=item_id)

#         wish_item, created = Wish.objects.get_or_create(user=request.user, item=item)

#         if not created:
#             wish_item.quantity += 1
#             wish_item.save()

#         return Response({'message': 'Item added to Wish successfully'}, status=status.HTTP_201_CREATED)
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Items, Wish
from .serializers import WishSerializer

class AddToWishView(generics.CreateAPIView):
    serializer_class = WishSerializer
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        item_id = request.data.get('item_id')
        item = get_object_or_404(Items, id=item_id)

        # Check if the item already exists in the user's wish list
        wish_item, created = Wish.objects.get_or_create(user=request.user, item=item)

        if not created:
            wish_item.quantity += 1
            wish_item.save()

        # Return the serialized wish item with item details
        serializer = WishSerializer(wish_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# Update quantity or remove from Wish
class UpdateWishView(generics.UpdateAPIView):
    serializer_class = WishSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        wish_id = self.kwargs['wish_id']
        wish_item = get_object_or_404(Wish, id=wish_id, user=request.user)
        action = request.data.get('action')

        if action == "increment":
            wish_item.quantity += 1
        elif action == "decrement":
            if wish_item.quantity > 1:
                wish_item.quantity -= 1 
            else:
                wish_item.delete()
                return Response({'message': 'Item removed from Wish'}, status=status.HTTP_204_NO_CONTENT)

        wish_item.save()
        return Response({'message': 'Wish updated successfully', 'quantity': wish_item.quantity, 'total_price': wish_item.total_price()})


# Remove an item from Wish
class RemoveWishItemView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        wish_id = kwargs.get('wish_id') 
        wish_item = get_object_or_404(Wish, id=wish_id, user=request.user)
        wish_item.delete()
        return Response({'message': 'Item removed from Wish'}, status=status.HTTP_204_NO_CONTENT)
    
# Items Crud

class itemsView(APIView):
    def get(self,request):
        key=Items.objects.all()
        key_level=itemSerializer(key,many=True).data
        count = key.count()  # Count the total number of items
        return Response({'total_items': count,'accessory':key_level})
    
    def post(self,request):
        keylow=itemSerializer(data=request.data)
        if keylow.is_valid():
            keylow.save()
            return Response({"message": "accessory created successfully"}, status=status.HTTP_201_CREATED)
        return Response(keylow.errors, status=status.HTTP_400_BAD_REQUEST)
    
class itemsViewById(APIView):
    
     def get(self,request,id):
        try:
            afters=Items.objects.get(id=id)
        except Items.DoesNotExist:
            return Response({"error":"accessory not found"},status=status.HTTP_404_NOT_FOUND)
        changed=itemSerializer(afters).data
        return Response(changed)
            
    
     def patch(self,request,id):
        try:
            down=Items.objects.get(id=id)
        except Items.DoesNotExist:
            return Response({"error": "accessory not found."}, status=status.HTTP_404_NOT_FOUND)
        
        falof=itemSerializer(down,data=request.data,partial=True)
        if falof.is_valid():
            falof.save()
            return Response({"message": "accessory updated successfully", "category": falof.data}, status=status.HTTP_200_OK)
        return Response(falof.errors, status=status.HTTP_400_BAD_REQUEST)
    
     def delete(self,request,id):
        proper=Items.objects.get(id=id)
        proper.delete()
        return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    

# Banner CRUD    
class BannerListCreate(APIView):
    
    def get(self, request):
        banners = Banner.objects.all()
        serializer = BannerSerializer(banners, many=True)
        return Response({"banners": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BannerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Banner created successfully", "banner": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BannerDetail(APIView):

    def get(self, request, id):
        try:
            banner = Banner.objects.get(id=id)
        except Banner.DoesNotExist:
            return Response({"error": "Banner not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = BannerSerializer(banner)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, id):
        try:
            banner = Banner.objects.get(id=id)
        except Banner.DoesNotExist:
            return Response({"error": "Banner not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = BannerSerializer(banner, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Banner updated successfully", "banner": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            banner = Banner.objects.get(id=id)
        except Banner.DoesNotExist:
            return Response({"error": "Banner not found."}, status=status.HTTP_404_NOT_FOUND)

        banner.delete()
        return Response({"message": "Banner deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
  
# Customer crud
class CustomerListCreateView(APIView):

  def get(self,request):
      customers=Customer.objects.all()
      customserial=CustomerSerializer(customers,many=True)
      return Response({"customer": customserial.data}, status=status.HTTP_200_OK)
  
  def post(self,request):
      customserial=CustomerSerializer(data=request.data)
      if customserial.is_valid():
        customserial.save()
        return Response({"message": "customer created successfully", "banner": customserial.data}, status=status.HTTP_201_CREATED)
      return Response(customserial.errors, status=status.HTTP_400_BAD_REQUEST)
  
class CustomerDetailView(APIView):
    def get(self, request, id):
        try:
            bannerial = Customer.objects.get(id=id)
        except Customer.DoesNotExist:
            return Response({"error": "customer not found."}, status=status.HTTP_404_NOT_FOUND)

        serializerersial = CustomerSerializer(bannerial)
        return Response(serializerersial.data, status=status.HTTP_200_OK)
    
    def patch(self, request, id):
        try:
            bannerial = Customer.objects.get(id=id)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)

        Customses = BannerSerializer(bannerial, data=request.data, partial=True)
        if Customses.is_valid():
            Customses.save()
            return Response({"message": "customer updated successfully", "banner": Customses.data}, status=status.HTTP_200_OK)
        return Response(Customses.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        try:
            bannerses = Customer.objects.get(id=id)
        except Customer.DoesNotExist:
            return Response({"error": "customer not found."}, status=status.HTTP_404_NOT_FOUND)

        bannerses.delete()
        return Response({"message": "customers deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class contactView(APIView):
    def get(self,request):
      contacts=Contact.objects.all()
      contactserial=CustomerSerializer(contacts,many=True)
      return Response({"customer": contactserial.data}, status=status.HTTP_200_OK)
  
    def post(self,request):
      contactserial=CustomerSerializer(data=request.data)
      if contactserial.is_valid():
        contactserial.save()
        return Response({"message": "customer created successfully", "banner": contactserial.data}, status=status.HTTP_201_CREATED)
      return Response(contactserial.errors, status=status.HTTP_400_BAD_REQUEST)      
    

# Authenticated crud

User = get_user_model()

# User Registration View
class UserSignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        
        return Response({"error": "Signup failed", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# User Login View
class UserLoginView(APIView):
    permission_classes = []

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user:
            user = UserProfile.objects.get(id=user.id)  
            print(f"DEBUG: Username={user.username}, Role={user.role}")  # Debugging output

            refresh = RefreshToken.for_user(user)  
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "role": user.role,  # ✅ This should return 'admin' correctly
                }
            }, status=status.HTTP_200_OK)

        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)



class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        print("Received Refresh Token:", refresh_token)  # Debugging Line

        if not refresh_token:
            print("Error: Refresh token not provided")
            return Response({"error": "Refresh token required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        except TokenError as e:
            print("Token Error:", str(e))  # Debugging Line
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("Unexpected Error:", str(e))  # Debugging Line
            return Response({"error": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

User = get_user_model()

class UserSignupView(APIView):
    permission_classes = [AllowAny]  # Allow anyone to sign up
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully", "user_id": user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminSignupView(APIView):
    permission_classes = [IsAdminUser]  # Only allow admin users to create admins

    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "Admin created successfully", "user_id": user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# from rest_framework import generics, status
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from django.shortcuts import get_object_or_404
# from .models import Order, Wish
# from .serializers import OrderSerializer

# # ✅ 1️⃣ Create Order from Wishlist
# class CreateOrderView(generics.CreateAPIView):
#     serializer_class = OrderSerializer
#     permission_classes = [AllowAny] 
#     # permission_classes = [IsAuthenticated]

#     def post(self, request, *args, **kwargs):
#         user_wishlist = Wish.objects.filter(user=request.user)
        
#         if not user_wishlist.exists():
#             return Response({"error": "Your wishlist is empty"}, status=status.HTTP_400_BAD_REQUEST)

#         order = Order.objects.create(user=request.user)
#         order.wishlist_items.set(user_wishlist)  # Add wishlist items to order
#         order.save()

#         return Response({"message": "Order placed successfully", "order_id": order.id}, status=status.HTTP_201_CREATED)

# ✅ 2️⃣ List All Orders of a User
from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer

class OrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.AllowAny]
# Open for all users
