from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from random import randint

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout as logout_, login as login_
from django.http import (HttpRequest, HttpResponse,                 
                         HttpResponsePermanentRedirect as HttpRedirect)
import django

from .models import Expense, Client
from .forms import UploadForm
from .auth import EmailAuthBackend as auth

def index(request: HttpRequest) -> HttpRedirect:
    # user = get_user(request)
    # if not user.is_authenticated:
    #     return redirect(f"/login/")
    # try:
    #     user = User.objects.get(id=user.id)
    # except User.DoesNotExist:
    #     return redirect(f"/login/")
    return redirect(f"/add/")

@login_required
def add(request: HttpRequest, errors: dict | None = None) -> HttpResponse:
    return render(request, 'add.html')

@login_required
def add_expense(request: HttpRequest) -> HttpRedirect:
    if request.method != 'POST': 
        return redirect('/')
    form = UploadForm(request.POST, request.FILES)
    if not form.is_valid():
        return HttpResponse(str(form.errors)) # FIXME return add(request, form.errors)
    image = request.FILES['image']
    content_type, *_, ext = image.content_type.split('/')
    if content_type != 'image':
        return HttpResponse(f"File was {image.content_type}, should be image.")
    
    filepath = ''.join([
            './expenses/image',
            str(datetime.now().timestamp()),
            '.', ext,
        ])

    with open(filepath, 'wb+') as file:
        for chunk in image.chunks():
            file.write(chunk)

    # FIXME Find a better way to transform the arguments

    expense = dict(request.POST)
    expense['date'] = datetime.strftime(
        datetime.strptime(request.POST['date'],"%m/%d/%Y"),
        '%Y-%m-%d %H:%M')

    print(expense)

    for item in ['expense', 'amount', 'gst', 'notes']:
        expense[item] = expense[item][0]

    del expense['csrfmiddlewaretoken']
    expense['gst'] = expense['gst'] == 'on'

    Expense.objects.create(date_added = date.today(), 
                           image = filepath, 
                           client = request.user, 
                           **expense
                           )
    
    return redirect('/add')

@login_required
def expenses(request: HttpRequest) -> HttpResponse:
    client = request.user
    if not client.is_authenticated: 
        return redirect('/')
    expenses = list(Expense.objects.filter(client=client))
    expenses.sort(key=lambda e: e.date, reverse=True)
    expenses = [
        [e.date.strftime('%-d %b %y'), e.expense, f"${e.amount:.2f}", e.notes] for e in expenses
        ]
    return render(request, 'expenses.html', {'expenses': expenses})

def help(request: HttpRequest) -> HttpResponse:
    return render(request, 'help.html')

@login_required
def manage(request: HttpRequest, client_id: int | None = None) -> HttpResponse:
    if client_id is None:
        context={'clients': [[
                client.username,
                len(client.expenses),
                client.total,
                client.notes,
                client.gst,
            ] for client in Client.objects.get()]}
        return render(request, 'manage.html', context)

    return render(request, 'expenses.html', client_id)

def login(request: HttpRequest, token: str | None = None
        ) -> HttpResponse | HttpRedirect:
    if request.method == 'POST':
        if 'email' in request.POST:
            email = request.POST['email']
            try:
                client = Client.objects.get(email=email)
            except django.core.exceptions.ObjectDoesNotExist:
                client = Client.objects.create(
                    email=email,
                    username=str(randint(100000, 999999)))
                print("Created client and sent email")
            else:
                print("Sent email to " + client.email)
            auth.send_auth_email(client)
            return render(
                request, 'message.html',
                {'message': f"An email has been sent to {client.email}. Please open the sign in link on this device."})
        elif 'username' and 'password' in request.POST:
            authenticate(request, request.POST['username', 'password'])
            print("Authenticated with username and password")
            return redirect(request.POST['next'])
        else:
            print("Error, redirecting")
            return redirect('/login')
    elif request.method == 'GET' and token is not None:
        client = authenticate(request, token=token)
        if client is not None:
            login_(request, client)
            print("Authenticated", client)
            return redirect('/')
        else:
            print('Token not accepted: ', token)
            return redirect('login')
    else:
        return render(request, 'login.html')

def logout(request: HttpRequest) -> HttpRedirect:
    logout_(request)
    return redirect('/')