from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth import authenticate, login


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
            print("Error")

    return render(request, 'login.html', context)