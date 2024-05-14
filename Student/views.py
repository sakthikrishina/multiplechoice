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
from django.db.models import F, FloatField, Sum, ExpressionWrapper
from django.contrib.auth import logout as logouts
from datetime import timedelta
    
def dashboard_view(request, pk):
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


def leaderview(request, pk):
    user = amodel.CustomUser.objects.get(id=pk)
    courses = imodel.Course.objects.all()
    results = imodel.Result.objects.filter(user=user).all() 

    # Calculate position, exam name, mark, and exam_percentage for each result
    course_marks = defaultdict(float)
    for result in results:
        # Aggregate marks for each course
        course = result.exam.course
        course_id = imodel.Course.objects.get(course=course).id
        course_marks[course_id] += result.marks

    # Create a dictionary to store aggregated marks for each course
    aggregated_results = []
    for course_id, total_marks in course_marks.items():
        exam_name = imodel.Course.objects.get(id=course_id).course
        exam_percentage = (total_marks / imodel.Course.objects.get(id=course_id).total_marks) * 100
        aggregated_results.append({
            'exam_name': exam_name,
            'total_marks': total_marks,
            'exam_percentage': exam_percentage
        })

    return render(request, 'otp/student/html/viewleader.html', {
        'aggregated_results': aggregated_results,
        'user': user,
        'courses': courses,
        'results': results,
    })
    
def examview(request,pk):
    user=amodel.CustomUser.objects.get(id=pk)
    courses=imodel.Course.objects.all()
    return render(request,'otp/student/html/examview.html',{'courses':courses, 'user':user})

def take_exam_view(request, pk):
    course=imodel.Course.objects.get(id=pk)
    return render(request,'otp/student/html/takeexam.html',{'course':course})

def start_exam_view(request,pk):
    course=imodel.Course.objects.get(id=pk)
    today_date = date.today()
    questions = list(imodel.Question.objects.filter(course=course).values('id', 'question', 'marks', 'option1', 'option2', 'option3', 'option4', 'answer').order_by('?'))
    shuffle(questions)
    if request.method=='POST':
        pass
    response= render(request,'otp/student/html/startexam.html',{'course':course,'questions':questions, 'today_date': today_date})
    response.set_cookie('course_id',course.id)
    return response
    
def review_answers(request, pk):
    course = imodel.Course.objects.get(id=pk)
    user = request.user
    
    if request.method == 'POST':
        submitted_answers = {}
        time_taken ={}
        today_date = date.today()
         
        for key, value in request.POST.items():
            if key.startswith('selected_option_'):
                question_id = key.replace('selected_option_', '')
                submitted_answers[question_id] = value
        
        total_questions_count = imodel.Question.objects.filter(course=course).count()
                
        if len(submitted_answers) < total_questions_count:
            messages.warning(request, 'You must answer all questions')
            return redirect('start-exam', pk=course.id) 
                
                
        exam_attempt = imodel.ExamAttempt.objects.create(user=user, course=course)        
        time_taken = request.POST.get('time_taken')   
        for question_id, selected_option in submitted_answers.items():
            
            csrf_token_value =  f"{user.name}_{today_date}"
            question = imodel.Question.objects.get(id=question_id)
            imodel.savequestion.objects.create(
                user=user,
                course=course,
                question=question,
                attempt=exam_attempt,
                selected_option=selected_option,  
                time_taken=time_taken,
                token=csrf_token_value
            )
            
        return redirect('ansreview', course_id=course.id)  
        
    else:
        
        return render(request, 'otp/student/html/startexam.html', {'course': course })
  
def ansreviews(request, course_id):
    course = imodel.Course.objects.get(id=course_id)
    latest_attempt = imodel.ExamAttempt.objects.filter(user=request.user, course=course).latest('id')
    saved_answers = imodel.savequestion.objects.filter(user=request.user,course_id=course_id, attempt=latest_attempt) 
    return render(request, 'otp/student/html/reviewanswer.html', {'course': course, 'saved_answers': saved_answers})


def save_user_response(request, course_id):
    course = imodel.Course.objects.get(id=course_id)
    latest_attempt = imodel.ExamAttempt.objects.filter(user=request.user, course=course).latest('id')
    questions = imodel.Question.objects.filter(course_id=course_id)
    saved_answers = imodel.savequestion.objects.filter(user=request.user,course_id=course_id, attempt=latest_attempt) 
    total_marks = 0
    correct_count = 0
    duration=0
    min_duration = None
    
    first_saved_answer = saved_answers.first()
    if first_saved_answer:
        duration = first_saved_answer.time_taken
    
    for question in questions:
        saved_answer = imodel.savequestion.objects.get(user=request.user, course_id=course_id, question=question, attempt=latest_attempt)
        marks = 0
        if saved_answer.selected_option == question.answer: 
            marks = question.marks
            correct_count += 1
        total_marks += marks

        if min_duration is None or saved_answer.time_taken < min_duration:
            min_duration = saved_answer.time_taken
    
    total_questions = questions.count()
    incorrect_count = total_questions - correct_count
    percentage = (total_marks / (total_questions * question.marks)) * 100
    
    # Calculate rank
    rank = imodel.Result.objects.filter(exam=course, marks__gte=total_marks, duration__lte=min_duration).count() + 1
    
    # Save the result
    imodel.Result.objects.create(
        user=request.user,
        rank=rank,
        exam=course,
        marks=total_marks,
        percentage=percentage,
        duration=duration,
    )
    
    return render(request, 'otp/student/html/result_page.html', {
        'correct_answer': question.answer,
        'marks': total_marks,
        'percentage': percentage,
        'rank': rank,
        'duration': duration,
        'correct_count': correct_count,
        'incorrect_count': incorrect_count,
        'course': course,
        'saved_answers': saved_answers
    })


def account(request):
    usr = amodel.CustomUser.objects.get(id=request.user.id)
    context = {}
    if request.method=="POST":
        name = request.POST["name"]
        user_profile = request.FILES["user_profile"]
        gender = request.POST["gender"]
        father_name = request.POST["father_name"]
        usr.name = name
        usr.user_profile=user_profile
        usr.gender = gender
        usr.father_name=father_name
        usr.save()
        messages.success(request, 'Profile changes Successfully')
        return redirect('profile') 
    return render(request,"otp/student/html/profilesetting.html",context)

def mpinupdate(request):
    usr = amodel.CustomUser.objects.get(id=request.user.id)
    context = {'mpin': usr.mpin}
    if request.method=="POST":
        mpin = request.POST["mpin"]
        cmpin = request.POST["cmpin"]
        existing_user = amodel.CustomUser.objects.filter(mpin=mpin).exclude(id=usr.id).exists()
        if existing_user:
            messages.warning(request, 'MPIN already exists. Please choose a different MPIN.')
            return redirect('chmpin')
        if mpin==cmpin:
            usr.mpin = mpin
            usr.save()
            messages.success(request, 'MPIN Updated Successfully. This MPIN is important for login.')
            return redirect('chmpin')
        else:
          messages.warning(request, 'mpin and confirm mpin must be same')
          return redirect('chmpin') 
      
    return render(request,"otp/student/html/updatempinlog.html",context)

def logout(request):
    if request.method == 'POST':
        logouts(request)
        return redirect('stulogin')