from django.urls import path, include
from . import views
urlpatterns = [
 
    path ('account', views.account_view, name = 'account'),
]
