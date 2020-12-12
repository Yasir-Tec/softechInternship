from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.core.exceptions import ValidationError

from .models import only_int,only_char

User._meta.get_field('email')._unique = True


class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, help_text='First Name',validators=[only_char])
    last_name = forms.CharField(max_length=100, help_text='Last Name',validators=[only_char])
    email = forms.EmailField(max_length=150, help_text='Email')
    mobile = forms.CharField(max_length=15,validators=[only_int])
    CompanyID = forms.CharField(max_length=20)



    class Meta:
        model = User
        fields = ('first_name', 'last_name',
                  'email', 'mobile', 'CompanyID', 'username', 'password1', 'password2')
