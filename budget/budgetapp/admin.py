from django.contrib import admin

from .models import User, Category, Ledger

class UserAdmin (admin.ModelAdmin):
    list_display = ('id', 'username', 'password')
    pass
admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(Ledger)
# Register your models here.
