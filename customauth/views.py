from djongo.models import json
import json
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.utils.http import is_safe_url
from django.core.mail import send_mail

User = get_user_model()


def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
        "form":form
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid():
        # print("form valid")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(request, email=email, password=password)
        print(request.user.is_authenticated)
        if user is not None:
            login(request,user)
            if is_safe_url(redirect_path,request.get_host()):
                return redirect(redirect_path)
            return redirect('/')
        else:
            HttpResponse(status=403)

    return render(request, 'login.html', context)


def register_page(request):
    # print(request.user)
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


# def validate_emails(self):
#     print(self)
#     is_valid = False
#     count_of_dogs = 0
#     for email in self:
#         print(is_valid)
#         for char in email:
#             print(char)
#             if char == "@":
#                 is_valid = True
#                 count_of_dogs += 1
#         if count_of_dogs > 1:
#             is_valid = False
#             return is_valid
#         elif not is_valid:
#             is_valid = False
#             return is_valid
#         else:
#             count_of_dogs = 0
#             is_valid = False
#     return is_valid


def sent(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        title_mail = data['title']
        text = data['text_mail']
        mail_from = data['mail_from']
        mail_to_str = data['mail_to']
        mail_to_list = mail_to_str.split(',')
        try:
            send_mail(title_mail,text,mail_from,
                      mail_to_list,
                      fail_silently=False)
            return HttpResponse(status=201)
        except:
            raise ImportError
    else:
        return render(request, "send.html", {})
