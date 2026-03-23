from django import forms
from .models import Appointment


class AppointmentForm(forms.ModelForm):
    preferred_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-input'})
    )
    preferred_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-input'})
    )

    class Meta:
        model = Appointment
        fields = ['name', 'age', 'email', 'phone', 'problem', 'preferred_date', 'preferred_time']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Full Name'}),
            'age': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Age', 'min': 1, 'max': 120}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email Address'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone Number'}),
            'problem': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Describe your problem or symptoms...', 'rows': 4}),
        }
