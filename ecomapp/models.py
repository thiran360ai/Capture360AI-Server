from django.db import models
from django.contrib.auth.models import AbstractUser


# Custom User Model
class Customer(AbstractUser):
    
    
    ROLE_CHOICES = [
        ('shopkeeper', 'Shopkeeper'),
        ('customer', 'Customer'),
        ]

    email = models.EmailField(unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=15, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer',blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    user_address = models.TextField(null=True, blank=True)


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='ecom_employees',
        related_query_name='ecom_employee',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='ecom_employees',
        related_query_name='ecom_employee',
    )

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"


class Banner(models.Model):
    shopkeeper = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="banners", help_text="Shopkeeper who owns the banner")
    title = models.CharField(max_length=255, help_text="Title of the banner")
    image = models.ImageField(upload_to="banners/", help_text="Upload banner image")
    description = models.TextField(blank=True, help_text="Short description")
    prize_offer = models.CharField(max_length=255, help_text="Prize or discount details")
    start_date = models.DateTimeField(help_text="Banner start date & time")
    end_date = models.DateTimeField(help_text="Banner end date & time")
    is_active = models.BooleanField(default=True, help_text="Is the banner active?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.shopkeeper.username}"


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, help_text="Category name")
    image = models.ImageField(upload_to="category_images/", blank=True, null=True, help_text="Upload category image")

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    name = models.CharField(max_length=255, unique=True, help_text="Subcategory name")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='subcategories', help_text="Parent category"
    )
    image = models.ImageField(upload_to="subcategory_images/", blank=True, null=True, help_text="Upload subcategory image")

    def __str__(self):
        return f"{self.category.name} -> {self.name}"


class Profile(models.Model):
    employee = models.ForeignKey(Customer, on_delete=models.CASCADE, help_text="Shop owner (employee)")
    shop_name = models.CharField(max_length=255, help_text="Name of the shop")
    shop_image = models.ImageField(upload_to='shops/', blank=True, null=True, help_text="Upload shop image")
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)  
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True, help_text="Shop category")
    subcategory = models.ForeignKey('Subcategory', on_delete=models.SET_NULL, null=True, blank=True, help_text="Shop subcategory")
    phone_number = models.CharField(max_length=15, blank=True, null=True, help_text="Contact number of the shop")
    email = models.EmailField(blank=True, null=True, help_text="Shop email")
    opening_time = models.TimeField(help_text="Opening time of the shop")
    closing_time = models.TimeField(help_text="Closing time of the shop")
    delivers_orders = models.BooleanField(default=True, help_text="Does the shop provide delivery?")
    is_verified = models.BooleanField(default=False, help_text="Is the shop verified by the admin?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.shop_name



class Product(models.Model):
    shop = models.ForeignKey('Profile', on_delete=models.CASCADE, help_text="Shop selling the product")
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, help_text="Product category")
    subcategory = models.ForeignKey('Subcategory', on_delete=models.SET_NULL, null=True, blank=True, help_text="Product subcategory")
    name = models.CharField(max_length=255, help_text="Product name")
    brand = models.CharField(max_length=255, blank=True, null=True, help_text="Brand name")
    description = models.TextField(blank=True, null=True, help_text="Detailed product description")
    warranty = models.CharField(max_length=255, blank=True, null=True, help_text="Warranty details")
    return_policy = models.CharField(max_length=255, blank=True, null=True, help_text="Return policy details")
    is_active = models.BooleanField(default=True, help_text="Is the product available?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to="product_images/", help_text="Upload product image")

    def __str__(self):
        return f"Image of {self.product.name}"


class ProductVariation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variations')
    
    variation_type = models.CharField(
        max_length=50, 
        choices=[
            ('weight', 'Weight (e.g., 100g, 250g)'),  # For items like soap, flour, etc.
            ('flavor', 'Flavor (e.g., Rose, Lemon, Aloe)'),  # For soaps, drinks, etc.
            ('size', 'Size (e.g., S, M, L)'),  # For clothing, shoes
            ('color', 'Color (e.g., Red, Blue, Black)'),  # For T-shirts, electronics
            ('storage', 'Storage (e.g., 64GB, 128GB)'),  # For phones, laptops
        ], 
        help_text="Type of variation (weight, flavor, size, color, etc.)"
    )

    value = models.CharField(max_length=255, help_text="E.g., '250g', 'Rose', 'Red', '128GB'")  
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price of this variation")  
    offer_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Discounted price")  
    stock = models.PositiveIntegerField(help_text="Available stock for this variation")  

    def __str__(self):
        return f"{self.product.name} - {self.variation_type}: {self.value}"


class Cart(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.email}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product_variation = models.ForeignKey(ProductVariation, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product_variation.product.name} - {self.quantity} pcs"
    

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Order {self.id} - {self.status}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_variation = models.ForeignKey(ProductVariation, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product_variation.product.name} - {self.quantity} pcs"


class Wishlist(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.email} - {self.product.name}"



class Review(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], help_text="1 to 5 stars")
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.product.name} ({self.rating} Stars)"


class Address(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} - {self.city}, {self.state}"


class Payment(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50, choices=[('COD', 'Cash on Delivery'), ('Online', 'Online Payment')])
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.order.id} - {self.status}"


class DeliveryPartner(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    vehicle_number = models.CharField(max_length=20, blank=True, null=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.email} - Available: {self.is_available}"


class OrderTracking(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='tracking')
    status = models.CharField(max_length=50, choices=[
        ('order_placed', 'Order Placed'),
        ('packed', 'Packed'),
        ('shipped', 'Shipped'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
    ])
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.order.id} - {self.status}"


class Notification(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} - Read: {self.is_read}"
    

    
