from functools import reduce
from typing import List

from django.db import models

class Client(models.Model): 
    name = models.TextField('Expense', max_length=300)
    email = models.EmailField("E-mail", 'email', max_length=60, unique=True)
    notes = models.TextField('Notes', max_length=300)
    username     = models.CharField(max_length=30,unique=True)
    date_joined  = models.DateTimeField('date joined', auto_now_add=True)
    auth_code    = models.TextField("Autentication Code", 'auth_code', None, 
                                    max_length=24)
    auth_expiry  = models.DateTimeField("Authentication Code Expiry Date",      
                                        'auth_expiry')

    REQUIRED_FIELDS = ['username', 'email', 'date_joined']
    READONLY_FIELDS = ['date_joined']

    def __str__(self):
        return self.name

    @property
    def expenses(self) -> list:
        return Expense.objects.all(client=self)

    @property
    def total(self) -> list:
        return reduce(lambda e: e.amount, Expense.objects.all(client=self))

class Expense(models.Model):
    readonly_fields = 'date_added', 'user'
    # id = models.IntegerField('ID', primary_key=True)
    expense = models.TextField('Expense', max_length=300)
    amount = models.DecimalField("Amount", 'amount', 12, 2)
    date = models.DateTimeField('Date', 'date')
    gst = models.BooleanField("Includes GST?", 'gst')
    notes = models.TextField('Notes', max_length=600)
    image = models.FilePathField("Image_File", path='./expenses')
    date_added = models.DateTimeField('Date Added', 'date_added')
    client = models.ForeignKey(
        Client,
        verbose_name="User", 
        on_delete=models.DO_NOTHING, 
        default=None,
        blank=True, 
        null=True
    )