from django.db import models
from django.contrib.auth.models import User

class Expense(models.Model):
    id = models.IntegerField('ID', primary_key=True)
    date_added = models.DateTimeField('Date Added')
    date = models.DateTimeField('Date')
    amount = models.DecimalField('Amount', decimal_places=1, max_digits=30)
    image = models.FilePathField()
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE, default=None, blank=True, null=True)