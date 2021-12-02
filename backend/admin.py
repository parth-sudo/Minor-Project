from django.contrib import admin
from .models import Student, Subject, Teacher

# Register your models here.
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Teacher)