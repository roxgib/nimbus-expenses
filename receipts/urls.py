from django.urls import include, path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('add/', views.add, name='add'),
    path('expenses/', views.expenses, name='expenses'),
    path('help/', views.help, name='help'),
    path('submit/', views.submit, name='submit'),
]

