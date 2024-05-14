from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.conf import settings
import secrets
from PIL import Image
# Create your models here.

class CustomUser(AbstractUser):   
    email = models.EmailField(unique=True)
    is_student= models.BooleanField('Student', default=False)   
        
    def __str__(self):
        return self.email
    
    
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    mobile=models.CharField(max_length=12, null='True')
    avatar = models.ImageField(default='default.jpg', upload_to='profile_pic')
    bio = models.TextField()

    def __str__(self):
        return f'{self.user.first_name} Profile' 
     
    def save(self):
        super().save()

        img = Image.open(self.image.path) # Open image

        # resize image
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size) # Resize image
            img.save(self.image.path)    

class OtpToken(models.Model):    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="otps")
    otp_code = models.CharField(max_length=6, default=secrets.token_hex(3))
    tp_created_at = models.DateTimeField(auto_now_add=True)
    otp_expires_at = models.DateTimeField(blank=True, null=True)
    
    
   
    
    def __str__(self):
        return self.user.username
