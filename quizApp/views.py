from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.forms.models import inlineformset_factory, modelformset_factory
from django.shortcuts import render, redirect

from quizApp.models import Quiz, Question, Choice, Attempt, AttemptItem


@login_required(login_url="login")
def index(request):
    quizzes = Quiz.objects.all()
    context = {'quiz': quizzes}
    return render(request, 'quizApp/index.html', context)


@login_required(login_url="login")
def add_quiz(request):
    quiz_formset = modelformset_factory(Quiz, fields=('title',), extra=1, can_delete=True, can_delete_extra=False)
    formset = quiz_formset(queryset=Quiz.objects.all())
    if request.method == "POST":
        formset = quiz_formset(data=request.POST, queryset=Quiz.objects.all())
        if formset.is_valid():
            formset.save()
            return redirect("add_quiz")

    context = {'quiz_formset': formset}
    return render(request, "quizApp/quiz_add.html", context)


@login_required(login_url="login")
def edit_quiz(request, quiz_id):
    quiz_item = Quiz.objects.get(id=quiz_id)
    question_formset = inlineformset_factory(Quiz, Question, fields=('question_text',), can_delete_extra=False, extra=1)

    if request.method == "POST":
        quiz_title = request.POST.get('title')
        quiz_item.title = quiz_title
        formset = question_formset(data=request.POST, instance=quiz_item)
        if formset.is_valid():
            formset.save()

    formset = question_formset(instance=quiz_item)
    context = {'quiz_title': quiz_item.title,
               'question_formset': formset, }

    return render(request, 'quizApp/quiz_edit.html', context)


@login_required(login_url="login")
def edit_choices(request, question_id):
    question_item = Question.objects.get(id=question_id)
    choices_formset = inlineformset_factory(Question, Choice, fields=('choice_text', 'is_correct',),
                                            can_delete_extra=False, extra=1)
    if request.method == "POST":
        formset = choices_formset(data=request.POST, instance=question_item)
        if formset.is_valid():
            formset.save()
    formset = choices_formset(instance=question_item)
    context = {'choice_formset': formset, 'question_text': question_item.question_text,
               'quiz_id': question_item.quiz_id}
    return render(request, 'quizApp/question_choice.html', context)


@login_required(login_url="login")
def quiz(request, quiz_id):
    quiz_item = Quiz.objects.get(id=quiz_id)
    context = {'quiz': quiz_item,
               'attempts': quiz_item.attempt_set.all()
               }
    return render(request, 'quizApp/quiz.html', context)


@login_required(login_url="login")
def quiz_start(request, quiz_id):
    questions = Question.objects.filter(quiz_id=quiz_id).order_by("?")
    context = {'questions': questions, 'quiz_title': questions[0].quiz.title, 'quiz_id': quiz_id}

    if request.method == "POST":
        data = request.POST
        correct_choices = []
        wrong_choices = []
        for item in data:
            if item == 'csrfmiddlewaretoken':
                continue
            chosen_choice = Choice.objects.get(id=data[item])
            if chosen_choice.is_correct:
                correct_choices.append(chosen_choice)
            else:
                wrong_choices.append(chosen_choice)
        context = {'correct_choices': correct_choices, 'wrong_choices': wrong_choices, 'score': len(correct_choices),
                   'total': questions.count(), 'quiz_id': quiz_id}
        return render(request, 'quizApp/quiz_finish.html', context)

    return render(request, 'quizApp/quiz_start.html', context)


@login_required(login_url="login")
def quiz_finish(request):
    return None


@login_required(login_url="login")
def start_attempt_quiz(request, quiz_id):
    attempt = Attempt.objects.create(quiz_id=quiz_id, is_ongoing=True, is_finished=False)
    questions = Question.objects.filter(quiz_id=quiz_id)
    for question in questions:
        attempt_item = AttemptItem(attempt=attempt, question=question)
        attempt_item.save()

    first_attempt_item = AttemptItem.objects.filter(attempt=attempt)[0]

    # context = {'attempt_item': first_attempt_item}
    return redirect("attempt_quiz_item", attempt_item_id=first_attempt_item.pk)


@login_required(login_url="login")
def attempt_quiz_item(request, attempt_item_id):
    attempt_item = AttemptItem.objects.get(id=attempt_item_id)
    context = {'attempt_quiz_item': attempt_item, }
    return render(request, 'quizApp/quiz_attempt_item.html', context)


@login_required(login_url="login")
def finish_attempt(request, attempt_id):
    attempt = Attempt.objects.get(id=attempt_id)


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'quizApp/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new user
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')  # Redirect to login page
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()

    return render(request, 'quizApp/register.html', {'form': form})
