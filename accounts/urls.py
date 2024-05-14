from django.urls import path
from . import views
from django.conf import settings

urlpatterns = [
    path('', views.BASE, name='BASE'),
    path('institutionsignup/', views.Staffsignup, name='staffsignup'),
    path('signup/', views.Studentsignup, name='studentsignup'),
    path('login/', views.login_with_email, name='login_with_email'),
    path('otp-verification/', views.otp_verification, name='otp_verification'),
    path('institutionlogin/', views.instmpin_login, name='instlogin'),
    path('studentlogin/', views.studmpin_login, name='stulogin'),
    path('forgotmpin/', views.login_with_email, name='forgotmpin'),
    path('forgot-otp-verification/', views.stuotp_verification, name='stuotp_verification'),
    path('<int:pk>/dashboard/', views.instdash, name='instdash'),
    path('<int:pk>/studentdashboard/', views.studash, name='studash'),
]