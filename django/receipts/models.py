from datetime import datetime, timedelta
from secrets import token_urlsafe

from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import User

from nimbus import settings

class Client(User):
    notes = models.TextField('Notes', max_length=300, null=True, blank=True)
    auth_token = models.CharField("Authentication Code", 'auth_token', None, 
                                  max_length=128, null=True, blank=True)
    auth_expiry = models.DateTimeField("Authentication Code Expiry Date",
                                       'auth_expiry', null=True, blank=True)

    def __str__(self):
        return self.username

    @property
    def expenses(self) -> list:
        return Expense.objects.filter(client=self)

    @property
    def total(self) -> list:
        expenses = Expense.objects.filter(client=self)
        if expenses is None: return 0
        return sum([e.amount for e in expenses])


class Expense(models.Model):
    readonly_fields = 'date_added', 'user'
    # id = models.IntegerField('ID', primary_key=True)
    expense = models.TextField('Expense', max_length=300)
    amount = models.DecimalField("Amount", 'amount', 12, 2)
    date = models.DateTimeField('Date', 'date')
    gst = models.BooleanField("Includes GST?", 'gst')
    notes = models.TextField('Notes', max_length=600, null=True, blank=True)
    image = models.FilePathField("Image_File", path='./expenses', null=True, blank=True)
    date_added = models.DateTimeField('Date Added', 'date_added')
    client = models.ForeignKey(
        Client,
        verbose_name="User", 
        on_delete=models.DO_NOTHING, 
        default=None,
        blank=True, 
        null=True
    )

    def __str__(self):
        date = self.date.strftime('%-d %b')
        return f"{self.client.username} ({self.expense}, ${self.amount}, {date})"