from django.contrib import admin

from .models import Client, Expense

admin.site.register(Expense)

@admin.register(Client)
class HeroAdmin(admin.ModelAdmin):
    readonly_fields = ['date_joined', 'auth_code', 'auth_expiry']
