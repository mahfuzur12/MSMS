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
    
    
class LessonForm(ModelForm):
    class Meta:
        model = Lesson
        fields = ['num_lessons',
                  'interval',
                  'teacher',
                  'duration',
                  'first_lesson_date']