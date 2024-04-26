from django.contrib import admin
from django.contrib import admin
from .models import *
from . import models
from import_export.admin import ImportExportModelAdmin, ExportActionMixin, ImportMixin
from django.contrib.auth.models import User
from import_export import resources
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