from django.shortcuts import render, redirect, get_object_or_404
from accounts import models as amodel
from django.contrib.auth import get_user_model
from Institution.models import Course, Question, Category, Questionbank
from .forms import CourseForm, QuestionForm, QuestioncategoryForm, QuestionbankForm
from django.contrib import messages



def dashboard_view(request):
    total_student = amodel.CustomUser.objects.filter(is_student='1').all().count()
    complete_mcq=Course.objects.filter(status='completed').all().count()
    pending_mcq=Course.objects.filter(status='pending').all().count()
    executed_mcq=Course.objects.filter(status='executed').all().count()
    question_cate=Category.objects.all().count()
    context = {
        'total_student': total_student,
        'complete_mcq': complete_mcq,
        'pending_mcq': pending_mcq,
        'executed_mcq': executed_mcq,
        'question_cate': question_cate,
        
    }
    return render(request, 'otp/institution/dashboard.html', context)

def mcq_view(request):
    return render(request, "otp/institution/viewquestion.html")

def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Exam added Successfully')
            return redirect('mcq_view')
    else:
        form = CourseForm()
    return render(request, 'otp/institution/mcqform.html', {'form': form})

def create_question(request):
    questionForm=QuestionForm()
    if request.method=='POST':
        questionForm=QuestionForm(request.POST)
        if questionForm.is_valid():
            question=questionForm.save(commit=False)
            course=Course.objects.get(id=request.POST.get('course'))
            question.course=course
            question.save()
            messages.success(request, 'Question added Successfully')
            return redirect('mcq_view')       
        else:
         questionForm= QuestionForm()
    return render(request, 'otp/institution/questionform.html', {'questionForm':questionForm})


def mcq_view(request):
    
    context={
        
        'all_courses': Course.objects.all(),
        'all_question': Question.objects.all()
    }
    
    return render(request,"otp/institution/viewquestion.html", context)

def UpdateCourse(request, id):
    selected_course= Course.objects.get(id=id)
    form=CourseForm(instance=selected_course)
    
    if request.method == 'POST':
        form=CourseForm(request.POST, instance=selected_course)
        if form.is_valid():
            form.save()
            return redirect('mcq_view')
    
    context={'form':form}
    
    return render(request, 'otp/institution/mcqform.html', context)

def deletecourse(request, id):
    cour=Course.objects.get(id=id)
    cour.delete()
    return redirect('mcq_view')

def UpdateQuestion(request, id):
    selected_course= Question.objects.get(id=id)
    questionForm=QuestionForm(instance=selected_course)
    
    if request.method == 'POST':
        questionForm=QuestionForm(request.POST, instance=selected_course)
        if questionForm.is_valid():
            questionForm.save()
            return redirect('mcq_view')
    
    context={'questionForm':questionForm}
    
    return render(request, 'otp/institution/questionform.html', context)

def deletequestion(request, id):
    cour=Question.objects.get(id=id)
    cour.delete()
    return redirect('mcq_view')

def question_view(request):
    
    context={
        
        'all_bank': Category.objects.all(),
        'all_question': Questionbank.objects.all()
    }
    
    return render(request,"otp/institution/viewquesbank.html", context)

def create_category(request):
    if request.method == 'POST':
        form = QuestioncategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Exam added Successfully')
            return redirect('question_view')
    else:
        form = QuestioncategoryForm()
    return render(request, 'otp/institution/bankcatform.html', {'form': form})

def create_questionbank(request):
    questionForm=QuestionbankForm()
    if request.method=='POST':
        questionForm=QuestionbankForm(request.POST)
        if questionForm.is_valid():
            question=questionForm.save(commit=False)
            category=Category.objects.get(id=request.POST.get('category'))
            question.category=category
            question.save()
            messages.success(request, 'Question added Successfully')
            return redirect('question_view')       
        else:
         questionForm= QuestionbankForm()
    return render(request, 'otp/institution/questionbankform.html', {'questionForm':questionForm})
    

def UpdateCategory(request, id):
    selected_course= Category.objects.get(id=id)
    form=QuestioncategoryForm(instance=selected_course)
    
    if request.method == 'POST':
        form=QuestioncategoryForm(request.POST, instance=selected_course)
        if form.is_valid():
            form.save()
            return redirect('question_view')
    
    context={'form':form}
    
    return render(request, 'otp/institution/bankcatform.html', context)

def deletecategory(request, id):
    cour=Category.objects.get(id=id)
    cour.delete()
    return redirect('question_view')

def UpdateQuestionbank(request, id):
    selected_course= Questionbank.objects.get(id=id)
    questionForm=QuestionbankForm(instance=selected_course)
    
    if request.method == 'POST':
        questionForm=QuestionbankForm(request.POST, instance=selected_course)
        if questionForm.is_valid():
            questionForm.save()
            return redirect('question_view')
    
    context={'questionForm':questionForm}
    
    return render(request, 'otp/institution/questionbankform.html', context)

def deletequestionbank(request, id):
    cour=Questionbank.objects.get(id=id)
    cour.delete()
    return redirect('question_view')

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
        return redirect('instprofile') 
    return render(request,"otp/institution/profilesetting.html",context)

def update_mpin(request):
    usr = amodel.CustomUser.objects.get(id=request.user.id)
    context = {'mpin': usr.mpin}
    if request.method=="POST":
        mpin = request.POST["mpin"]
        cmpin = request.POST["cmpin"]
        existing_user = amodel.CustomUser.objects.filter(mpin=mpin).exclude(id=usr.id).exists()
        if existing_user:
            messages.warning(request, 'MPIN already exists. Please choose a different MPIN.')
            return redirect('update_mpin')
        if mpin==cmpin:
            usr.mpin = mpin
            usr.save()
            messages.success(request, 'MPIN Updated Successfully. This MPIN is important for login.')
            return redirect('update_mpin')
        else:
          messages.warning(request, 'mpin and confirm mpin must be same')
          return redirect('update_mpin') 
    return render(request,"otp/institution/updatempin.html",context)

def logout(request):
    return render(request, 'otp/rolebase.html')