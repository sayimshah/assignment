from django import forms
from .models import Answer, Question

from django import forms

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'content']

        
class AnswerForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}))


    class Meta:
        model = Answer
        fields = ['content']
