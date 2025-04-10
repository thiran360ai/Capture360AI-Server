from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Device, GPSData

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):  # Extend UserAdmin for better UI
    list_display = ("username", "email",  "password")
    search_fields = ("username", "email")
    ordering = ("email",)

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ("user", "device")


@admin.register(GPSData)
class GPSDataAdmin(admin.ModelAdmin):
    list_display = ("device", "location", "timestamp")

