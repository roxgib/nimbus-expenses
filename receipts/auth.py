from typing import Callable
from datetime import datetime
from secrets import token_hex

from django.http import HttpRequest

from django.contrib.auth import get_user
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .models import Client

def require_auth(func: Callable, request: HttpRequest, 
                   *args, **kwargs) -> Callable:
    user = get_user(request)
    if not user.is_authenticated:
        return redirect(f"/manage/login/")
    try:
        user = User.objects.get(id=user.id)
    except User.DoesNotExist:
        return redirect(f"/manage/login/")


def require_auth(func: Callable, request: HttpRequest, 
                   *args, **kwargs) -> Callable:
    user = get_user(request)
    if not user.is_authenticated:
        return redirect(f"/manage/login/")
    try:
        user = User.objects.get(id=user.id)
    except User.DoesNotExist:
        return redirect(f"/manage/login/")

from django.contrib.auth.models import User, check_password


def auth_email(self, username=None, password=None):
    try:
        user = User.objects.get(email=username)
        if user.check_password(password):
            return user
    except User.DoesNotExist:
        return None


def get_client(self, user_id):
    try:
        return Client.objects.get(pk=user_id)
    except User.DoesNotExist:
        return None


def send_auth_email(client: Client) -> str:
    auth_code = token_hex(24)
    client.auth_code = auth_code
    client.auth_expiry = datetime.now() + datetime(0, 0, 1)
    client.save()
    # send_auth_email(client.email, auth_code)
    return auth_code


def validate_email_authentication(client: Client, auth_code: str) -> bool:
    if not client:
        return False
    if (client.auth_code
        and client.auth_code == auth_code 
        and client.auth_expiry > datetime.now()
    ):
        client.auth_code = ""
        client.save()
        return True
    else:
        return False