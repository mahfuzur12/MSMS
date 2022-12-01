from django.contrib import admin

from accounts.forms import UserChangeForm, UserCreationForm
from accounts.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    
    list_display = ["id",
                    "first_name",
                    "last_name",
                    "email",
                    "role",
                    "is_staff",
                    "password"
                    ]
    