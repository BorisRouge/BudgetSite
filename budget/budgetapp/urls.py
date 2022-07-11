from urllib import request
from django.urls import path, include
from . import views
urlpatterns = [ 
    path ('account', views.AccountView.as_view(), name = 'account'),
    path ('account/load_categories', views.load_categories, name = 'load_categories'),    
]
