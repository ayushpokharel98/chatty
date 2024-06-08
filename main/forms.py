from django import forms
from django.contrib.auth.models import User
from .models import Profile
import re
class Login(forms.Form):
    username = forms.CharField(max_length=10)
    password = forms.CharField(widget=forms.PasswordInput())

def validate_username(username):
    if User.objects.filter(username = username).exists():
        raise forms.ValidationError('Username already exists.')
def validate_email(email):
    if User.objects.filter(email = email).exists():
        raise forms.ValidationError('Email already exists.')


def validate_password(password):
    if not re.search(r'[A-Z]', password):
        raise forms.ValidationError('Password must contain at least one uppercase letter.')
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise forms.ValidationError('Password must contain at least one special character.')
    if not re.search(r'\d', password):
        raise forms.ValidationError('Password must contain at least one digit.')

class SignUp(forms.Form):
    username = forms.CharField(
        max_length=10, 
        error_messages={'max_length': 'Username cannot exceed 10 characters.'},
        validators=[validate_username]
    )
    email = forms.EmailField(validators=[validate_email])
    password = forms.CharField(
        widget=forms.PasswordInput(),
        min_length=8,
        validators=[validate_password],
        error_messages={
            'min_length': 'Password must be at least 8 characters long.',
        }
    )
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['fn', 'bio', 'location', 'birth_date', 'gender', 'avatar']