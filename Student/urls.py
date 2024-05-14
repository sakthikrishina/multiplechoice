from django.urls import path
from . import views

urlpatterns = [
    path('studentdashboardview/<int:pk>', views.dashboard_view, name='studdash'),
    path('exam/<int:pk>', views.examview, name='exam_view'),
    path('take-exam/<int:pk>', views.take_exam_view,name='takeexam'),
    path('<int:pk>/data', views.start_exam_view,name='start-exam'),
    path('<int:pk>/save', views.review_answers,name='review-view'),
    path('<int:course_id>/review', views.ansreviews,name='ansreview'),
    path('<int:course_id>/result', views.save_user_response,name='result'),
    path('updateprofile/', views.account, name='profile'),
    path('updatempinn/', views.mpinupdate, name='chmpin'),
    path('leaderboard/<int:pk>', views.leaderview, name='leaderview'),
    path('logout', views.logout, name='logout'),
    ]