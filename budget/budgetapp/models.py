from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


# Create your models here.
class SiteUser(User):
    pass


class UserSelectedCategory(models.Model):
    user = models.OneToOneField(SiteUser, on_delete=models.CASCADE)
    selected_category = models.IntegerField()


class Category(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,default=0 , on_delete=models.CASCADE)
    category_id = models.BigAutoField(primary_key=True)
    category_name = models.CharField(max_length=50)
    balance = models.DecimalField(max_digits=19,decimal_places=2)
    def __str__(self):
        return self.category_name


class Ledger(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    transaction_id = models.BigAutoField(primary_key=True)
    transaction_time = models.DateTimeField (auto_now=True)
    amount = models.DecimalField(max_digits=19,decimal_places=2)
    description = models.CharField(max_length=50)
    def __str__(self):
        return self.description