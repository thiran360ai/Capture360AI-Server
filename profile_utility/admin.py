from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Post, Plan, ItemList, VideoUpload, VideoFrame, Customer, SaveJson

# Register your models here.
@admin.register(Post)
class PostAdmin(ImportExportModelAdmin):
    list_display = ['user', 'project_name', 'company_name', 'location']


@admin.register(Plan)
class PlanAdmin(ImportExportModelAdmin):
    list_display = ['project', 'floor', 'floor_or_name', 'image']


@admin.register(ItemList)
class ItemListAdmin(ImportExportModelAdmin):
    list_display = ['project', 'image', 'total_floors', 'no_of_employees']


@admin.register(VideoUpload)
class VideoUploadAdmin(ImportExportModelAdmin):
    list_display = ['user', 'floor', 'description', 'file', 'thumbnail', 'upload_date', 'plan','json']


@admin.register(VideoFrame)
class VideoFrameAdmin(ImportExportModelAdmin):
    list_display = ['video', 'frame_number', 'image', 'timestamp', 'plan','json']


@admin.register(Customer)
class CustomerAdmin(ImportExportModelAdmin):
    list_display = ['username', 'email_id', 'course', 'mobile', 'designation', 'college_name', 'address', 'resume']


@admin.register(SaveJson)
class SaveJsonAdmin(ImportExportModelAdmin):
    list_display = ['id','project', 'name', 'data','plan']
