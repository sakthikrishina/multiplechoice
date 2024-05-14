from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    
    def create_user(self, email, password , **extra_fields):
        if not email:
            raise ValueError("Email is Required")
        
        phone_number = extra_fields.pop('phone_number', None)
        email=self.normalize_email(email)
        user=self.model(email = email, **extra_fields)
        user.set_password(password)
        
        if phone_number is not None:
            user.phone_number = phone_number
            
        user.save(using=self.db)
        
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        return self.create_user(email, password , **extra_fields)
    
    def __str__(self):
        return str(self.email)