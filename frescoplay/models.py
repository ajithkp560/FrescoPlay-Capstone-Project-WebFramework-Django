import datetime

from django.core.validators import EmailValidator
from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _

from frescoplay import settings
class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, firstname, lastname, password=None, my_photo=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, firstname=firstname, lastname=lastname, my_photo=my_photo, **extra_fields)
        user.set_password(password)
        user.save()
        return user

# def CustomUser(AbstractBaseUser):
#     email = models.EmailField(primary_key=True, max_length=50, validators=[EmailValidator()])
#     username = models.CharField(unique=True, max_length=50)
#     firstname = models.CharField(max_length=50)
#     lastname = models.CharField(max_length=50)
#     dob = models.DateField(null=True, blank=True)
#     my_photo = models.ImageField(upload_to='photos/', null=True, blank=True)
#
#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = [email, firstname, lastname, dob]
#
#     objects = CustomUserManager()
#
#     def __str__(self):
#         return self.email

class CustomUser(AbstractBaseUser):
    email = models.EmailField(_("email"), unique=True, max_length=50)
    username = models.CharField(unique=True, max_length=50)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    dob = models.DateField(null=True, blank=True)
    my_photo = models.ImageField(upload_to='photos/', null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [email, firstname, lastname, dob]

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    blog_photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    created_at = models.DateField(default=datetime.date.today)
    blogger = models.ForeignKey(settings.AUTH_USER_MODEL,   on_delete=models.CASCADE, related_name='blogs')