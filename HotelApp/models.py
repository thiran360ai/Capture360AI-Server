from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Employee(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('member', 'Member')
    )
    email = models.CharField(max_length=255, null=True, blank=True, unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')
    mobile = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255)
    image = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    success = models.BooleanField(default=False)
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='hotel_employees',  # Unique related name for groups
        related_query_name='hotel_employee',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='hotel_employees',  # Unique related name for user permissions
        related_query_name='hotel_employee',
    )

class UserDetails(models.Model):
    name = models.CharField(max_length=256, blank=True, null=True)
    password = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15,null=True,blank=True)

    def __str__(self):
        return self.name
