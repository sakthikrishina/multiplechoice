from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from .models import *
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
import random
from django.shortcuts import render, redirect, get_object_or_404
from accounts import models as amodel
from Institution import models as imodel
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages
from random import shuffle
import random
from django.utils import timezone
from django.http import JsonResponse
from django.http import HttpResponse
from django.template import loader 
import matplotlib.pyplot as plt
import numpy as np
from django.conf import settings
import os
from django.http import FileResponse
import matplotlib
matplotlib.use('Agg')  
import io
from django.core.files.base import ContentFile
from django.db.models import Sum 
from datetime import date, datetime
from django.middleware.csrf import get_token
from collections import defaultdict

User = get_user_model()

def index(request):
    return render(request, "otp/index.html")

def BASE(request):
    return render(request, 'otp/rolebase.html')

def Staffsignup(request):
    email_exists = False
    phone_number_exists = False
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        user_profile = request.FILES.get('user_profile')
        if not validate_email(email):
            messages.warning(request, "Please enter a valid email address.")
            return redirect('staffsignup')
        if  User.objects.filter(email=email).exists():
            messages.warning(request, "Email already exists.")
            return redirect('staffsignup')
        if  User.objects.filter(phone_number=phone_number).exists():
            messages.warning(request, "Phone number already exists.")
            return redirect('staffsignup')
        if not validate_phone_number(phone_number):
            messages.warning(request, "Please enter a valid phone number.")
            return redirect('staffsignup')
        user = User.objects.create(name=name, email=email, phone_number=phone_number, user_profile=user_profile, is_staff=True)
        user.save()
        # Generate OTP
        otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        otp_instance = OTP.objects.create(user=user, otp=otp)
        # Send OTP via email
        send_mail(
            'Your OTP for Staff Registration',
            f'Hi {name}, here is your OTP: {otp}',
            'sender@example.com',
            [email],
            fail_silently=False,
        )

        # Store the email in the session
        request.session['email'] = email
        messages.success(request, 'Registered Successfully. Please check your email for OTP.')
        return redirect(reverse('otp_verification'))  # Redirect to OTP verification page
    return render(request, 'otp/staffsignup.html')

def Studentsignup(request):
    email_exists = False
    phone_number_exists = False
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        user_profile = request.FILES.get('user_profile')
        if not validate_email(email):
            messages.warning(request, "Please enter a valid email address.")
            return redirect('studentsignup')
        if  User.objects.filter(email=email).exists():
            messages.warning(request, "Email already exists.")
            return redirect('studentsignup')
        if  User.objects.filter(phone_number=phone_number).exists():
            messages.warning(request, "Phone number already exists.")
            return redirect('studentsignup')
        if not validate_phone_number(phone_number):
            messages.warning(request, "Please enter a valid phone number.")
            return redirect('studentsignup')
        user = User.objects.create(name=name, email=email, phone_number=phone_number, user_profile=user_profile, is_student=True)
        user.is_student
        user.save()
        otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        otp_instance = OTP.objects.create(user=user, otp=otp)
        # Send OTP via email
        send_mail(
            'Your OTP for Student Registration',
            f'Hi {name}, here is your OTP: {otp}',
            'sender@example.com',
            [email],
            fail_silently=False,
        )

        # Store the email in the session
        request.session['email'] = email
        messages.success(request, 'Registered Successfully. Please check your email for OTP.')
        return redirect(reverse('otp_verification'))
    return render(request, 'otp/signup.html')

import re

def validate_email(email):
    
    email_regex = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    return re.match(email_regex, email)

def validate_phone_number(phone_number):
    return phone_number.isdigit() and len(phone_number) == 10

@login_required
def login_with_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            # Generate OTP
            otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
            otp_instance = FORGOTOTP.objects.create(user=user, otp=otp)
            # Send OTP via email
            send_mail(
                'Your OTP for MCQ login',
                f'Hi, here is your OTP: {otp}',
                'sender@example.com',
                [email],
                fail_silently=False,
            )

            # Store the OTP in the session
            request.session['otp'] = otp
            request.session['email'] = email
            return redirect('stuotp_verification')
        else:
            messages.warning(request, "User with this email does not exist.")
            return redirect('login_with_email')

    return render(request, 'otp/login_with_email.html')

def stuotp_verification(request):
    if request.method == 'POST':
        otp_entered = request.POST.get('stuotp')
        email = request.session.get('email')
        user = authenticate(request, email=email)
        otp_instance = FORGOTOTP.objects.filter(user__email=email).order_by('-tp_created_at').first()  # Ordering by latest first

        print("Entered OTP:", otp_entered)
        print("Stored OTP:", otp_instance.otp if otp_instance else None)

        if otp_instance and otp_entered == otp_instance.otp:
            # OTP verified, log in the user
            user = otp_instance.user
            login(request, user)
            if user.is_staff:
                update_mpin_url = reverse('update_mpin')  # URL for updating MPIN
                success_message = 'Logged in successfully. Please <a href="{}">Update Your MPIN</a>'.format(update_mpin_url)
                messages.success(request, success_message)
                return redirect('instdash', pk=user.id)
            else:
                messages.success(request, 'Logged in successfully. Please Update Your MPIN')
                return redirect('studash', pk=user.id)
        else:
            messages.warning(request, 'Invalid OTP. Please try again.')
            return redirect('stuotp_verification')

    return render(request, 'otp/stuotp_verification.html')

def otp_verification(request):
    if request.method == 'POST':
        otp_entered = request.POST.get('otp')
        email = request.session.get('email')
        user = authenticate(request, email=email)
        otp_instance = OTP.objects.filter(user__email=email).order_by('tp_created_at').first()

        if otp_instance and otp_entered == otp_instance.otp:
            # OTP verified, log in the user
            user = otp_instance.user
            login(request, user)
            if  user.is_staff:# Add the success message with the URL
                success_message = 'Logged in successfully. Please Update Your MPIN for login purpose'
                messages.success(request, success_message)
                return redirect('instdash',pk=user.id)
            else:
                succes_message = 'Logged in successfully. Please Update Your MPIN for login purpose'
                messages.success(request, succes_message)
                return redirect('studash', pk=user.id) 
        else:
            messages.warning(request, 'Invalid OTP. Please try again.')
            return redirect('otp_verification')

    return render(request, 'otp/otp_verification.html')

def instmpin_login(request):
    if request.method == 'POST':
        mpin = request.POST.get('mpin')
        user = User.objects.filter(mpin=mpin).first()
        if user is not None and user.mpin == mpin:
            login(request, user)
            if user.is_staff:
                return redirect('instdash', pk=user.id)
            else:
                messages.warning(request, 'Invalid. Please Register.')
        else:
            messages.warning(request, 'Invalid MPIN.')
    
    return render(request, 'otp/login.html')

def studmpin_login(request):
    if request.method == 'POST':
        mpin = request.POST.get('mpin')
        user = User.objects.filter(mpin=mpin).first()
        if user is not None and user.mpin == mpin:
            login(request, user)
            if user.is_student:
                messages.success(request, 'Login Successfully')
                return redirect('studash', pk=user.id)
            else:
                messages.warning(request, 'Invalid. Please Register.')
        else:
            messages.warning(request, 'Invalid MPIN.')
    
    return render(request, 'otp/studentlogin.html')


def instdash(request, pk):
    user = amodel.CustomUser.objects.get(id=pk)
    total_student = amodel.CustomUser.objects.filter(is_student='1').all().count()
    complete_mcq=imodel.Course.objects.filter(status='completed').all().count()
    pending_mcq=imodel.Course.objects.filter(status='pending').all().count()
    executed_mcq=imodel.Course.objects.filter(status='executed').all().count()
    question_cate=imodel.Category.objects.all().count()
    context = {
        'total_student': total_student,
        'complete_mcq': complete_mcq,
        'pending_mcq': pending_mcq,
        'executed_mcq': executed_mcq,
        'question_cate': question_cate,
        'user': user,
    }
    return render(request, 'otp/institution/dashboard.html', context)

def studash(request, pk):
    complete_mcq = imodel.Course.objects.all().count()
    pending_mcq = imodel.Course.objects.filter(status='pending').count()
    user = amodel.CustomUser.objects.get(id=pk)
    courses = imodel.Course.objects.all()
    results = imodel.Result.objects.filter(user=user).all()

    plot_paths = {}
    download_links = {}

    if results.exists():
        # Initialize dictionary to store total marks for each course
        course_marks = defaultdict(float)
        
        for result in results:
            # Aggregate marks for each course
            course_marks[result.exam.course] += result.marks  

        course_names = list(course_marks.keys())
        marks = list(course_marks.values())

        fig, ax = plt.subplots(figsize=(10, 6))
        x = np.arange(len(course_names))
        width = 0.2

        ax.bar(x, marks, width)  # Plot marks for each course

        ax.set_ylabel('Total Marks')
        ax.set_title(f'Performance Matrix for {user.name}')
        ax.set_xticks(x)
        ax.set_xticklabels(course_names)
        ax.legend()

        # Get the total marks from the Course model
        total_marks = imodel.Course.objects.aggregate(total_marks=Sum('total_marks'))['total_marks']

        # Set y-axis limit to the total marks from the Course model
        ax.set_ylim(0, total_marks)

        # Save the plot to a buffer
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)

        # Save the plot image to the database
        plot = imodel.PerformancePlot.objects.create(user=user)
        plot.plot_image.save(f'{user.name}_performance_matrix.png', ContentFile(buffer.getvalue()))

        plot_paths[user.name] = plot.plot_image.url
        download_links[user.name] = plot.plot_image.url

    else:
        # If no results exist, provide default values for plot_paths and download_links
        plot_paths[user.name] = None
        download_links[user.name] = None

    return render(request, 'otp/student/html/dashboard.html', {
        'user': user,
        'complete_mcq': complete_mcq,
        'pending_mcq': pending_mcq,
        'plot_paths': plot_paths,
        'download_links': download_links,
        'results': results,
        'courses': courses,
    })