from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, get_user_model, logout

User = get_user_model()


def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
        "form":form
    }
    if form.is_valid():
        # print("form valid")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(request, email=email, password=password)
        print(request.user.is_authenticated)
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
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        try:
            User.create_user(email, password)
            return redirect('/login')
        except:
            HttpResponse(status=403)
    return render(request, 'registration.html', context)


def logout_page(request):
    logout(request)
    return redirect('/')