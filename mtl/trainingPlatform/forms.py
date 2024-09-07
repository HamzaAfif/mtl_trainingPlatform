from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Predefined lists of allowed email addresses
ALLOWED_EMAILS_FOR_STAFF = ['staff@example.com', 'admin@example.com']
ALLOWED_EMAILS_FOR_REGISTRATION = ['ha.afif@gmail.com', 'allowed2@example.com', 'allowed3@example.com']

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
