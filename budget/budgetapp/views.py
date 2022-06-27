
from unicodedata import category, decimal
from decimal import Decimal
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.generic import FormView
from django.core.exceptions import ValidationError
from .models import User, Category as CatModel, Ledger
from .forms import *
from .budget import Category as CatBudget, display

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
"""
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
"""
""" This is a test CBV for account """
class AccountView (FormView):
    

    def get (self, request, *args, **kwargs):
        template = "budgetapp/account.html"
        current_user = request.user
        category_form = CategoryForm 
        transaction_form = TransactionForm
        select_category_form = SelectForm (user=current_user)
        user_categories = CatModel.objects.filter (user = current_user)
        # Input data for the display function.
        current_category = user_categories[0] # This will throw an error later, when a user has multiple cats
        current_ledger = Ledger.objects.filter (category = current_category.category_id).values("amount", "description")       
        category_display = display(category_name = current_category.category_name, ledger = current_ledger, balance = current_category.balance)
        # Context.
        context = {"category_form":category_form,
                    "transaction_form":transaction_form,
                    "user_categories":user_categories,
                    "select_category_form":select_category_form,
                    "current_user":current_user,
                    "category_display":category_display,
                    "current_category_balance":current_category.balance}        
        return render (request, template, context)
    
    def post (self, request):
        transaction_form = TransactionForm(request.POST)
        category_form = CategoryForm (request.POST)
        # Creates a category.
        if request.POST.get("create_category") and category_form.is_valid():
            category_name = request.POST ["category"]
            current_user = request.user         # Might need to delete and use the class variable with self.
            CatB = CatBudget(category_name)     # Category name is centered with *** should be removed later and styled instead with CSS
            CatM = CatModel(category_name=CatB.category_name,
                            balance=CatB.balance,
                            user_id = current_user.id)
            CatM.save()            
            return HttpResponseRedirect ("account")
        if "submit_transaction" in request.POST and transaction_form.is_valid():
            # This looks fucked up, but: Creates an object of CatBudget class with the current 
            # category data from the DB (current should be modified to selected later)
            current_user = request.user
            current_category = get_object_or_404(CatModel, user = current_user)
            current_ledger = Ledger.objects.filter(
                category = current_category.category_id).values("amount", "description")
            CatB = CatBudget(
                category_name = current_category.category_name, 
                balance=current_category.balance, 
                ledger = list(current_ledger))

            # Deposit transaction.
            if request.POST["deposit_or_withdraw"] == 'deposit':
                CatB.deposit(amount=request.POST["amount"], description=request.POST["description"])
                add_to_ledger = Ledger(category = current_category,
                                       amount = CatB.ledger[-1]["amount"],
                                       description = CatB.ledger[-1]["description"])
                add_to_ledger.save()
                current_category.balance = CatB.balance
                current_category.save (update_fields=['balance'])
                return HttpResponseRedirect ("account")

            # Withdrawal transaction.
            if request.POST["deposit_or_withdraw"] == 'withdraw':
                amount = request.POST["amount"]
                # Checks that the withdrawal amount does not exceed the balance and save                
                if CatB.withdraw(amount=amount,
                                 description=request.POST["description"]) == True:
                    add_to_ledger = Ledger(
                                           category = current_category,
                                           amount = CatB.ledger[-1]["amount"],
                                           description = CatB.ledger[-1]["description"])
                    add_to_ledger.save()
                    current_category.balance = CatB.balance
                    current_category.save (update_fields=['balance'])
                else: 
                    messages.error(request,'The withdrawal amount exceeds the balance of this category! Transaction aborted.')
                return HttpResponseRedirect ("account")

            print("no response from the radio select")
            print(request.POST)
            return HttpResponseRedirect ("account")

        print("no response from the button")
        return HttpResponseRedirect ("account")

    def load_categories(request):
        template = ''
        current_user = request.user
        user_categories = CatModel.objects.filter (user = current_user)
        return render(request, template, {'categories': user_categories})
        
    
    






























































































