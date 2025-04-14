from django.contrib import admin
from .models import Organization, Employee, Device

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone', 'email', 'website', 'key')
    search_fields = ('name', 'email')
    list_filter = ('name',)

from django.contrib import admin
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'role', 'get_organizations', 'employee_id', 'is_active')
    search_fields = ('name', 'email', 'employee_id')
    list_filter = ('role', 'is_active')  # Remove 'organizations' from list_filter

    def get_organizations(self, obj):
        return ", ".join([org.name for org in obj.organizations.all()])
    
    get_organizations.short_description = "Organizations"  # Column Name in Admin

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'user', 'is_active')
    search_fields = ('device_id', 'user__name', 'user__email')
    list_filter = ('is_active',)


from django.contrib import admin
from .models import Attendance

# @admin.register(Attendance)
# class AttendanceAdmin(admin.ModelAdmin):
#     list_display = ('employee', 'date', 'check_in_time', 'check_out_time', 'total_hours')
#     list_filter = ('date', 'employee')
#     search_fields = ('employee__name', 'employee__employee_id')
#     ordering = ['-date']  # Show latest records first
from django.contrib import admin
from .models import Attendance

from django.contrib import admin
from .models import Attendance

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'total_hours')  # Display these fields in the admin list view
    search_fields = ('employee__name', 'date')  # Allow search by employee name and date
    list_filter = ('date', 'employee')  # Add filters for date and employee
    # readonly_fields = ('total_hours',)  # Make total_hours read-only
    
    def get_logs(self, obj):
        return obj.logs  # Display logs as a readable format
    get_logs.short_description = 'Logs'
    
admin.site.register(Attendance, AttendanceAdmin)

