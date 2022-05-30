from django.contrib import admin

from .models import User, Category, Ledger

class UserAdmin (admin.ModelAdmin):
    list_display = ('user_id', 'username', 'password')

admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(Ledger)
# Register your models here.
