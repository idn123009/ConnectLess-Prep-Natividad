from django import forms

from quizApp.models import Quiz


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ("title",)

# class ChoiceForm(forms.ModelForm):
#     class Meta:
#         model = Choice
#         fields = ['choice_text', 'is_correct']

# QuestionFormSet = modelformset_factory(
#     Question,  # Model to use
#     form=QuestionForm,
#     extra=1,  # Start with one empty form
#     can_delete=True  # Allow deleting questions
# )
#
# ChoiceFormSet = inlineformset_factory(
#     Question,  # Parent model
#     Choice,  # Related model
#     form=ChoiceForm,
#     extra=1,  # Start with one empty choice
#     can_delete=True  # Allow deleting choices
# )
