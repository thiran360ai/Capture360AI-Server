from django.contrib import admin
from .models import *

@admin.register(Employee)
class CustomEmployeeAdmin(admin.ModelAdmin):
    list_display= ['id','username','role','mobile','location','password','attendance','total_attendance','image','is_active']

@admin.register(UserDetails)
class UserDetailsAdmin(admin.ModelAdmin):
    list_display= ['name','password','membership','subscribed','premium_amount']


@admin.register(SaloonOrder)
class SaloonOrdersAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_id', 'employee_id', 'order_type', 'category', 'services', 'payment_status', 'date', 'payment_type', 'time', 'amount', 'created_at', 'status']


@admin.register(GymOrder)
class GymOrderAdmin(admin.ModelAdmin):
    list_display= ['id', 'customer_id', 'employee_id', 'gender','age', 'timeslot', 'status', 'category', 'plan', 'amount', 'attendance', 'purchaseddate', 'expiry_date', 'created_at', 'payment_status']


# @admin.register(SpaOrder)
# class SpaOrdersAdmin(admin.ModelAdmin):
#     list_display= ['id','username','order_type','category','services','date','time','created_at']


class HotelOrdersAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_id', 'employee_id', 'guest_name', 'amount', 'check_in', 'check_out', 'category',
                    'room_count', 'guest_count', 'status', 'payment_status', 'created_at']

    def room_count(self, obj):
        return ", ".join([str(item) for item in obj.room_count.all()])  # Replace 'many_to_many_field' with actual field name

    room_count.short_description = "Related Items"  # Custom column name


admin.site.register(HotelOrder, HotelOrdersAdmin)


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display= ['id', 'employee_attendance', 'status', 'check_in', 'check_out']
    

@admin.register(Rooms)
class RoomsAdmin(admin.ModelAdmin):
    list_display= ['id', 'room', 'status']