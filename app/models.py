from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


# User Model
class User(AbstractUser):
    email = models.EmailField(unique=True)  # Unique Email for authentication
    mobile_number = models.CharField(max_length=15, unique=True)  # Store phone numbers
    is_employee = models.BooleanField(default=False)  # True for shop owners
    latitude = models.FloatField(null=True, blank=True)  # User's location
    longitude = models.FloatField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)  # Optional address
    # delivers_orders = models.BooleanField(default=True) 

    USERNAME_FIELD = 'email'  # Login using Email instead of Username
    REQUIRED_FIELDS = ['username', 'mobile_number']
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='employees',  # Unique related name for groups
        related_query_name='employee',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='employees',  # Unique related name for user permissions
        related_query_name='employee',
    )
    def __str__(self):
        return self.email
    
# # Category Model
# class Category(models.Model):
#     name = models.CharField(max_length=255)

# # Shop Profile Model
# class Profile(models.Model):
#     employee = models.ForeignKey(User, on_delete=models.CASCADE)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     # shop_name
#     # shop_image = models.ImageField(upload_to='shops/',blank=True,null=True)
#     latitude = models.FloatField()
#     longitude = models.FloatField()
#     delivers_orders = models.BooleanField(default=True) 


# # Product Model
# class Product(models.Model):
#     name = models.CharField(max_length=255)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     price = models.FloatField()
#     offer_price = models.FloatField()
#     profile = models.ForeignKey(Profile, on_delete=models.CASCADE)



# # Order Model
# class Order(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     status = models.CharField(max_length=255, default='Pending')
#     timestamp = models.DateTimeField(auto_now_add=True)
#     delivery_time = models.IntegerField()
    

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    parent = models.ForeignKey(
        'self', null=True, blank=True, 
        on_delete=models.CASCADE, related_name='subcategories'
    )

    class Meta:
        app_label = 'app'  # Ensure Django knows the app

    def __str__(self):
        return f"{self.parent.name} -> {self.name}" if self.parent else self.name


class Profile(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    # //userid
    shop_name = models.CharField(max_length=255)
    shop_image = models.ImageField(upload_to='shops/', blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    delivers_orders = models.BooleanField(default=True)

    def __str__(self):
        return self.shop_name


class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    price = models.FloatField()
    offer_price = models.FloatField()
    description = models.TextField()
    # stock = models.PositiveIntegerField(default=0)
    # created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ProductVariation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variations")
    attribute_name = models.CharField(max_length=255)  # Size, Color, etc.
    attribute_value = models.CharField(max_length=255)  # Red, XL, etc.
    price = models.FloatField()
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} - {self.attribute_name}: {self.attribute_value}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductVariation, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    timestamp = models.DateTimeField(auto_now_add=True)
    delivery_time = models.IntegerField(null=True, blank=True)  # Estimated delivery time in hours
    tracking_id = models.CharField(max_length=255, unique=True, blank=True)

    def __str__(self):
        return f"Order {self.id} - {self.status}"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductVariation, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.product.name} ({self.quantity})"


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductVariation, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.product.name}"
