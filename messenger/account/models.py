from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

# from main import models as main

"""
User
"""
class UserProfileManager(BaseUserManager):

    def create_user(self, username, first_name, last_name, email, password = None):
        user = self.model(first_name = first_name, last_name = last_name , username = username, email=email)
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self, username, first_name, last_name, email , password = None):

        user = self.create_user(username, first_name, last_name, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using = self._db)
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    username =  models.CharField(max_length = 12, unique = True)
    first_name = models.CharField(max_length = 50, blank = True, null = True)
    last_name = models.CharField(max_length = 50, blank = True, null = True)
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(default = timezone.now)
    image = models.ImageField(blank=True, null=True, upload_to="accounts/images/")
    
    userid = models.CharField(blank=True, null=True, max_length=50, unique=True)

    username_public = models.BooleanField(default=False)
    email_public = models.BooleanField(default=False)
    image_public = models.BooleanField(default=True)

    is_active = models.BooleanField(default = True, verbose_name = "فعال")
    is_staff = models.BooleanField( default = False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']


    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)
