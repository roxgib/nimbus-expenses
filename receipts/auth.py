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

def get_client(self, user_id):
    try:
        return Client.objects.get(pk=user_id)
    except User.DoesNotExist:
        return None