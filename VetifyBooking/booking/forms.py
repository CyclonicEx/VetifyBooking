from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Appointment

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add CSS classes to form fields
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({
                'class': 'form-input'
            })

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['pet_name', 'pet_type', 'owner_name', 'email', 'phone', 
                  'service', 'date', 'time', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-input'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-input'}),
            'pet_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g., Max'}),
            'owner_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your name'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'you@example.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '(555) 123-4567'}),
            'pet_type': forms.RadioSelect(attrs={'class': 'radio-input'}),
            'service': forms.Select(attrs={'class': 'form-input'}),
        }