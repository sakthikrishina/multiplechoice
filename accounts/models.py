from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
from django.conf import settings
import secrets


class CustomUser(AbstractUser):
    
    ROLES = [
        ('institution', 'Institution'),
        ('student', 'Student'),
    ]
    
    username= None
    name= models.CharField(max_length=100, null=True)
    email= models.CharField(max_length=100, unique=True)
    phone_number=models.CharField(max_length=100)
    mpin=models.CharField(max_length=12, null=True)
    user_profile=models.ImageField(upload_to = 'user_profile', max_length=100,null=True,blank=False)
    is_student=models.BooleanField(null=True)
    gender= models.CharField(max_length=100, null=True)
    father_name= models.CharField(max_length=100, null=True)
    
    objects=UserManager()
    
    USERNAME_FIELD= 'email'
    REQUIRED_FIELDS=[]
    
    class Meta:
        verbose_name = "CustomUser"
        verbose_name_plural='CustomUsers'
    
    
    
    
class OTP(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="otps")
    otp = models.CharField(max_length=6)
    tp_created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OTP for {self.user.email}: {self.otp}"
    
    
    
class FORGOTOTP(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="otpss")
    otp = models.CharField(max_length=6)
    tp_created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OTP for {self.user.email}: {self.otp}"