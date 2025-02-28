from django.db import models
from datetime import timedelta
from django.utils import timezone


class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('member', 'Member'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')
    location = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255)
    latitude = models.CharField(max_length=255, null=True, blank=True)
    longitude = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True, db_index=True)
    profileStatus = models.CharField(max_length=255, default="not completed", null=True, blank=True)
    success = models.CharField(max_length=255, null=True, blank=True, default='Not completed')
    mobile = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.profileStatus or self.profileStatus.strip() == "":
            self.profileStatus = "not completed"
        super().save(*args, **kwargs)


class Attendance(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    device_id = models.CharField(max_length=255, null=True, blank=True)
    month = models.IntegerField(null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    pause_time = models.DateTimeField(null=True, blank=True)
    resume_time = models.DateTimeField(null=True, blank=True)
    stop_time = models.DateTimeField(null=True, blank=True)
    total_hours = models.DurationField(default=timedelta(0))  # ✅ Fix Here

    def __str__(self):
        return f"{self.device_id} - {self.month}/{self.year}"