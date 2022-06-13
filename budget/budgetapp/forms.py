
from tabnanny import verbose
from urllib import request
from django import forms
from django.contrib.auth import password_validation

from .models import User, Category

class CreateUserForm(forms.Form):
    username = forms.CharField(label='Create your username:', max_length=50)
    password = forms.CharField(label='Create your password:', max_length=256, widget = forms.PasswordInput(render_value=False))
    
class LoginForm(forms.Form):
    username = forms.CharField(label='Enter your username:', max_length=50)
    password = forms.CharField(label='Enter your password:', max_length=256, widget = forms.PasswordInput(render_value=True))


class CategoryForm(forms.Form):
    category = forms.CharField(label='Create your category', max_length=50, required=False)

class TransactionForm(forms.Form):
    TRANSACTION_TYPE = [('deposit', 'Deposit'), ('withdraw', 'Withdraw')]
    amount = forms.CharField(label='Transaction amount', max_length=50, required=False) #should be only float
    deposit_or_withdraw = forms.ChoiceField (label ="", widget=forms.RadioSelect, choices=TRANSACTION_TYPE, required=False)
    
class SelectForm(forms.Form):
    categories = forms.ModelChoiceField(queryset=Category.objects.all()) #how to get only the categories by user_id? StackO question No. 7299973




