from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import UserCreationForm
from .models import Question, Answer, Like
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from .forms import *
from django.shortcuts import render, redirect, get_object_or_404
from .models import Question, Answer
from .forms import AnswerForm


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("login")  # Redirect to the home page after registration
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})

def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("all_questions")  #
    return render(request, "login.html")


def add_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            return redirect('all_questions') 
    else:
        form = QuestionForm()

    return render(request, 'add_question.html', {'form': form})

def all_questions(request):
    questions = Question.objects.all().annotate(answer_count=Count('answer')).annotate(like_count=Count('answer__like'))
    return render(request, 'all_questions.html', {'questions': questions})

@login_required
def answer_question(request, question_id):
    question = Question.objects.get(pk=question_id)

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = Answer(content=form.cleaned_data['content'], question=question, author=request.user)
            answer.save()
            return redirect('question_detail', question_id=question_id)
    else:
        form = AnswerForm()

    return render(request, 'answer_form.html', {'form': form, 'question': question})



@login_required
def question_detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    answers = Answer.objects.filter(question=question)

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = Answer(content=form.cleaned_data['content'], question=question, author=request.user)
            answer.save()
            return redirect('question_detail', question_id=question_id)

    else:
        form = AnswerForm()

    return render(request, 'question_detail.html', {'question': question, 'answers': answers, 'form': form})


@login_required
def like_answer(request, answer_id):
    answer = Answer.objects.get(pk=answer_id)

    # Check if the user has already liked the answer
    existing_like = Like.objects.filter(answer=answer, user=request.user).first()
    if existing_like:
        existing_like.delete()
    else:
        new_like = Like(answer=answer, user=request.user)
        new_like.save()

    return redirect('question_detail', question_id=answer.question.id)

def user_logout(request):
    logout(request)
    return redirect('login')