# forms.py
from django import forms
from .models import Plan


class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ['project', 'floor', 'floor_or_name', 'image']