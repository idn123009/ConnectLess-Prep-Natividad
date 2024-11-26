from django.contrib import admin

from quizApp.models import Quiz, Question, Choice

# Register your models here.
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Choice)