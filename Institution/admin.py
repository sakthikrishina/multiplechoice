from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin


class AnswerInline(admin.TabularInline):
    model = Answer

class QuestionAdmin(admin.ModelAdmin):
    inlines= [AnswerInline]

admin.site.register(Course)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Result)
admin.site.register(savequestion)