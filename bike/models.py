from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.contrib.auth import get_user_model

# User = get_user_model()

class Category(models.Model):
    image=models.ImageField(upload_to='logo_images/',null=True,blank=True)     
    
class Products(models.Model):
    Category_reference=models.ForeignKey(Category,on_delete=models.CASCADE)
    name=models.CharField(max_length=255,null=True,blank=True)
    image=models.ImageField(upload_to='bike_image/',null=True,blank=True)
    
    def __str__(self):
        return self.name      
    
class Accessories(models.Model):
    Product_reference=models.ForeignKey(Products,on_delete=models.CASCADE)
    name=models.CharField(max_length=255,blank=True,null=True)
    image=models.ImageField(max_length=256,null=True,blank=True)
    
    def __str__(self):
        return self.name if self.name else "Unnamed Accessory"
    
class Items(models.Model):
    Accessories_reference=models.ForeignKey(Accessories,on_delete=models.CASCADE)
    name=models.CharField(max_length=255,blank=True,null=True)
    image=models.ImageField(upload_to='accessories_images/',blank=True,null=True)
    price=models.TextField(null=True,blank=True)
    description=models.TextField(null=True,blank=True)
    stock = models.CharField(max_length=255,blank=True,null=True)
      
    def __str__(self):
        return self.name
    
class Banner(models.Model):
    image=models.ImageField(upload_to='banner_img/',blank=True,null=True)
    
class UserProfile(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    # phone_number = models.CharField(max_length=15, blank=True, null=True)

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='user_profiles',
        related_query_name='user_profiles',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='user_profiles',
        related_query_name='user_profiles',
    )

    def is_admin(self):
        return self.role == 'admin' and self.is_staff and self.is_superuser

    def __str__(self):
        return f"{self.username} ({self.role})"
    
# Username: admin
# Email address: admin@example.com
# Password: admin123

    
class Customer(models.Model):
    INDIAN_STATES = [
        ("AP", "Andhra Pradesh"),
        ("AR", "Arunachal Pradesh"),
        ("AS", "Assam"),
        ("BR", "Bihar"),
        ("CT", "Chhattisgarh"),
        ("GA", "Goa"),
        ("GJ", "Gujarat"),
        ("HR", "Haryana"),
        ("HP", "Himachal Pradesh"),
        ("JH", "Jharkhand"),
        ("KA", "Karnataka"),
        ("KL", "Kerala"),
        ("MP", "Madhya Pradesh"),
        ("MH", "Maharashtra"),
        ("MN", "Manipur"),
        ("ML", "Meghalaya"),
        ("MZ", "Mizoram"),
        ("NL", "Nagaland"),
        ("OD", "Odisha"),
        ("PB", "Punjab"),
        ("RJ", "Rajasthan"),
        ("SK", "Sikkim"),
        ("TN", "Tamil Nadu"),
        ("TG", "Telangana"),
        ("TR", "Tripura"),
        ("UP", "Uttar Pradesh"),
        ("UK", "Uttarakhand"),
        ("WB", "West Bengal"),
        ("AN", "Andaman and Nicobar Islands"),
        ("CH", "Chandigarh"),
        ("DN", "Dadra and Nagar Haveli and Daman and Diu"),
        ("DL", "Delhi"),
        ("LD", "Lakshadweep"),
        ("JK", "Jammu and Kashmir"),
        ("LA", "Ladakh"),
        ("PY", "Puducherry"),
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)
    state = models.CharField(max_length=2, choices=INDIAN_STATES, default="TN") 

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Contact(models.Model):
    name=models.CharField(max_length=255,null=True)
    email=models.EmailField()
    subject=models.TextField(null=True)
    description=models.TextField(null=True)
        
class Wish(models.Model):
    user = models.ForeignKey(settings.BIKE_USER_MODEL, on_delete=models.CASCADE)  
    item = models.ForeignKey(Items, on_delete=models.CASCADE)  # Reference Items instead of Products
    image = models.ImageField(upload_to='cart/', blank=True, null=True)
    name = models.TextField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)  
    added_at = models.DateTimeField(auto_now_add=True)  
    gst = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)  # GST percentage (e.g., 18.00 for 18%)
    shipping_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Shipping fee

    def total_price(self):
        """
        Calculate the total price including GST and shipping charge.
        """
        if self.price:
            base_total = self.price * self.quantity
            gst_amount = (self.gst / 100) * base_total  # Calculate GST amount
            total = base_total + gst_amount + self.shipping_charge  # Add GST & shipping
            return total
        return 0

    def __str__(self):
        return f"{self.user.username} - {self.item.name} ({self.quantity})"
    
from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField  # ✅ Use JSONField

UserProfile = get_user_model()

class Order(models.Model):
    user = models.ForeignKey(settings.BIKE_USER_MODEL, on_delete=models.CASCADE,blank=True, null=True)
    name = models.CharField(max_length=255,blank=True, null=True)  # ✅ Store Name
    address = models.TextField()  # ✅ Store Address
    wishlist_items = models.JSONField(default=list,blank=True, null=True)  # ✅ Store wishlist items as JSON
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    order_status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')],
        default='Pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"
