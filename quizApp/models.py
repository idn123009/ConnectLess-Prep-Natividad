from django.db import models
from django.utils import timezone


# Create your models here.
class Quiz(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return (f'ID:{self.id}|'
                f'Title:{self.title}')


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    def __str__(self):
        return (f'ID:{self.id}|'
                f'Question:{self.question_text}')


class Choice(models.Model):
    choice_text = models.CharField(max_length=200)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return (f'ID:{self.id}|'
                f'Question:<{self.question_id}>:{self.question.question_text}|'
                f'Choice: {self.choice_text}|'
                f'Correct:{self.is_correct}')


class Score(models.Model):
    date = models.DateField(default=timezone.now)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)


class Attempt(models.Model):
    date = models.DateField(default=timezone.now)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    num_items = models.IntegerField(default=0)
    is_ongoing = models.BooleanField(default=False)
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return (f'ID:{self.id}|'
                f'Quiz:<{self.quiz_id}>{self.quiz.title}|'
                f'Score:{self.num_items}/{self.points}|'
                f'Ongoing:{self.is_ongoing}')


class AttemptItem(models.Model):
    attempt = models.ForeignKey(Attempt, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return (f'ID:{self.id}|'
                f'Question<{self.question_id}>:{self.question.question_text}|'
                f'Choice<{self.choice_id}>:{self.choice.choice_text}|'
                f'Correct: {self.choice.is_correct}')
