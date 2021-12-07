from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('studentView/', views.student_view, name="student_view"),
    path('teacherView/', views.teacher_view, name="teacher_view"),
    path('teacherForm/', views.evaluation, name="evaluation"),
    path('student_result/', views.student_result, name="student_result"),
]


