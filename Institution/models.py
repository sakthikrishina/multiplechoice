from django.db import models
from accounts.models import CustomUser
import random
from django.conf import settings

class Course(models.Model):
   STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('executed', 'Executed'),
        ('pending', 'Pending'),
   ]
   
   course = models.CharField(max_length=50)
   total_question = models.PositiveIntegerField()
   total_marks = models.PositiveIntegerField()
   examdate=models.DateTimeField(null=True)
   duration=models.IntegerField(help_text="duration of the exam in minutes", null=True)
   status = models.CharField(max_length=50, null=True, choices=STATUS_CHOICES)
   
   def __str__(self):
        return self.course
    
   def get_questions(self):
        questions=list(self.question_set.all())
        random.shuffle(questions)
        return questions[:self.total_question]

class Question(models.Model):    
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    marks=models.PositiveIntegerField()
    question=models.CharField(max_length=600)
    option1=models.CharField(max_length=200)
    option2=models.CharField(max_length=200)
    option3=models.CharField(max_length=200)
    option4=models.CharField(max_length=200)
    duration=models.IntegerField(help_text="duration of the exam in minutes", null=True)
    answer=models.CharField(max_length=200)
    
    
    def  __str__(self):
        return str(self.question)
    
    def get_answers(self):
        return self.answers.all()
    
    
class Answer(models.Model):
    question= models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text=models.CharField(max_length=200)
    correct=models.BooleanField(default=False)
    created= models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f"question: {self.question.question}, answer: {self.text}, correct: {self.correct}"
    
    
class Category(models.Model):
   STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('executed', 'Executed'),
        ('pending', 'Pending'),
   ]
   
   category = models.CharField(max_length=50)
   total_question = models.PositiveIntegerField()
   date=models.DateTimeField(null=True)
   status = models.CharField(max_length=50, null=True, choices=STATUS_CHOICES)
   
   def __str__(self):
        return self.category

class Questionbank(models.Model):    
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    question=models.CharField(max_length=600)
    option1=models.CharField(max_length=200)
    option2=models.CharField(max_length=200)
    option3=models.CharField(max_length=200)
    option4=models.CharField(max_length=200)
    cat=(('Option1','Option1'),('Option2','Option2'),('Option3','Option3'),('Option4','Option4'))
    answer=models.CharField(max_length=200,choices=cat)
    explanation=models.CharField(max_length=800, null=True)
    
class ExamAttempt(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class savequestion(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    attempt = models.ForeignKey(ExamAttempt, on_delete=models.CASCADE, null=True)
    selected_option = models.CharField(max_length=200)
    token = models.CharField(max_length=200, null=True)
    time_taken = models.CharField(max_length=200,null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.course.course} - {self.question.question}"



class Result(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    rank=models.IntegerField(null=True)
    exam = models.ForeignKey(Course,on_delete=models.CASCADE, null=True)
    marks = models.PositiveIntegerField()
    percentage=models.PositiveIntegerField(null=True)
    duration=models.CharField(max_length=200, null=True)
    date = models.DateTimeField(auto_now=True)
  
    def __str__(self):
        return f"{self.user.name} - {self.exam.course}"
    
    
class PerformancePlot(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    plot_image = models.ImageField(upload_to='performance_plots')