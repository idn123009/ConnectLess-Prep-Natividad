from django.urls import path

from . import views

urlpatterns = [
    # Login
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),

    # Home
    path('', views.index, name='index'),

    # Add Quiz
    path('quiz/add', views.add_quiz, name='add_quiz'),

    # Edit Quiz
    path('quiz/<int:quiz_id>/edit', views.edit_quiz, name='edit_quiz'),

    # Edit question choices
    path('question/<int:question_id>/choices', views.edit_choices, name='question_choices'),

    # Get quiz info and scores
    path('quiz/<int:quiz_id>', views.quiz, name='quiz'),

    # Start quiz
    path('quiz/<int:quiz_id>/start', views.quiz_start, name='quiz_start'),

    # End quiz
    path('quiz/<int:quiz_id>/finish', views.quiz_finish, name='quiz_finish'),

    # Attempt quiz
    path('quiz/<int:quiz_id>/attempt', views.start_attempt_quiz, name='attempt'),

    path('attempt_item/<int:attempt_item_id>', views.attempt_quiz_item, name='attempt_quiz_item'),

    # path('attempt/<int:attempt_id>', views.attempt, name='attempt'),
]
