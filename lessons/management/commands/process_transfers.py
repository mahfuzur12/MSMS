'''A command for processing the incoming transfers of the app'''
from django.core.management.base import BaseCommand

from lessons.models import Transfer
from msms.models import User, Student


class Command(BaseCommand):
    '''A class responsible for processing all incoming transfers'''
    
    def handle(self, *args, **options):
        print("Processing")
        transfers = Transfer.objects.filter(state="I")
        for transfer in transfers.iterator():
            reference = transfer.reference
            # refeference is in form stud_id-inv_id
            try:
                stud_id = int(reference.split("-")[0])
                user = User.objects.get(pk=stud_id)
                student = Student.objects.get(user=user)
                
                balance_added = transfer.amount
                student.balance += balance_added
                transfer.state = "P"
                transfer.save()
                student.save()
            except:
                pass
            
        print("Finished")
