import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from django.shortcuts import get_object_or_404

from lessons.forms import AvailabilityForm, LessonAdminForm, LessonForm, LessonStudentForm, LessonTeacherForm
from lessons.models import Lesson, Transfer, Invoice
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
        messages.add_message(request, messages.INFO, "This page is not available to you")
        return redirect('home')
    
    if request.method == 'POST':
        # recreate form from existing details given in POST
        form = AvailabilityForm(request.POST)
        if form.is_valid():
            # get new availability from form
            newavail = [form.cleaned_data[day] for day in DAYS]
            user = model.objects.get(user=request.user)
            
            # converts newavail list into string
            user.availability = json.dumps(newavail)
            user.save()
            
            messages.add_message(request, messages.SUCCESS, message=message)
            return redirect('availability')

    # create form using users pre-existing availability
    days = get_availability(request.user, model)
    form = AvailabilityForm(days)
    return render(request, 'availability.html', {'form':form})


DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
def get_availability(user:User, model:type[Student|Teacher]):
    '''Returns a dictionary mapping of a day of the week to the user's availability on that day'''
    
    avail_list:list = model.objects.get(user=user).get_availability()
    return dict(zip(DAYS, avail_list))


@login_required(login_url='login')
def options(request):
    return render(request, "lessonoptions.html")


@login_required(login_url='login')
def request_lesson(request):
    '''Redirects user to a specific type of request page depending on user type'''
    
    if request.user.is_student:
        return redirect('student_request_lesson')
    elif request.user.is_teacher:
        return redirect('teacher_request_lesson')
    else:
        return redirect('admin_request_lesson')


class RequestLesson(LoginRequiredMixin, CreateView):
    '''A base request lesson form. Includes success page, 
    and what to do when the form is valid'''
    
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
    '''Modifies form class of the base RequestLesson class,
    redirects used to home if user is not a student'''
    
    form_class = LessonStudentForm
    
    def get(self, request, *args, **kwargs):
        # if user must be student to see this page
        if not request.user.is_student:
            messages.add_message(self.request, messages.INFO, "This page is not available to you")
            return redirect('home')

        return super().get(request, *args, **kwargs)
    
    
class TeacherRequestLesson(RequestLesson):
    '''Modifies form class of the base RequestLesson class,
    redirects used to home if user is not a teacher'''
    
    form_class = LessonTeacherForm
    
    def get(self, request, *args, **kwargs):
        # if user must be teacher to see this page
        if not request.user.is_teacher:
            messages.add_message(self.request, messages.INFO, "This page is not available to you")
            return redirect('home')

        return super().get(request, *args, **kwargs)
    
    
class AdminRequestLesson(RequestLesson):
    '''Modifies form class of the base RequestLesson class,
    redirects used to home if user is not an admin'''
    
    form_class = LessonAdminForm
    
    def get(self, request, *args, **kwargs):
        # if user must be admin to see this page
        if not (request.user.is_admin or request.user.is_superuser):
            messages.add_message(self.request, messages.INFO, "This page is not available to you")
            return redirect('home')

        return super().get(request, *args, **kwargs)
    
    
def edit_lesson(request, pk:int):
    '''Redirects user to a specific type of edit page depending on user type'''
    
    if request.user.is_student:
        return redirect('student_edit_lesson', pk)
    elif request.user.is_teacher:
        return redirect('teacher_edit_lesson', pk)
    else:
        return redirect('admin_edit_lesson', pk)


class EditLesson(LoginRequiredMixin, UpdateView):
    '''A base edit lesson form. Includes success page, 
    and what to do when the form is valid'''
    
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
    '''Modifies form class of the base EditLesson class, 
    redirects used to home if user is not a student'''
    
    form_class = LessonStudentForm
    
    def get(self, request, *args, **kwargs):
        # user must be student to see this page
        if not request.user.is_student:
            messages.add_message(self.request, messages.INFO, "This page is not available to you")
            return redirect('home')
        
        lesson = self.get_object(pk=self.kwargs['pk'])
        if lesson.student != request.user.student:
            messages.add_message(self.request, messages.INFO, "This page is not available to you")
            return redirect('home')

        return super().get(request, *args, **kwargs)


class TeacherEditLesson(EditLesson):
    '''Modifies form class of the base EditLesson class, 
    redirects used to home if user is not a teacher'''
    
    form_class = LessonTeacherForm
    
    def get(self, request, *args, **kwargs):
        # user must be teacher to see this page
        if not request.user.is_teacher:
            messages.add_message(self.request, messages.INFO, "This page is not available to you")
            return redirect('home')
        
        lesson = self.get_object(pk=self.kwargs['pk'])
        if lesson.teacher != request.user.teacher:
            messages.add_message(self.request, messages.INFO, "This page is not available to you")
            return redirect('home')

        return super().get(request, *args, **kwargs)


class AdminEditLesson(EditLesson):
    '''Modifies form class of the base EditLesson class, 
    redirects used to home if user is not an admin'''
    
    form_class = LessonAdminForm
    
    def get(self, request, *args, **kwargs):
        # user must be amin to see this page
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
    '''A view for displaying lessons on the page'''
    
    model = Lesson
    template_name = "viewlessons.html"
    context_object_name = "lesson_list"

    def get_queryset(self):
        user:User = self.request.user
        # by default display every lesson
        kwarg = {"id__gte":0}
        
        if user.is_student:
            # display lessons where this user is the student
            student = Student.objects.get(user=user)
            kwarg = {"student":student}
        
        elif user.is_teacher:
            # display lessons where this user is the teacher
            teacher = Teacher.objects.get(user=user)
            kwarg = {"teacher":teacher}
            
        elif user.is_admin:
            # display lessons where the teacher is from the admin's school
            school = user.admin.school
            kwarg = {"teacher__school":school}

        
        # seperate booked, requested and cancelled lessons   
        qs = {"booked":Lesson.objects.filter(state="B",**kwarg).order_by("state", "-first_lesson_date"),
              "requested":Lesson.objects.filter(state="R",**kwarg).order_by("state", "-first_lesson_date"),
              "cancelled":Lesson.objects.filter(state="C",**kwarg).order_by("state", "-first_lesson_date")}
        
        return qs
    
    
@login_required(login_url="login")
def cancel_lesson(request, pk:int):
    '''A view which cancels a lesson.
    Cancels from Non-superuser accounts have some restrictions'''
    
    lesson = get_object_or_404(Lesson, pk=pk)
    if request.user.is_admin:
        # redirect if lesson if not taught by teacher from the same school as admin
        if lesson.teacher.school != request.user.admin.school:
            messages.add_message(request, messages.INFO, "This page is not available to you")
            return redirect('home')
    
    if request.user.is_student or request.user.is_teacher:
        # redirect if lesson is not taught by or studied by user
        if lesson.teacher.user != request.user and lesson.student.user != request.user:
            messages.add_message(request, messages.INFO, "This page is not available to you")
            return redirect('home')
       
    lesson.cancel()
    messages.add_message(request, messages.INFO, "Succesfully cancelled lesson")
    return redirect("view_lessons") 
    


@login_required(login_url="login")
def book_lesson(request, pk:int):
    '''A view which cancels a lesson.
    Cancels from Non-superuser accounts have some restrictions'''
    
    if not (request.user.is_admin or request.user.is_superuser):
        # only admins and superusers can book lessons
        messages.add_message(request, messages.INFO, "This page is not available to you")
        return redirect('home')
    
    lesson = get_object_or_404(Lesson, pk=pk)
    if request.user.is_admin:
        # redirect if lesson if not taught by teacher from the same school as admin
        if lesson.teacher.school != request.user.admin.school:
            messages.add_message(request, messages.INFO, "This page is not available to you")
            return redirect('home')
     
    lesson.make_booking()
    messages.add_message(request, messages.INFO, "Succesfully booked lesson")
    return redirect("view_lessons") 
    
    
class Finances(LoginRequiredMixin, ListView):
    '''A view for seeing a user's finances'''

    model = Transfer
    template_name = "finances.html"
    # name of dictionary containing list of transfers and invoices 
    context_object_name = "confirmed_transfers_and_invoices_list"

    def get_queryset(self):
        user:User = self.request.user
        kwarg = {"id__gte":0}

        if user.is_student:
            # studentTransfers; transfers to be viewed by students.
            student = Student.objects.get(user=user)
            kwarg = {"student":student}
            qs = {"allTransfers":Transfer.objects.filter(**kwarg).order_by("-date_transferred"),
            "allInvoices":Invoice.objects.filter(**kwarg).order_by("-date")}
            return qs

        elif user.is_teacher:
            # redirect if teacher reaches finance page
            messages.add_message(self.request, messages.INFO, "This page is not available to you")
            return redirect('home')

        elif user.is_admin:
            # allTransfers; all transfers to be viewed by admin.
            qs = {"allTransfers":Transfer.objects.all(),
            "allInvoices":Transfer.objects.all()}
            return qs

        # by default display every transfer and invoice
        qs = {"allTransfers":Transfer.objects.all(),
            "allInvoices":Transfer.objects.all()}

        return qs

        


@login_required(login_url="login")
def confirmTransfer(request):
    '''A view for confirming a bank transfer'''




    return render(request, "confirmTransfer.html")

@login_required(login_url="login")
def view_invoice(request, pk:int):
    '''A view for seeing an invoice'''

    invoice = get_object_or_404(Invoice, pk=pk)
    if request.user.is_admin:
        # redirect if the admin is not in the same school the invoice comes from
        if invoice.lesson.teacher.school != request.user.admin.school:
            messages.add_message(request, messages.INFO, "This page is not available to you")
            return redirect('home')
    
    if request.user.is_student:
        # redirect if the user is not the student in the invoice
        if invoice.student.user.pk != request.user.pk:
            messages.add_message(request, messages.INFO, "This page is not available to you")
            return redirect('home')

    return render(request, 'invoice_view.html', {"invoice":invoice})

