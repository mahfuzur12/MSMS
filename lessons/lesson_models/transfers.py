from django.db import models
from django.utils import timezone


class Transfer(models.Model):
    reference = models.CharField(max_length=30)
    state = models.CharField(max_length=20, choices=[("I","incoming"),("C","confirmed")], default="I")
    amount = models.DecimalField(max_digits=20, default=0, decimal_places=2)
    date_transferred = models.DateField(default=timezone.now)