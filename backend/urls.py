from django.urls import path
from . import views
from .views import TeacherCreateView

urlpatterns = [
    path('', views.home, name="home"),
    path('studentView/', views.student_view, name="student_view"),
    path('teacherView/', views.teacher_view, name="teacher_view"),
    path('teacherForm/', TeacherCreateView.as_view(), name="teacher_form"),
    path('student_result/', views.student_result, name="student_result"),
]
