from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, Group, Permission
import uuid

# Organization Model with Latitude & Longitude
class Organization(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.EmailField()
    website = models.URLField()
    logo = models.ImageField(upload_to='logos/')
    key = models.CharField(max_length=10, unique=True, editable=False, blank=True)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = str(uuid.uuid4().hex[:10]).upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.key

# Employee Model
# The `Employee` class defines a model for employees with various fields such as email, device ID,
# role, organizations, and permissions in a Django application.
class Employee(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('member', 'Member'),
    )
    email = models.EmailField(unique=True, blank=True, null=True)
    device_id = models.CharField(max_length=255, unique=True, blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')
    organizations = models.ManyToManyField(Organization, related_name="employees")
    employee_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name='employee_groups',
        related_query_name='employee_group',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='employee_permissions',
        related_query_name='employee_permission',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'organizations']

    def __str__(self):
        return self.name




class Device(models.Model):
    device_id = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(Employee, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)  # Active field for device status

    def __str__(self):
        return f"{self.device_id} - {self.user.name}"

from django.db import models
from django.utils import timezone
from datetime import timedelta

from django.db import models
from django.utils import timezone

from django.db import models
from django.utils import timezone
from datetime import timedelta

import uuid  # For generating unique session IDs
from datetime import timedelta
from django.db import models
from django.utils import timezone

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    logs = models.JSONField(default=list)  # Logs each attendance entry
    total_hours = models.FloatField(default=0)  # Stores total working hours
