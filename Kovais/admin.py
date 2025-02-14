from django.contrib import admin
from.models import *

@admin.register(Employee)
class CustomEmployeeAdmin(admin.ModelAdmin):
    list_display= ['id','username','role','mobile','location','password','attendance','total_attendance','image','is_active']

@admin.register(UserDetails)
class UserDetailsAdmin(admin.ModelAdmin):
    list_display= ['name','password','membership','subscribed','premium_amount']


@admin.register(SaloonOrder)
class SaloonOrdersAdmin(admin.ModelAdmin):
    list_display= ['id','username','order_type','category','services','payment_status','date','payment_type','time','amount','created_at']


@admin.register(GymOrder)
class GymOrderAdmin(admin.ModelAdmin):
    list_display= ['id','customer_id','gender','timeslot','status','category','plan','amount','attendance','purchaseddate','expiry_date','created_at']


@admin.register(SpaOrder)
class SpaOrdersAdmin(admin.ModelAdmin):
    list_display= ['id','username','order_type','category','services','date','time','created_at']


@admin.register(HotelOrder)
class HotelOrdersAdmin(admin.ModelAdmin):
    list_display=['id','username','price','category','check_in','check_out','room_count','guest','created_at']
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display= ['id','employee_attendance','status','check_in','check_out']