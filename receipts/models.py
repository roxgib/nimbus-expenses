from datetime import datetime, timedelta
from secrets import token_hex

from django.db import models

class Client(models.Model): 
    name = models.CharField('Expense', max_length=300)
    email = models.EmailField("E-mail", 'email', max_length=60, unique=True)
    notes = models.TextField('Notes', max_length=300, null=True, blank=True)
    username     = models.CharField(max_length=30, unique=True)
    date_joined  = models.DateTimeField('date joined', auto_now_add=True)
    auth_code    = models.CharField("Autentication Code", 'auth_code', None, 
                                    max_length=24, null=True, blank=True)
    auth_expiry  = models.DateTimeField("Authentication Code Expiry Date",      
                                        'auth_expiry', null=True, blank=True)

    REQUIRED_FIELDS = ['username', 'email', 'date_joined']
    READONLY_FIELDS = ['date_joined']

    def __str__(self):
        return self.name

    @property
    def expenses(self) -> list:
        return Expense.objects.filter(client=self)

    @property
    def total(self) -> list:
        expenses = Expense.objects.filter(client=self)
        if expenses is None: return 0
        return sum([e.amount for e in expenses])

    def send_auth_email(self, code: str) -> None:
        pass

    def set_auth_code(self) -> str:
        auth_code = token_hex(24)
        self.auth_code = auth_code
        self.auth_expiry = datetime.now() + timedelta(1)
        return auth_code

    def validate_auth_code(self, auth_code: str) -> bool:
        if (self.auth_code is not None
            and self.auth_code == auth_code 
            and self.auth_expiry > datetime.now()
        ):
            self.reset_auth()
            return True
        else:
            self.reset_auth()
            return False

    def reset_auth(self):
        self.auth_code = None
        self.auth_expiry = None


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
        return f"{self.client.name} ({self.expense}, ${self.amount}, {date})"