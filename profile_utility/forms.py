from django import forms
from .models import VideoUpload, Plan, Marker

class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = VideoUpload
        fields = ['description', 'file', 'thumbnail']


class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ['project', 'floor', 'floor_or_name', 'image']


class MarkerForm(forms.ModelForm):
    class Meta:
        model = Marker
        fields = ['x', 'y', 'distance']
