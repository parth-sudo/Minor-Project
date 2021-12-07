from django.http.response import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic
from .models import Teacher, Student
from .forms import StudentForm, TeacherForm
import io
import PyPDF2

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

            for char in teacher_id:
                if char not in range(0, 10):
                    return HttpResponseBadRequest("Invalid teacher id, try again.") 
            if len(teacher_id) < 5:
                return HttpResponse("Invalid teacher id, try again.")
            
            form.save()
            return redirect("evaluation")
    else:
        form = TeacherForm()
        context['form'] = form

    return render(request, 'backend/teacher.html', context)

def student_result(request):
    if request.method == 'POST':
        answer_sheet = request.FILES['answer_sheet']
        roll = request.POST['roll_number']
        enroll = Student.objects.all().filter(enrollment_number = roll)
        if not enroll.exists():
            return HttpResponse("No student with that roll number found.")
        
        pdfFileObj = answer_sheet.read() 
        pdfReader = PyPDF2.PdfFileReader(io.BytesIO(pdfFileObj))
        NumPages = pdfReader.numPages
        i = 0
        content = []
        while (i<NumPages):
            text = pdfReader.getPage(i)
            content.append(text.extractText())
            i += 1
        print(content)

        return redirect('home')
        
    return render(request, 'backend/student_result.html', {})


def evaluation(request):
    return render(request, 'backend/evaluation.html', {})