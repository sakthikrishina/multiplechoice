from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import *


user=get_user_model

class staffRegisterForm(UserCreationForm):
    email=forms.CharField(widget=forms.EmailInput(attrs={"placeholder": "Enter email-address", "class": "form-control"}))
    name=forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter  Name", "class": "form-control"}))
    
    class Meta:
        model = get_user_model()
        fields = ["email", "name", "phone_number"]
        
class studentRegisterForm(UserCreationForm):
    email=forms.CharField(widget=forms.EmailInput(attrs={"placeholder": "Enter email-address", "class": "form-control"}))
    name=forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter  Name", "class": "form-control"}))
    
    class Meta:
        model = get_user_model()
        fields = ["email", "name", "phone_number"]