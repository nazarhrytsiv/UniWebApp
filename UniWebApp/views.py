from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login,get_user_model

User = get_user_model()

def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
        "form":form
    }
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        # print(request.user.is_authenticated)
        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            HttpResponse(status=403)

    return render(request, 'login.html', context)

def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        'form':form
    }
    if form.is_valid():
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        new_user = User.objects.create_user(username,email,password)
        print(new_user)
    return render(request, 'registration.html', context)