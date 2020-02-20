from django import forms
from django.contrib.auth import get_user_model, password_validation
# from .models import Transaction
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import CustomUser
User = get_user_model()


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields

class SignupForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    isDeveloper = forms.BooleanField(label="Sign up as developer",
                                      required=False)
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        try:
            password_validation.validate_password(password, self.instance)
        except forms.ValidationError as error:
            self.add_error('password', error)
        return password

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password', 'isDeveloper']
