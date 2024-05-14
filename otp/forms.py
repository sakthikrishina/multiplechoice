from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from . import models 


class RegisterForm(UserCreationForm):
    email=forms.CharField(widget=forms.EmailInput(attrs={"placeholder": "Enter email-address", "class": "form-control"}))
    first_name=forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter First Name", "class": "form-control"}))
    last_name=forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter Last Name", "class": "form-control"}))
    
    
    class Meta:
        model = get_user_model()
        fields = ["email", "first_name", "last_name"]
        
class StudentForm(forms.ModelForm):
    class Meta:
        model=models.Profile
        fields=['mobile','avatar']