from django.db import models


class School(models.Model):
    name = models.CharField(max_length=20)
    
    def __str__(self):
        return f"({self.pk}) {self.name}"