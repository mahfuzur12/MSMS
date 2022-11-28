from django.contrib.auth.forms import UserCreationForm as UCreate, UserChangeForm as UChange

from accounts.models import User


class UserCreationForm(UCreate):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "role", "is_staff")
    
    
class UserChangeForm(UChange):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "role", "is_staff")