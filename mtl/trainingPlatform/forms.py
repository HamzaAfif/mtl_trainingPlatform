from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


ALLOWED_EMAILS_FOR_STAFF = [
    'hafif@microtechleaders.com',
    'helalamy@microtechleaders.com',
    'zelmajdouli@microtechleaders.com',
    'melothemany@microtechleaders.com',
    'tnakkouch@microtechleaders.com',
    'shachlaf@microtechleaders.com',
    'ielamraoui@microtechleaders.com',
]

ALLOWED_EMAILS_FOR_REGISTRATION = [
    'hafif@microtechleaders.com',
    'helalamy@microtechleaders.com',
    'zelmajdouli@microtechleaders.com',
    'shachlaf@microtechleaders.com',
    'ielamraoui@microtechleaders.com',
    'abdoukhalikihnouhaila4@gmail.com',
    'adilelkhaider80@gmail.com',
    'melothemany@microtechleaders.com',
    'salmahaidar869@gmail.com',
    'hajarjedouani@gmail.com',
    'tnakkouch@microtechleaders.com',
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

