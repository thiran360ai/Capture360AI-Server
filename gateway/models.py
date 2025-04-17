from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
# from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  
    password = models.CharField(max_length=255)
    username = models.CharField(max_length=150, null=True, blank=True)
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='users',  # Unique related name for groups
        related_query_name='users',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='users',  # Unique related name for user permissions
        related_query_name='users',
    )

    def __str__(self):
        return self.username if self.username else self.email  # Return username or email as a fallback
class Device(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="devices")
    device = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255, null=True, blank=True)  

    def __str__(self):
        return self.device



class GPSData(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, blank=True, null=True)
    latitude = models.JSONField(default=list, null=True, blank=True)
    longitude = models.JSONField(default=list, null=True, blank=True)
    engine_status = models.JSONField(default=list, null=True, blank=True)
    speed_kmh = models.JSONField(default=list, null=True, blank=True)
    max_speed = models.JSONField(default=list, null=True, blank=True)
    battery_level = models.JSONField(default=list, null=True, blank=True)
    ignition_on = models.JSONField(default=list, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

