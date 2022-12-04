import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import CreateView, ListView, UpdateView
from django.shortcuts import get_object_or_404

from lessons.forms import AvailabilityForm, LessonAdminForm, LessonForm
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



class RequestLesson(LoginRequiredMixin, CreateView):
    model = Lesson
    form_class = LessonForm
    template_name = "requestlesson.html"
    
    def form_valid(self, form):
        lesson:Lesson = form.save()
        student = None
        if self.request.user.is_student:
            student = Student.objects.get(user=self.request.user)
        else:
            # user shoudln't be on this page, send home!
            messages.add_message(self.request, messages.INFO, "Non students can't view lessons!?")
            return redirect('home')

        lesson.student = student
        lesson.save()
        messages.add_message(self.request, messages.INFO, "Successfully created a lesson!")
        return redirect('view_lessons')
    

class EditLesson(LoginRequiredMixin, UpdateView):
    model = Lesson
    form_class = LessonAdminForm
    template_name = "editlesson.html"
    
    def get_object(self, *args, **kwargs):
        lesson = get_object_or_404(Lesson, pk=self.kwargs['pk'])
        return lesson

    def get_success_url(self, *args, **kwargs):
        return redirect("home")
    
    '''
    def form_valid(self, form):
        lesson:Lesson = form.save()
        student = None
        if self.request.user.is_student:
            student = Student.objects.get(user=self.request.user)
        else:
            # user shoudln't be on this page, send home!
            messages.add_message(self.request, messages.INFO, "Non students can't view lessons!?")
            return redirect('home')

        lesson.student = student
        lesson.save()
        messages.add_message(self.request, messages.INFO, "Successfully created a lesson!")
        return redirect('view_lessons')'''
    

class ViewLessons(LoginRequiredMixin, ListView):
    model = Lesson
    template_name = "viewlessons.html"
    paginate_by = 10
    
    def get_queryset(self):
        user:User = self.request.user
        kwarg = {"id__gte":0}
        if user.is_student:
            student = Student.objects.get(user=user)
            kwarg = {"student":student}
        
        elif user.is_teacher:
            teacher = Teacher.objects.get(user=user)
            kwarg = {"teacher":teacher, "state":"B"}
            
        elif user.is_admin:
            school = user.admin.school
            kwarg = {"teacher__school":school}

            
        return Lesson.objects.filter(**kwarg).order_by("state")
    
    
    
    