"""budget URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from budgetapp import views

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path ('', views.register_request, name='register'),# make it a homepage later, and registration should be a part of it
    path ('login', views.login_view, name ='login'),
    #path("", views.homepage, name="homepage"),
    path("budget/", include('budgetapp.urls')),
    
    #path('ajax/load-categories/', 
    #      views.AccountView.load_categories, name='ajax_load_categories'),
]
