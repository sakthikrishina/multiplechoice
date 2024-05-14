from django.urls import path
from . import views

urlpatterns = [
    
    path('institutiondashboard/', views.dashboard_view, name='dash'),
    path('mcqmanagement/', views.mcq_view, name='mcq_view'),
    path('addexam/', views.create_course, name='create_course'),
    path('addquestion/', views.create_question, name='create_question'),
    path('editexam/<int:id>/', views.UpdateCourse, name='editexam'),
    path('deleteexam/<int:id>/', views.deletecourse, name='deleteexam'),
    path('editquestion/<int:id>/', views.UpdateQuestion, name='editquestion'),
    path('deletequestion/<int:id>/', views.deletequestion, name='deletequestion'),
    path('questionbankmanagement/', views.question_view, name='question_view'),
    path('addcategory/', views.create_category, name='create_category'),
    path('addquestionbank/', views.create_questionbank, name='create_questionbank'),
    path('editcategory/<int:id>/', views.UpdateCategory, name='editcategory'),
    path('deletecategory/<int:id>/', views.deletecategory, name='deletecategory'),
    path('editquestionbank/<int:id>/', views.UpdateQuestionbank, name='editquestionbank'),
    path('deletequestionbank/<int:id>/', views.deletequestionbank, name='deletequestionbank'),
    path('profile/', views.account, name='instprofile'),
    path('updatempin/', views.update_mpin, name='update_mpin'),
    path('', views.logout, name='logout'),
    
]
