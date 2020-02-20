from django.contrib import admin

# Register your models here.
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import SignupForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = SignupForm
    form = CustomUserChangeForm
    list_display = ['email', 'username', 'isDeveloper']

admin.site.register(CustomUser, CustomUserAdmin)
