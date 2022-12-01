from django.db import models
from django.utils import timezone
from msms.models import Student, Teacher
from lessons.schoolmodel import School

    
class Transfer(models.Model):
    reference = models.CharField(max_length=30)
    state = models.CharField(max_length=20, choices=[("I","incoming"),("P","processed")], default="I")
    amount = models.DecimalField(max_digits=20, default=0, decimal_places=2)
    date_transferred = models.DateField(default=timezone.now)
    
    
COST_PER_LESSON = 20

class Lesson(models.Model):
    num_lessons = models.IntegerField()
    interval = models.IntegerField(choices=[(1, 1),(2, 2)])
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    duration = models.DurationField()
    state = models.CharField(max_length=20, choices=[("R","request"),("B","booking"),("C","cancelled")], default="R")
    first_lesson_date = models.DateField(default=timezone.now)
      
    def make_booking(self):
        if self.state == "B":
            return
        
        self.state = "B"
        invoice = Invoice.create(
            amount=COST_PER_LESSON,
            student=self.student,
            lesson=self)
        try:
            self.save()
            invoice.save()
            return invoice
        except:
            self.state = "R"
            self.save()
            return None
    
    
    def __str__(self):
        return f"Lesson({self.pk}) {self.student}-{self.teacher}"
    
    
class Invoice(models.Model):
    amount = models.DecimalField(max_digits=20, default=0, decimal_places=2)
    number = models.IntegerField()
    date = models.DateField(default=timezone.now)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE)   
    
    def create(student, **kwargs):
        # get the next available invoice number
        number = Invoice.objects.filter(student=student).__len__() + 1
        return Invoice(student=student, number=number,**kwargs)
    
    
    def __str__(self):
        return f"Invoice {self.ref()}"
    
    
    def ref(self):
        return f"{self.student.user.pk}-{self.number}"