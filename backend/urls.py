from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('studentView/', views.student_view, name="student_view"),
    path('teacherView/', views.teacher_view, name="teacher_view"),
    path('teacherForm/', views.teacher_entry, name="teacher_entry"),
    path('student_result/', views.student_result, name="student_result"),
    path('teacherForm/evaluate_result/<int:teacher_id>/', views.evaluate_result, name = "evaluate")
]


