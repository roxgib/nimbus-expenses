from __future__ import annotations

from datetime import date, datetime

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse

from .models import Expense, Client
from .forms import UploadForm

def index(request: HttpRequest) -> HttpResponse:
    # user = get_user(request)
    # if not user.is_authenticated:
    #     return redirect(f"/login/")
    # try:
    #     user = User.objects.get(id=user.id)
    # except User.DoesNotExist:
    #     return redirect(f"/login/")
    return redirect(f"/add/")

def add(request: HttpRequest, errors: dict | None = None) -> HttpResponse:
    return render(request, 'add.html')

def expenses(request: HttpRequest, user: int | None = None) -> HttpResponse:
    expense_list =  [
        [
            expense.date.strftime('%-d %b %y'),
            expense.expense,
            f"${expense.amount:.2f}",
            expense.notes,
        ] for expense in sorted(Expense.objects.all(), 
                                key=lambda e: e.date, 
                                reverse=True)
    ]
    return render(request, 'expenses.html', {'expenses': expense_list})

def help(request: HttpRequest) -> HttpResponse:
    return render(request, 'help.html')

def submit(request: HttpRequest) -> HttpResponse:
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

    # FIXME Subclass model.init to transform the arguments
    request.POST['date'] = datetime.strftime(
            datetime.strptime(request.POST['date'],"%m/%d/%Y"),
            '%Y-%m-%d %H:%M')

    Expense(date_added = date.today(), image = filepath, **request.POST).save()
        # user = request.POST['user'], # FIXME Need to send user information
    
    return redirect('/add')

def manage(request: HttpRequest, client: int | None = None) -> HttpResponse:
    if client is None:
        context={'clients': [[
                _user.user,
                len(_user.expenses),
                _user.total,
                _user.notes,
                _user.gst,
            ] for _user in Client.objects.get()]}
        return render(request, 'manage.html', context)

    return render(request, 'expenses.html', client)