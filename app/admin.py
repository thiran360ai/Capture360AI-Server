from django.contrib import admin
from .models import Property, Banner, LandListing



class LandListingAdmin(admin.ModelAdmin):
    list_display = ("title", "district", "price")
    list_filter = ("district",)
    search_fields = ("title", "description")
    # inlines = [LandImageInline]  # Display images inside land listings

admin.site.register(Property)
admin.site.register(Banner)
admin.site.register(LandListing, LandListingAdmin)
