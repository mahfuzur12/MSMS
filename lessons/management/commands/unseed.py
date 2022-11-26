from django.core.management.base import BaseCommand, CommandError
from lessons.lesson_models.accounts import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Unseeding")
        User.objects.exclude(role="admin"
                            ).exclude(role="superadmin"
                            ).exclude(role="director").delete()
                            
        School.objects.all().delete()
        print("Finished")