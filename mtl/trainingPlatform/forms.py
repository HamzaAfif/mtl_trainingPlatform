from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


ALLOWED_EMAILS_FOR_STAFF = [
    'ha.afif25@gmail.com',
    'helalamy@microtechleaders.com',
    'zakariae.elmajdouli@gmail.com',
    'elothemanymaha@gmail.com',
    'nakkouchtarek@gmail.com',
]

ALLOWED_EMAILS_FOR_REGISTRATION = [
    'ha.afif25@gmail.com',
    'helalamy@microtechleaders.com',
    'zakariae.elmajdouli@gmail.com',
    'saadeddine.hachlaf@gmail.com',
    'ibrahim.elamraoui1507@gmail.com',
    'abdoukhalikihnouhaila4@gmail.com',
    'adilelkhaider80@gmail.com',
    'elothemanymaha@gmail.com',
    'salmahaidar869@gmail.com',
    'hajarjedouani@gmail.com',
    'nakkouchtarek@gmail.com',
]

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email not in ALLOWED_EMAILS_FOR_REGISTRATION:
            raise forms.ValidationError("This email is not allowed to register.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        
        # Assign staff status based on email
        if user.email in ALLOWED_EMAILS_FOR_STAFF:
            user.is_staff = True
        else:
            user.is_staff = False
        
        if commit:
            user.save()
        return user

