from django import forms
from .models import Beneficiary

class BeneficiaryForm(forms.ModelForm):
    class Meta:
        model = Beneficiary
        fields = ['name', 'village', 'project', 'livelihood_activity', 'literacy_level', 'skills', 'training_history', 'attendance', 'courses_completed']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'village': forms.TextInput(attrs={'class': 'form-control'}),
            'project': forms.Select(attrs={'class': 'form-control'}),
            'livelihood_activity': forms.TextInput(attrs={'class': 'form-control'}),
            'literacy_level': forms.Select(attrs={'class': 'form-control'}),
            'skills': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'training_history': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'attendance': forms.NumberInput(attrs={'class': 'form-control'}),
            'courses_completed': forms.NumberInput(attrs={'class': 'form-control'}),
        }