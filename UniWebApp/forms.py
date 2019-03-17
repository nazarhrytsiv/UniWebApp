from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password


User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)
        if not qs.exists():
            raise forms.ValidationError("Your login is incorrect!")
        return username

    def clean_password(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.get(username=username)
        password = self.cleaned_data.get('password')
        # print(qs.check_password)
        if check_password(password, qs.password) == False:
            raise forms.ValidationError("Your password wrong!")
        else:
            return password


# TODO:validate for password

class RegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password',widget=forms.PasswordInput)

    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError("Password doesn`t match")

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username = username)
        if qs.exists():
            raise forms.ValidationError("Username already exist")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Email already exist")
        return email
