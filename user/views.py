from django.shortcuts import render
from django.http import HttpResponse


def user(request):
    return HttpResponse('<h1>Hi</h1>')

# Create your views here.
