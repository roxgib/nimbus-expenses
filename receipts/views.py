from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import get_user

def index(request):
    # user = get_user(request)
    # if not user.is_authenticated:
    #     return redirect(f"/login/")
    # try:
    #     user = User.objects.get(id=user.id)
    # except User.DoesNotExist:
    #     return redirect(f"/login/")
    return redirect(f"/add/")

def add(request):
    return render(request, 'add.html')

def expenses(request):
    return render(request, 'expenses.html')

def help(request):
    return render(request, 'help.html')

