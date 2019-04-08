from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import IntegrityError
from  django.contrib.auth.models import PermissionsMixin

# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_superuser(self, email,password):
        user = CustomUser()
        user.email = email
        user.set_password(password)
        try:
            user.is_staff = True
            user.is_active = True
            user.is_superuser = True
            user.save()
            return user
        except (ValueError, IntegrityError):
            pass


class CustomUser(AbstractBaseUser, PermissionsMixin):
    # username = models.CharField()
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    password2 = models.CharField(max_length=128)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField( default=True)

    USERNAME_FIELD = 'email'
    objects = CustomUserManager()

    @staticmethod
    def create_user(email, password):
        user = CustomUser()
        user.email = email
        user.set_password(password)
        try:
            user.save()
            return user
        except (ValueError, IntegrityError):
            pass




