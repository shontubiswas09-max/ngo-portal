from django import forms
from .models import Donor

class DonorForm(forms.ModelForm):
    class Meta:
        model = Donor
        fields = ['name', 'organization', 'email', 'phone', 'profile_picture', 'document', 'donation_amount', 'project']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'organization': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
            'document': forms.FileInput(attrs={'class': 'form-control'}),
            'donation_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'project': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError('Donor name is required.')
        return name
    
    def clean_organization(self):
        org = self.cleaned_data.get('organization')
        if not org:
            raise forms.ValidationError('Organization name is required.')
        return org
    
    def clean_donation_amount(self):
        amount = self.cleaned_data.get('donation_amount')
        if amount is not None and amount < 0:
            raise forms.ValidationError('Donation amount must be positive.')
        return amount