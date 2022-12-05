import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from django.shortcuts import get_object_or_404

from lessons.forms import AvailabilityForm, LessonAdminForm, LessonForm, LessonStudentForm, LessonTeacherForm
from lessons.models import Lesson
from msms.models import Student, Teacher, User


@login_required(login_url='login')
def availability(request):
    '''View for a page which allows teachers & students to set their availability'''
    
    message = "Availability saved, "
    if request.user.is_student:
        model = Student
        message += "Request some lessons!"
    elif request.user.is_teacher:
        model = Teacher
        message += "Check your lessons"
    else:
        # user shoudln't be on this page, send home!
        return redirect('home')
    
    if request.method == 'POST':
        form = AvailabilityForm(request.POST)
        if form.is_valid():
            newavail = [form.cleaned_data[day] for day in DAYS]
            user = model.objects.get(user=request.user)
            user.availability = json.dumps(newavail)
            user.save()
            
            messages.add_message(request, messages.SUCCESS, message=message)
            return redirect('availability')

    days = get_availability(request.user, model)
    form = AvailabilityForm(days)
    return render(request, 'availability.html', {'form':form})


DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
def get_availability(user:User, model:type[Student|Teacher]):
    avail_list:list = model.objects.get(user=user).get_availability()
    return dict(zip(DAYS, avail_list))


@login_required(login_url='login')
def options(request):
    return render(request, "lessonoptions.html")


@login_required(login_url='login')
def request_lesson(request):
    if request.user.is_student:
        return redirect('student_request_lesson')
    elif request.user.is_teacher:
        return redirect('teacher_request_lesson')
    else:
        return redirect('admin_request_lesson')


class RequestLesson(LoginRequiredMixin, CreateView):
    model = Lesson
    form_class = LessonForm
    template_name = "requestlesson.html"
    
    def get_success_url(self, *args, **kwargs):
        return reverse_lazy("view_lessons")
  
    def form_valid(self, form):
        lesson:Lesson = form.save()
        if self.request.user.is_student:
            lesson.student = self.request.user.student
        
        elif self.request.user.is_teacher:
            lesson.teacher = self.request.user.teacher
            
        lesson.day = DAYS[lesson.first_lesson_date.weekday()].capitalize()
        lesson.save()
        messages.add_message(self.request, messages.INFO, "Successfully created a lesson!")
        return redirect('view_lessons')


class StudentRequestLesson(RequestLesson):
    form_class = LessonStudentForm
    
    def get(self, request, *args, **kwargs):
        # if user must be student to see this page
        if not request.user.is_student:
            messages.add_message(self.request, messages.INFO, "This page is not available to you")
            return redirect('home')

        return super().get(request, *args, **kwargs)
    
    
class TeacherRequestLesson(RequestLesson):
    form_class = LessonTeacherForm
    
    def get(self, request, *args, **kwargs):
        # if user must be teacher to see this page
        if not request.user.is_teacher:
            messages.add_message(self.request, messages.INFO, "This page is not available to you")
            return redirect('home')

        return super().get(request, *args, **kwargs)
    
    
class AdminRequestLesson(RequestLesson):
    form_class = LessonAdminForm
    
    def get(self, request, *args, **kwargs):
        # if user must be admin to see this page
        if not (request.user.is_admin or request.user.is_superuser):
            messages.add_message(self.request, messages.INFO, "This page is not available to you")
            return redirect('home')

        return super().get(request, *args, **kwargs)
    
    
def edit_lesson(request, pk:int):
    if request.user.is_student:
        return redirect('student_edit_lesson', pk)
    elif request.user.is_teacher:
        return redirect('teacher_edit_lesson', pk)
    else:
        return redirect('admin_edit_lesson', pk)


class EditLesson(LoginRequiredMixin, UpdateView):
    model = Lesson
    form_class = LessonForm
    template_name = "editlesson.html"
    
    def get_object(self, *args, **kwargs):
        lesson = get_object_or_404(Lesson, pk=self.kwargs['pk'])
        return lesson

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy("view_lessons")
    
    def form_valid(self, form):
        lesson:Lesson = form.save()
        lesson.day = DAYS[lesson.first_lesson_date.weekday()].capitalize()
        lesson.save()
        messages.add_message(self.request, messages.INFO, "Successfully edited a lesson!")
        return super().form_valid(form)


class StudentEditLesson(EditLesson):
    form_class = LessonStudentForm
    
    def get(self, request, *args, **kwargs):
        # if user must be student to see this page
        if not request.user.is_student:
            messages.add_message(self.request, messages.INFO, "This page is not available to you")
            return redirect('home')
        
        lesson = self.get_object(pk=self.kwargs['pk'])
        if lesson.student != request.user.student:
            messages.add_message(self.request, messages.INFO, "This page is not available to you")
            return redirect('home')

        return super().get(request, *args, **kwargs)


class TeacherEditLesson(EditLesson):
    form_class = LessonTeacherForm
    
    def get(self, request, *args, **kwargs):
        # if user must be teacher to see this page
        if not request.user.is_teacher:
            messages.add_message(self.request, messages.INFO, "This page is not available to you")
            return redirect('home')
        
        lesson = self.get_object(pk=self.kwargs['pk'])
        if lesson.teacher != request.user.teacher:
            messages.add_message(self.request, messages.INFO, "This page is not available to you")
            return redirect('home')

        return super().get(request, *args, **kwargs)


class AdminEditLesson(EditLesson):
    form_class = LessonAdminForm
    
    def get(self, request, *args, **kwargs):
        # if user must be teacher to see this page
        if not (request.user.is_admin or request.user.is_superuser):
            messages.add_message(self.request, messages.INFO, "This page is not available to you")
            return redirect('home')
        
        if request.user.is_admin:
            # redirect if lesson if not taught by teacher from the same school as admin
            lesson = self.get_object(pk=self.kwargs['pk'])
            if lesson.teacher.school != request.user.admin.school:
                messages.add_message(self.request, messages.INFO, "This page is not available to you")
                return redirect('home')

        return super().get(request, *args, **kwargs)


class ViewLessons(LoginRequiredMixin, ListView):
    model = Lesson
    template_name = "viewlessons.html"
    context_object_name = "lesson_list"
    
    def get_queryset(self):
        user:User = self.request.user
        kwarg = {"id__gte":0}
        if user.is_student:
            student = Student.objects.get(user=user)
            kwarg = {"student":student}
        
        elif user.is_teacher:
            teacher = Teacher.objects.get(user=user)
            kwarg = {"teacher":teacher}
            
        elif user.is_admin:
            school = user.admin.school
            kwarg = {"teacher__school":school}

            
        qs = {"booked":Lesson.objects.filter(state="B",**kwarg).order_by("state", "-first_lesson_date"),
              "requested":Lesson.objects.filter(state="R",**kwarg).order_by("state", "-first_lesson_date"),
              "cancelled":Lesson.objects.filter(state="C",**kwarg).order_by("state", "-first_lesson_date")}
        
        return qs
    
    
@login_required(login_url="login")
def cancel_lesson(request, pk:int):
    lesson = get_object_or_404(Lesson, pk=pk)
    if request.user.is_admin:
        # redirect if lesson if not taught by teacher from the same school as admin
        if lesson.teacher.school != request.user.admin.school:
            messages.add_message(request, messages.INFO, "This page is not available to you")
            return redirect('home')
    
    if request.user.is_student or request.user.is_teacher:
        if lesson.teacher.user != request.user and lesson.student.user != request.user:
            messages.add_message(request, messages.INFO, "This page is not available to you")
            return redirect('home')
       
    lesson.cancel()
    messages.add_message(request, messages.INFO, "Succesfully cancelled lesson")
    return redirect("view_lessons") 
    


@login_required(login_url="login")
def book_lesson(request, pk:int):
    if not (request.user.is_admin or request.user.is_superuser):
        messages.add_message(request, messages.INFO, "This page is not available to you")
        return redirect('home')
    
    lesson = get_object_or_404(Lesson, pk=pk)
    lesson.make_booking()
    messages.add_message(request, messages.INFO, "Succesfully booked lesson")
    return redirect("view_lessons") 
    
    
@login_required(login_url="login")
def finances(request):
    return render(request, "finances.html")