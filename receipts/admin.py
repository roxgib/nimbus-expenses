from django.contrib import admin

from receipts.models import Client, Expense

admin.site.register(Expense)
admin.site.register(Client)
