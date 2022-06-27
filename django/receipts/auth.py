from datetime import datetime, timedelta, timezone
from secrets import token_hex
import string

from django.http import HttpRequest
import django.contrib.auth.backends
from django.core import mail
from django.conf import settings

from receipts.models import Client

class EmailAuthBackend(django.contrib.auth.backends.BaseBackend):
    @classmethod
    def authenticate(auth, request: HttpRequest, token: str):
        try: 
            client = Client.objects.get(auth_token=token)
        except Client.DoesNotExist:
            return None

        auth_expiry = client.auth_expiry

        if not (auth.reset_auth(client)
            and token
            and auth_expiry
            and auth_expiry > datetime.now(timezone.utc)
            and type(token) is str
            and len(token) == settings.AUTH_TOKEN_LENGTH * 2
            and all(d in string.hexdigits for d in token)
            and client.is_active):
                return None
        return client
        
    @staticmethod
    def get_user(user_id):
        try:
            return Client.objects.get(id=user_id)
        except Client.DoesNotExist:
            return None

    @staticmethod
    def set_auth_token(client: Client) -> str:
        token = token_hex(settings.AUTH_TOKEN_LENGTH)
        client.auth_token = token
        client.auth_expiry = datetime.now() + timedelta(1)
        client.save()
        return token

    @classmethod
    def send_auth_email(auth, client: Client):
        token = auth.set_auth_token(client)
        content = ("Please use this link to authenticate: "
                + settings.EMAIL_LINK_DOMAIN
                + '/login/'
                + token)
        mail.send_mail("Nimbus Expenses", content,
                       "expenses@nimbus.financial", 
                       [client.email])

    @staticmethod
    def reset_auth(client: Client):
        client.auth_token = None
        client.auth_expiry = None
        client.save()
        return True