from django.contrib import admin
from django.contrib import admin
from .models import *
from . import models
from import_export.admin import ImportExportModelAdmin, ExportActionMixin, ImportMixin
from django.contrib.auth.models import User
from import_export import resources
from django.contrib import admin
from .models import VideoUpload

# Register your models here.
@admin.register(Post)
class POSTAdmin(admin.ModelAdmin):
    list_display=['user','project_name','company_name','location']

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display=['project','floor','floor_or_name','image']
    
@admin.register(ItemList)
class ItemListAdmin(admin.ModelAdmin):
    list_display=['project','image','total_floors','no_of_employees']
    
    
@admin.register(VideoUpload)
class VideoUploadAdmin(admin.ModelAdmin):
    list_display=['user','floor','description','file','thumbnail','upload_date','plan']

@admin.register(VideoFrame)
class VideoFrameAdmin(admin.ModelAdmin):
    list_display=['video','frame_number','image','timestamp','plan']

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display =['username','email_id','course','mobile','designation','college_name','address','resume']
    
    
@admin.register(SaveJson)
class SaveJsonAdmin(admin.ModelAdmin):
    list_display =['id','name','data']
    
    