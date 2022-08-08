from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.generic import FormView
from .models import SiteUser, Category as CatModel, Ledger
from .models import UserSelectedCategory as SelectedCat
from .forms import *
from .budget import Category as CatBudget, display, percentage

# Create your views here.
#https://docs.djangoproject.com/en/4.0/intro/tutorial04/


def register_request(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = SiteUser(username=username, password=password)
            user.set_password(password)
            user.save()
            messages.success(request, "Registration successful")
            login(request, user)
            return redirect ("account")
        messages.error(request, "Not registered.")
    form = CreateUserForm()
    return render(request=request, template_name="budgetapp/register.html",
                  context={"form": form}
                 )


def login_view (request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            print(username, password)
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("account")
            else: messages.error(request, "Not logged in.")
    form = LoginForm()
    return render (request=request, template_name="budgetapp/login.html", context={"form":form})


class AccountView (FormView):

    def get (self, request,*args, **kwargs):
        template = "budgetapp/account.html"
        current_user = request.user
        category_form = CategoryForm
        transaction_form = TransactionForm
        select_category_form = SelectForm (user=current_user)
        user_categories = CatModel.objects.filter (user = current_user)
        chart_data = percentage(user_categories)

        # Context.
        context = {"category_form": category_form,
                    "transaction_form": transaction_form,
                    "user_categories": user_categories,
                    "select_category_form": select_category_form,
                    "current_user": current_user,
                    "chart_data": chart_data
                    }
        return render(request, template, context)

    def post (self, request):
        transaction_form = TransactionForm(request.POST)
        category_form = CategoryForm (request.POST)
        # Creates a category.
        if "create_category" in request.POST and category_form.is_valid():
            category_name = request.POST ["category"]
            current_user = request.user
            CatB = CatBudget(category_name)
            CatM = CatModel(category_name=CatB.category_name,
                            balance=CatB.balance,
                            user_id = current_user.id)
            CatM.save()
            return HttpResponseRedirect ("account")
        if "submit_transaction" in request.POST and transaction_form.is_valid():
            # This looks fucked up, but: Creates an object of CatBudget class with the current
            # category data from the DB.
            current_user = request.user
            current_category = CatModel.objects.filter(
                category_id=SelectedCat.objects.filter(user=current_user)[0].selected_category)[0]
            current_ledger = Ledger.objects.filter(
                category=current_category.category_id).values("amount", "description")
            CatB = CatBudget(
                category_name=current_category.category_name,
                balance=current_category.balance,
                ledger=list(current_ledger))

            # Deposit transaction.
            if request.POST["deposit_or_withdraw"] == 'deposit':
                CatB.deposit(amount=request.POST["amount"], description=request.POST["description"])
                add_to_ledger = Ledger(category = current_category,
                                       amount = CatB.ledger[-1]["amount"],
                                       description = CatB.ledger[-1]["description"])
                add_to_ledger.save()
                current_category.balance = CatB.balance
                current_category.save(update_fields=['balance'])
                return HttpResponseRedirect("account")

            # Withdrawal transaction.
            if request.POST["deposit_or_withdraw"] == 'withdraw':
                amount = request.POST["amount"]
                # Checks that the withdrawal amount does not exceed the balance and saves.
                if CatB.withdraw(amount=amount,
                                 description=request.POST["description"]):
                    add_to_ledger = Ledger(category=current_category,
                                           amount=CatB.ledger[-1]["amount"],
                                           description=CatB.ledger[-1]["description"])
                    add_to_ledger.save()
                    current_category.balance = CatB.balance
                    current_category.save(update_fields=['balance'])
                else:
                    messages.error(request,
                    'The withdrawal amount exceeds the balance of this category! Transaction aborted.')
                return HttpResponseRedirect("account")
            return HttpResponseRedirect("account")
        return HttpResponseRedirect("account")

    def load_categories(request):
        """Displays selected category in the form of a cheque slip"""
        template = "budgetapp/load_categories.html"
        current_user = request.user
        user_categories = CatModel.objects.filter(user=current_user)
        select_category_form = SelectForm(user=current_user)
        # Input data for the display function.
        # Gets the category_id value from the htmx returned query string.
        category_id = request.GET['categories']
        current_category = user_categories.filter(category_id = category_id)[0]
        current_ledger = Ledger.objects.filter (
            category = current_category.category_id).values("amount", "description")
        category_display = display(category_name = current_category.category_name,
                                   ledger = current_ledger,
                                   balance = current_category.balance)
        context = {'select_category_form':select_category_form,
                   'category_display':category_display,
                   }
        print (request.GET['categories'])
        # Communicate selected category to other methods via a separate model field.
        try:
            user_selected_category =SelectedCat.objects.filter(
                user=current_user.id)[0]
        except:
            print ('USC for this cat does not exist. Creating')
            user_selected_category = SelectedCat(
                    user=SiteUser.objects.filter(id=current_user.id)[0])
        user_selected_category.selected_category = category_id #This is the message
        user_selected_category.save()
        print (user_selected_category.selected_category)
        #
        return render(request, template, context)





























































































