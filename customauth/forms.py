from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

from .models import CustomUser
# User = get_user_model()


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = CustomUser.objects.filter(email=email)

        print("heeeffe")
        if not qs.exists():
            print("heeee")
            raise forms.ValidationError("Your login is incorrect!")
        return email

    def clean_password(self):
        email = self.cleaned_data.get('email')
        try:
            qs = CustomUser.objects.get(email=email)
            password = self.cleaned_data.get('password')

            if check_password(password, qs.password) == False:
                raise forms.ValidationError("Your password wrong!")
            else:
                return password
        except:
            raise forms.ValidationError("Your Email is does not exists")



# TODO:validate for password

class RegisterForm(forms.Form):
    # username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password',widget=forms.PasswordInput)

    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError("Password doesn`t match")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = CustomUser.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Email already exist")
        return email