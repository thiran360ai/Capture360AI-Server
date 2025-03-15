from django.contrib import admin

from import_export.admin import ImportExportModelAdmin
from .models import *

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['role', 'location', 'password', 'latitude','longitude','email','profileStatus','success','mobile']

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['user_id','device_id','month','year','start_time','pause_time','resume_time','stop_time','total_hours']

