from datetime import datetime, timedelta
from secrets import token_hex
import string

from django.http import HttpRequest
from django.contrib import auth
from django.contrib.auth.models import User
from django.core import mail
from django.conf import settings

from receipts.models import Client

class EmailAuthBackend(auth.backends.BaseBackend):
    @staticmethod
    def authenticate(request: HttpRequest, token: str):
        try: 
            client = Client.objects.get(auth_token=token)
            print("Client matched: ", client)
        except Client.DoesNotExist:
            print("Client not matched: ", token)
            for client in Client.objects.all():
                print(client, client.auth_token)
            return None

        auth_expiry = client.auth_expiry
        client.reset_auth()

        print(
            auth_expiry,
            # auth_expiry > datetime.now(),
            type(token) is str,
            len(token) == settings.AUTH_TOKEN_LENGTH * 2,
            all(d in string.hexdigits for d in token),
            client.is_active,
        )

        if not (token
            and auth_expiry
            # and auth_expiry > datetime.now()
            and type(token) is str
            and len(token) == settings.AUTH_TOKEN_LENGTH * 2
            and all(d in string.hexdigits for d in token)
            and client.is_active):
                return None

        return client
        
    @classmethod
    def get_user(self, user_id):
        try:
            return Client.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    @classmethod
    def set_auth_token(self, client: Client) -> str:
        token = token_hex(settings.AUTH_TOKEN_LENGTH)
        client.auth_token = token
        client.auth_expiry = datetime.now() + timedelta(1)
        client.save()
        return token    # returned for testing purposes

    @classmethod
    def send_auth_email(self, client: Client):
        token = self.set_auth_token(client)
        content = ("Please use this link to authenticate: "
                + settings.EMAIL_LINK_DOMAIN
                + 'login/'
                + token)
        mail.send_mail("Nimbus Expenses", content,
                       "expenses@nimbus.financial", 
                       [client.email])