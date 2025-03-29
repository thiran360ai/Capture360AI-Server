# from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
# from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(models.Model):  
    email = models.EmailField(unique=True)  
    password=models.CharField(max_length=255)
    username = models.CharField(max_length=150,null=True,blank=True)
    # groups = models.ManyToManyField(Group, related_name="customuser_set", blank=True)
    # user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions", blank=True)

    def __str__(self):
        return self.username


class Device(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="devices")
    device = models.CharField(max_length=100)

    def __str__(self):
        return self.device



class GPSData(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE,blank=True,null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(default=timezone.now)

 