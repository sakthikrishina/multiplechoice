from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

admin.site.register(CustomUser)
# Register your models here.

admin.site.register(OTP)