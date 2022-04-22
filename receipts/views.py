from datetime import date, datetime

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import get_user
from django.http import HttpRequest, HttpResponse

from .models import Expense
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

def add(request: HttpRequest) -> HttpResponse:
    return render(request, 'add.html')

def expenses(request: HttpRequest) -> HttpResponse:
    expense_list =  [
        [
            expense.date.strftime('%-d %b %y'),
            expense.expense,
            f"${expense.amount:.2f}",
            expense.notes,
        ] for expense in sorted(Expense.objects.all(), key=lambda e: e.date, reverse=True)
    ]

    return render(request, 'expenses.html', {'expenses':expense_list})

def help(request: HttpRequest) -> HttpResponse:
    return render(request, 'help.html')

def submit(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid() and request.FILES['image'].content_type.split('/')[0] == 'image':
            print(request.FILES['image'].content_type)
            filepath = ''.join(
                [
                    './expenses/image',
                    str(datetime.now().timestamp()),
                    '.',
                    request.FILES['image'].content_type.split('/')[-1],
                ]
            )
            with open(filepath, 'wb+') as file:
                for chunk in request.FILES['image'].chunks():
            
                    file.write(chunk)
            e = Expense(
                date_added = date.today(),
                # date = request.POST['date'],
                date = datetime.strftime(
                    datetime.strptime(
                        request.POST['date'],
                        "%m/%d/%Y"
                    ),
                    '%Y-%m-%d %H:%M'
                ),
                amount = request.POST['amount'],
                image = filepath,
                notes = request.POST['notes'],
                expense = request.POST['expense'],
                # user = request.POST['user'],
            )
            e.save()
            return redirect('/add')
        else:
            return HttpResponse(str(form.errors))