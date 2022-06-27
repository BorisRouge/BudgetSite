
from tabnanny import verbose
from urllib import request
from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from .models import User, Category

# This validator was not working and is not used now.
def only_digits(value):
    """Removes - from the value"""
    if "-" in str(value):
        raise ValidationError('Please use only positive values')




class CreateUserForm(forms.Form):
    username = forms.CharField(label='Create your username:', max_length=50)
    password = forms.CharField(label='Create your password:', max_length=256, widget = forms.PasswordInput(render_value=False))
    
class LoginForm(forms.Form):
    username = forms.CharField(label='Enter your username:', max_length=50)
    password = forms.CharField(label='Enter your password:', max_length=256, widget = forms.PasswordInput(render_value=True))


class CategoryForm(forms.Form):
    category = forms.CharField(label='Create your category', max_length=50, required=False)

class TransactionForm(forms.Form):
    """Manages transactions in the account."""
    TRANSACTION_TYPE = [('deposit', 'Deposit'), ('withdraw', 'Withdraw')]
    deposit_or_withdraw = forms.ChoiceField (label ="", widget=forms.RadioSelect, choices=TRANSACTION_TYPE, required=True)
    amount = forms.DecimalField(label='Transaction amount', required=False, min_value=0.01) 
    description = forms.CharField(label='Comment', max_length=50, required=False)
    
    
class SelectForm(forms.Form):
    categories = forms.ModelChoiceField(queryset=Category.objects.all()) #how to get only the categories by user_id? StackO question No. 7299973
    
    """Create an additional argument to limit the form to the current user."""
    def __init__(self,  user, **kwargs) -> None:
        super(SelectForm, self).__init__(**kwargs)
        self.fields['categories'].queryset = Category.objects.filter(user=user)
        

    
