
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import User, Category as CatModel
from .forms import *
from .budget import Category as CatBudget

# Create your views here.
#https://docs.djangoproject.com/en/4.0/intro/tutorial04/

def register_request(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = User(username = username, password = password)
            user.set_password(password)
            user.save()                       
            messages.success(request, "Registration successful")
            return redirect ("account") 
        messages.error(request, "Not registered.")
        print ('nah, not good')
    form = CreateUserForm()
    return render (request=request, template_name="budgetapp/register.html", context={"form":form})#need the arguments here

def login_view (request): 
    if request.method == "POST":        
        form = LoginForm(request.POST)
        if form.is_valid():            
            username = request.POST['username']
            password = request.POST['password']
            print(username, password)
            user = authenticate(username=username, password=password)            
            if user is not None:
                print ("User is not none")
                login(request,user) 
                return redirect ("account") 
            else: messages.error(request, "Not logged in.")
    form = LoginForm()
    return render (request=request, template_name="budgetapp/login.html", context={"form":form})

def account_view (request): #lots of work. need to process forms separately (stackoverflow-qustion:866272)
    current_user = request.user
    if request.method == "POST":        
        transaction_form = TransactionForm(request.POST)
        category_form = CategoryForm (request.POST)
        if category_form.is_valid() or transaction_form.is_valid():
            category_name = request.POST ["category"]
            #urrent_user = request.user
            CatB = CatBudget(category_name)# category name is centered with *** should be removed later and styled instead with CSS
            CatM = CatModel(category_name=CatB.category_name, balance=CatB.balance, user_id = current_user)
            
            CatM.save()
            print(CatM.category_id, CatM.category_name,CatM.balance, current_user.id)
            #category.save() #how to connect budget.category and models.category?        
            #amount = request.POST['amount']
    user_categories = CatModel.objects.all()
            
    category_form = CategoryForm (request.GET)
    transaction_form = TransactionForm(request.GET)
    select_category_form = SelectForm (request.GET)
    context = {"category_form":category_form,
               "transaction_form":transaction_form,
               "user_categories":user_categories,
               "select_category_form":select_category_form}
    return render (request=request, template_name="budgetapp/account.html", context=context)
