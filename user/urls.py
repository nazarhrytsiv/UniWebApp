from django.contrib.auth import login
from django.urls import path
from . import views

urlpatterns = [
    path('',         views.user, name='user'),
    path('login/', login, {'template_name': 'user/login.html'})
]
