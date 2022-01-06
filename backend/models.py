from django.db import models

# Create your models here.
class Subject(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Student(models.Model):
    enrollment_number = models.CharField(max_length=11, unique=True)
    full_name = models.CharField(max_length=30, blank=False)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name

class Teacher(models.Model):
    teacher_id = models.CharField(max_length = 10, unique=True, blank = False)
    name = models.CharField(max_length=30, blank=False)
    email = models.EmailField(blank=True)
    subject = models.OneToOneField(Subject, on_delete=models.CASCADE)
    # student = models.ForeignKey(Student, on_delete=models.CASCADE)
    # answer_key = models.FileField(upload_to='media/')

    def __str__(self):
        return self.name


