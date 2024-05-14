from django import forms
from .models import Course, Question, Category, Questionbank
from . import models

class CourseForm(forms.ModelForm):
    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('executed', 'Executed'),
        ('pending', 'Pending'),
    ]
    status = forms.ChoiceField(choices=STATUS_CHOICES)
    examdate = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    class Meta:
        model = Course
        fields = ['course','total_question','total_marks','examdate','duration', 'status']
        widgets = {
           
        }
class QuestionForm(forms.ModelForm):
    course=forms.ModelChoiceField(queryset=models.Course.objects.all(),empty_label="Exam Name", to_field_name="id")
    class Meta:
        model = Question
        fields = ['course','duration','marks', 'question', 'option1', 'option2', 'option3', 'option4', 'answer']
        widgets = {
            'question': forms.Textarea(attrs={'rows': 3, 'cols': 50})
            
        }

class QuestioncategoryForm(forms.ModelForm):
    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('executed', 'Executed'),
        ('pending', 'Pending'),
    ]
    status = forms.ChoiceField(choices=STATUS_CHOICES)
    date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    class Meta:
        model = Category
        fields = ['category','total_question','date', 'status']
        widgets = {
           
        }
class QuestionbankForm(forms.ModelForm):
    category=forms.ModelChoiceField(queryset=models.Category.objects.all(), empty_label="Category Name", to_field_name="id")
    class Meta:
        model = Questionbank
        fields = ['category', 'question', 'option1', 'option2', 'option3', 'option4', 'answer', 'explanation']
        widgets = {
            'question': forms.Textarea(attrs={'rows': 3, 'cols': 50}),
            'explanation': forms.Textarea(attrs={'rows': 5, 'cols': 50})
            
        }
        
        