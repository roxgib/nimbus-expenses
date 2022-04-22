from django.db import models
from django.contrib.auth.models import User as DefaultUser

class User(DefaultUser):
    pass

class Expense(models.Model):
    readonly_fields = 'date_added', 'user'
    # id = models.IntegerField('ID', primary_key=True)
    date_added = models.DateTimeField('Date Added')
    date = models.DateTimeField('Date')
    amount = models.DecimalField('Amount', decimal_places=1, max_digits=30)
    image = models.FilePathField(path='./expenses')
    notes = models.TextField('Notes', max_length=600)
    expense = models.TextField('Expense', max_length=300)
    user = models.ForeignKey(
        User,
        verbose_name="User", 
        on_delete=models.CASCADE, 
        default=None, 
        blank=True, 
        null=True
        )
    