from django.urls import include, path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('login/<str:token>/', views.login, name='login'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),


    path('add/', views.add, name='add'),
    path('expenses/', views.expenses, name='expenses'),
    path('submit/', views.add_expense, name='add_expense'),

    path('help/', views.help, name='help'),

    path('manage/', views.manage, name='manage'),
    path('manage/<int:client>/', views.manage, name='manage'),   
]