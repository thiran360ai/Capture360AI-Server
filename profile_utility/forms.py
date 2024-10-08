from django import forms
from .models import VideoUpload

class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = VideoUpload
        fields = ['description', 'file', 'thumbnail']


from django import forms
from .models import Plan, Marker

from django import forms
from .models import Plan

class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ['project', 'floor', 'floor_or_name', 'image']


class MarkerForm(forms.ModelForm):
    class Meta:
        model = Marker
        
        fields = ['x', 'y','distance']
