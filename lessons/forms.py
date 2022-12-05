import datetime
from django import forms
from django.forms import ModelForm

from lessons.models import Lesson


class AvailabilityForm(forms.Form):
    monday = forms.BooleanField(required=False)
    tuesday = forms.BooleanField(required=False)
    wednesday = forms.BooleanField(required=False)
    thursday = forms.BooleanField(required=False)
    friday = forms.BooleanField(required=False)
    saturday = forms.BooleanField(required=False)
    sunday = forms.BooleanField(required=False)
    
    
class LessonMeta():
    model = Lesson
    fields = ['num_lessons',
              'interval',
              'duration',
              'first_lesson_date']
    
    widgets = {
        'first_lesson_date':forms.widgets.DateInput(attrs={'type': 'date'})
    }


class LessonForm(ModelForm):
    class Meta(LessonMeta):
        pass
        
    def clean_first_lesson_date(self):
        '''Make sure date is today or in the future'''
        date = self.cleaned_data['first_lesson_date']
        if date < datetime.date.today():
            raise forms.ValidationError("Date must be today or in the future")
        return date


class LessonStudentForm(LessonForm):
    '''Normal Lesson form but also includes student instead of teacher'''
    class Meta(LessonMeta):
        fields = ['num_lessons',
                  'interval',
                  'teacher',
                  'duration',
                  'first_lesson_date']


class LessonTeacherForm(LessonForm):
    '''Normal Lesson form but also includes student instead of teacher'''
    class Meta(LessonMeta):
        fields = ['num_lessons',
                  'interval',
                  'student',
                  'duration',
                  'first_lesson_date']
        


class LessonAdminForm(LessonForm):
    '''Normal Lesson form but also includes student'''
    class Meta(LessonMeta):
        fields = ['num_lessons',
                  'interval',
                  'student',
                  'teacher',
                  'duration',
                  'first_lesson_date']