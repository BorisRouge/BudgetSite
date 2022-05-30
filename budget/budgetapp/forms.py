
from django import forms

from .models import User

class CreateUserForm(forms.Form):
    username = forms.CharField(label='Create your username:', max_length=50)
    password = forms.CharField(label='Create your password:', max_length=50)
    






