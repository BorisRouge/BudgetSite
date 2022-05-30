
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from .models import User
from .forms import CreateUserForm

# Create your views here.
#https://docs.djangoproject.com/en/4.0/intro/tutorial04/

def register_request(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = User(username = username, password = password)
            user.save()                       
            messages.success(request, "Registration successful")
            return redirect ("/admin") #need the url here
        messages.error(request, "Not good.")
        print ('nah, not good')
    form = CreateUserForm()
    return render (request=request, template_name="budgetapp/register.html", context={"form":form})#need the arguments here
            