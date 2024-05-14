from django.shortcuts import render, redirect
from .forms import RegisterForm
from . import models
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import cache_control


# Create your views here.

def index(request):
    return render(request, "otp/index.html")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signup(request):    
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! An OTP was sent to your Email")
            return redirect("verify-email", username=request.POST['username'])
    context = {"form": form}
    return render(request, "otp/signup.html", context)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def verify_email(request, username):
    user = get_user_model().objects.get(username=username)
    user_otp = OtpToken.objects.filter(user=user).last()
    
    
    if request.method == 'POST':
        # valid token
        if user_otp.otp_code == request.POST['otp_code']:
            
            # checking for expired token
            if user_otp.otp_expires_at > timezone.now():
                user.is_active=True
                user.save()
                messages.success(request, "Account activated successfully!! You can Login.")
                return redirect("signin")
            
            # expired token
            else:
                messages.warning(request, "The OTP has expired, get a new OTP!")
                return redirect("verify-email", username=user.username)
        
        
        # invalid otp code
        else:
            messages.warning(request, "Invalid OTP entered, enter a valid OTP!")
            return redirect("verify-email", username=user.username)
        
    context = {}
    return render(request, "otp/verify_token.html", context)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def resend_otp(request):
    if request.method == 'POST':
        user_email = request.POST["otp_email"]
        
        if get_user_model().objects.filter(email=user_email).exists():
            user = get_user_model().objects.get(email=user_email)
            otp = OtpToken.objects.create(user=user, otp_expires_at=timezone.now() + timezone.timedelta(minutes=5))
            
            
            # email variables
            subject="Email Verification"
            message = f"""
                                Hi {user.username}, here is your OTP {otp.otp_code} 
                                it expires in 5 minute, use the url below to redirect back to the website
                                http://127.0.0.1:8000/verify-email/{user.username}
                                
                                Here is your password recovery mpin code {otp.mpin} . In case your password is forgotten, no problem at all. 
                                Regaining access to your account is a breeze. 
                                Just click on the 'Forgot Password' option, enter this MPIN. Your account security is our priority, and we're here to help you every step of the way.
                                
                                """
            sender = "sakthikrish2001@gmail.com"
            receiver = [user.email, ]
        
        
            # send email
            send_mail(
                    subject,
                    message,
                    sender,
                    receiver,
                    fail_silently=False,
                )
            
            messages.success(request, "A new OTP has been sent to your email-address")
            return redirect("verify-email", username=user.username)

        else:
            messages.warning(request, "This email dosen't exist in the database")
            return redirect("resend-otp")
        
           
    context = {}
    return render(request, "otp/resend_otp.html", context)
    
   
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        
        if user is not None and user.is_superuser:            
            login(request, user)    
            return redirect('institution')
        elif user is not None and user.is_staff:
            login(request, user)
            return redirect('staff')
        elif user is not None and user is not user.is_staff and user is not user.is_superuser:
            login(request, user)
            messages.success(request, f"Hi {request.user.username}, Please wait patiently until you receive confirmation from the admin team before attempting to log in. ")
            return redirect("signin") 
        else:
            messages.warning(request, "Invalid credentials")
            return redirect("signin")
        
    return render(request, "otp/login.html")
    
def sample(request):
    return render(request, "otp/student/html/dashbase.html")

def institution(request):
    return render(request,"otp/institution.html")

def staff(request):
    return render(request,"otp/staff.html")

def BASE(request):
    return render(request, 'otp/index.html')

def dash(request):
    return render(request, 'otp/student/html/index.html')

