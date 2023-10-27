from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path('add_question/', views.add_question, name='add_question'),
    path('all_questions/', views.all_questions, name='all_questions'),
    path('question_detail/<int:question_id>/', views.question_detail, name='question_detail'),
    path('answer_question/<int:question_id>/', views.answer_question, name='answer_question'),
    path('like/<int:answer_id>/', views.like_answer, name='like_answer'),
    path('logout/', views.user_logout, name='logout'),
]
