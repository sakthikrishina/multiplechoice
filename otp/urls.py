from django.urls import path
from . import views 
from django.contrib.auth.views import LoginView
urlpatterns = [
    path('', views.BASE, name='BASE'),
    path("", views.index, name="index"),
    path("register", views.signup, name="register"),
    path("verify-email/<slug:username>", views.verify_email, name="verify-email"),
    path("resend-otp", views.resend_otp, name="resend-otp"),
    path("signin", views.signin, name="signin"),
    path("sample", views.sample, name="sample"),
    path("institution", views.institution, name="institution"),
    path("staff", views.staff, name="staff"),
    path("dashboard", views.dash, name="dash"),
    
]

