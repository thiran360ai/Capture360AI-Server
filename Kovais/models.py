from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import ValidationError


# Create your models here.

class Employee(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('member', 'Member'),
        ('saloon', 'Saloon'),
        ('spa', 'Spa'),
        ('gym', 'Gym'),
        ('hotel', 'Hotel')
    )
    email = models.CharField(max_length=255, null=True, blank=True, unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')
    mobile = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255)
    attendance = models.CharField(max_length=15, null=True, blank=True)
    total_attendance = models.CharField(max_length=255, blank=True, null=True)
    image = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    success = models.BooleanField(default=False)
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


class UserDetails(models.Model):
    MEMBERSHIP_CHOICES = (
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        ('platinum', 'Platinum'),
    )
    name = models.CharField(max_length=256, blank=True, null=True)
    membership = models.CharField(max_length=20, choices=MEMBERSHIP_CHOICES, default='silver', null=True, blank=True)
    password = models.CharField(max_length=255)
    subscribed = models.BooleanField(default=False, null=True, blank=True)
    premium_amount = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class Bonus(models.Model):
    name = models.ForeignKey(Employee, on_delete=models.CASCADE)
    points = models.CharField(max_length=256, null=True, blank=True)
    is_active = models.BooleanField(default=True)


class Booking(models.Model):
    customer_id = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    time_slot = models.DateTimeField(auto_now=True)
    bonus = models.ForeignKey(Bonus, on_delete=models.CASCADE)


class SaloonOrder(models.Model):
    customer_id = models.ForeignKey(UserDetails, on_delete=models.CASCADE, null=True, blank=True)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True)
    order_type = models.CharField(max_length=255, null=True, blank=True)
    category = models.CharField(max_length=255, null=True, blank=True)
    services = models.TextField(null=True, blank=True)
    payment_status = models.CharField(max_length=255, null=True, blank=True, default='pending')
    payment_type = models.CharField(max_length=255, null=True, blank=True)
    amount = models.CharField(max_length=255, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    time = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255, null=True, blank=True)


class GymOrder(models.Model):
    customer_id = models.ForeignKey(UserDetails, on_delete=models.CASCADE, null=True, blank=True)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True)
    gender = models.CharField(max_length=255, null=True, blank=True)
    age = models.CharField(max_length=255, null=True, blank=True)
    timeslot = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    plan = models.CharField(max_length=255, null=True, blank=True)
    attendance = models.CharField(max_length=255, null=True, blank=True)
    category = models.CharField(max_length=255, null=True, blank=True)
    amount = models.TextField(null=True, blank=True)
    purchaseddate = models.TextField(null=True, blank=True)
    expiry_date = models.TextField(null=True, blank=True)
    payment_status = models.CharField(max_length=255, null=True, blank=True, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)


class SpaOrder(models.Model):
    customer_id = models.ForeignKey(UserDetails, on_delete=models.CASCADE, null=True, blank=True)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True)
    # order_type = models.CharField(max_length=255,null=True,blank=True)
    category = models.CharField(max_length=255, null=True, blank=True)
    services = models.TextField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    time = models.CharField(max_length=255, null=True, blank=True)
    amount = models.TextField(null=True, blank=True)
    payment_status = models.CharField(max_length=255, null=True, blank=True, default='pending')
    payment_type = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255, null=True, blank=True)


class Rooms(models.Model):
    room = models.IntegerField(unique=True, null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True, default='Available')


class HotelOrder(models.Model):
    customer_id = models.ForeignKey(UserDetails, on_delete=models.CASCADE, null=True, blank=True)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True)
    guest_name = models.CharField(max_length=255, null=True, blank=True)
    amount = models.CharField(max_length=255, null=True, blank=True)
    check_in = models.DateTimeField(null=True, blank=True)
    check_out = models.DateTimeField(null=True, blank=True)
    category = models.CharField(max_length=255, null=True, blank=True)
    # Many-to-many relationship with Rooms to allow multiple rooms per booking
    room_count = models.CharField(max_length=255, null=True, blank=True)
    guest_count = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True, default='Available')
    payment_status = models.CharField(max_length=255, null=True, blank=True, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.check_in and self.check_out:
            if self.check_out <= self.check_in:
                raise ValidationError({'check_out': 'Check-out date must be later than check-in date.'})


class Attendance(models.Model):
    employee_attendance = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='attendances'  # Unique related name for reverse relation
    )
    status = models.CharField(max_length=255)
    latitude = models.CharField(max_length=255, null=True, blank=True)
    longitude = models.CharField(max_length=255, null=True, blank=True)
    check_in = models.DateTimeField(null=True, blank=True)
    check_out = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.employee_attendance} - Status: {self.status}'


class Task(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True)
    assigned_to = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField()
    status = models.CharField(max_length=255, null=True, blank=True, default="pending")
