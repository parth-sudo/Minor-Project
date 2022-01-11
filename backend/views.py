from django.http.response import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic
from .models import Teacher, Student, Subject, Marks
from .forms import StudentForm, TeacherForm
import io
import PyPDF2
import easyocr
import cv2
from matplotlib import pyplot as plt
import numpy as np
from django.core.files.storage import FileSystemStorage

# Create your views here.
def home(request):
    return render(request, 'backend/home.html', {})

def student_view(request):
    context = {}
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        context['form'] = form
        if form.is_valid():
            enrollment_number = form.cleaned_data.get('enrollment_number')
            full_name = form.cleaned_data.get('full_name')
            subject = form.cleaned_data.get('subject')
            answer_sheet = form.cleaned_data.get('answer_sheet')

            lenn = len(enrollment_number)
            if(lenn < 11):
                return HttpResponse("Invalid enrollment_number, try again")
            form.save() 

            return redirect("student_result")
    else:
        form = StudentForm()
        context['form'] = form
        
    return render(request, 'backend/student.html', context)
        

def teacher_view(request):
    context = {}
    if request.method == 'POST':
        form = TeacherForm(request.POST or None)
        context['form'] = form
        if form.is_valid():
            teacher_id = form.cleaned_data['teacher_id']
            name = form.cleaned_data['name']
            subject = form.cleaned_data['subject']

            # for num in teacher_id:
            #     if num not in range(0, 10):
            #         return HttpResponseBadRequest("Invalid teacher id, try again.") 
            # if len(teacher_id) < 5:
            #     return HttpResponseBadRequest("Invalid teacher id, try again.")
            
            form.save()
            return redirect("teacher_entry")
    else:
        form = TeacherForm()
        context['form'] = form

    return render(request, 'backend/teacher.html', context)

# todo 
def student_result(request):
    if request.method == 'POST':
        # answer_sheet = request.FILES['answer_sheet']
        roll = request.POST['roll_number']
        enroll = Student.objects.all().filter(enrollment_number = roll)
        if not enroll.exists():
            return HttpResponse("No student with that roll number found.")
        
        # todo
        student = Student.objects.get(enrollment_number = roll)
        queryset = Marks.objects.filter(student_roll_number = roll)

        context = {}
        context['queryset'] = queryset
        print(queryset)
        context['student'] = student

        return render(request, 'backend/student_notice.html', context)
        
    return render(request, 'backend/student_result.html', {})


def teacher_entry(request):
    if request.method == 'POST':
        id = request.POST['teacherID']
        teacher = Teacher.objects.filter(teacher_id = id)
        # print(type(teacher_id))

        if not teacher.exists():
            return HttpResponse("No Teacher with that teacher ID found.")
        
        return redirect(f"evaluate_result/{id}")

    return render(request, 'backend/teacher_entry.html', {})

#utility function.
def converter(key):
    IMAGE_PATH = f"media/{key}"

    reader = easyocr.Reader(['en'])
    result = reader.readtext(IMAGE_PATH)
    #print(result)
    res=[lis[1] for lis in result]
    return res

#utility function.
def percentage_calculator(raw_teacher_string, raw_student_string):

    teacher_word_list = [sub.split() for sub in raw_teacher_string]
    student_word_list = [sub.split() for sub in raw_student_string]

    print(teacher_word_list)

    unwanted = ['the', 'is', 'was', '.', ',', ':', 'for']

    teacher_dict = {}
    student_dict = {}

    for lis in teacher_word_list:
        for word in lis:
            if word not in unwanted: 
                if (word in teacher_dict):
                    teacher_dict[word] += 1
                else:
                    teacher_dict[word] = 1

    for lis in student_word_list:
        for word in lis:
            if word not in unwanted:
                if (word in student_dict):
                    student_dict[word] += 1
                else:
                    student_dict[word] = 1
    
    tsize = len(teacher_dict)
    ssize = 0

    for word, tfreq in teacher_dict.items():
        if word in student_dict:
            sfreq = student_dict[word]
            if abs(tfreq - sfreq) >= 5:
                ssize += 1
    
    result = ((tsize - ssize)/tsize)*100
    
    return result

def evaluate_result(request, teacher_id):
    # print(teacher_id)
    context = {}
    teacher = Teacher.objects.get(teacher_id=teacher_id)
    context['teacher_id'] = teacher_id
    context['teacher'] = teacher

    if request.method == 'POST':

        teacher_key = request.FILES['teacher_key']
        student_sheet = request.FILES['student_sheet']
        student_roll = request.POST['roll_number']

        # print(teacher_key.name)
        # print(student_sheet.name)

        # answer_key = request.FILES.get('answer_key')
        fs = FileSystemStorage()
        fs.save(teacher_key.name, teacher_key)
        fs.save(student_sheet.name, student_sheet)

        teacher_string = converter(teacher_key.name)
        student_string = converter(student_sheet.name)

        context['teacher_string'] = teacher_string
        context['student_string'] = student_string

        percentage = percentage_calculator(teacher_string, student_string)
        context['percentage'] = percentage

        student = Student.objects.get(enrollment_number = student_roll)
        subject = Subject.objects.get(name = teacher.subject)
        context['student'] = student
        context['subject_id'] = subject.id

        marked_guy_obj = Marks(student_roll_number=student_roll, subject=subject.name, percentage=int(percentage))
        marked_guy_obj.save()

        print(marked_guy_obj)

        return render(request, 'backend/final_result.html', context)
    else:
        if request.method == 'GET':
            return render(request, 'backend/evaluate_result.html', context)
    
    return render(request, 'backend/evaluate_result.html', context)