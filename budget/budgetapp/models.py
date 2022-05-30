from django.db import models

# Create your models here.
class User(models.Model):
    user_id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50) #https://stackoverflow.com/questions/17523263/how-to-create-password-field-in-model-django
    def __str__(self):
        return self.username
        
class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category_id = models.BigAutoField(primary_key=True)
    category_name = models.CharField(max_length=50)
    balance = models.DecimalField(max_digits=19,decimal_places=2)
    def __str__(self):
        return self.category_name

class Ledger(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE) #primary_key=True might cause problems
    transaction_id = models.BigAutoField(primary_key=True)
    transaction_time = models.DateTimeField (auto_now=True) #should it be auto_now?
    amount = models.DecimalField(max_digits=19,decimal_places=2)
    description = models.CharField(max_length=50)