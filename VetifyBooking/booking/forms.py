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

from django import forms
from .models import Appointment, Pet


class AppointmentForm(forms.ModelForm):

    class Meta:
        model = Appointment
        fields = ['pet', 'service', 'date', 'time', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # 🔥 SOLO mostrar mascotas del usuario logueado
        if user:
            self.fields['pet'].queryset = Pet.objects.filter(owner=user)