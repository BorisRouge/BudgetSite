from django.contrib import admin

from .models import SiteUser, Category, Ledger

class UserAdmin (admin.ModelAdmin):
    list_display = ('id', 'username', 'password')
    pass
class CatAdmin (admin.ModelAdmin):
    list_display = ('user', 'category_id', 'category_name', 'balance')
    pass
admin.site.register(SiteUser, UserAdmin)
admin.site.register(Category, CatAdmin)
admin.site.register(Ledger)
# Register your models here.
