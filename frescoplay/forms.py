from attr.validators import max_len
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import validate_password
from django.forms import PasswordInput

from . import settings
from .models import CustomUser


# class CustomUserCreationForm(UserCreationForm):
#     class Meta:
#         model = CustomUser
#         fields = ('email', 'username', 'firstname', 'lastname', 'dob', 'my_photo')
#
#     password1 = forms.CharField(
#         label="Password",
#         widget=forms.PasswordInput(attrs={'class': 'form-control'}),
#     )
#     password2 = forms.CharField(
#         label="Confirm Password",
#         widget=forms.PasswordInput(attrs={'class': 'form-control'}),
#     )
#
#
#     def clean(self):
#         cleaned_data = super().clean()
#         password1 = cleaned_data.get('password1')
#         password2 = cleaned_data.get('password2')
#
#         if password1 != password2:
#             raise forms.ValidationError("Passwords do not match")
#
#         return cleaned_data
#

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser

class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(max_length=50, widget=PasswordInput(), required=True)
    confirm = forms.CharField(max_length=50, widget=PasswordInput(), required=True)
    dob = forms.DateField(required=True, widget=forms.DateInput(attrs={'type':'date'}))
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'firstname', 'lastname', 'dob', 'my_photo')

    def clean_password(self):
        # Custom password validation using Django's built-in password validators
        password = self.cleaned_data.get("password")
        if password:
            validate_password(password, self.instance)  # Use Django's password validators
        return password

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('confirm')

        if password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class loginForm(forms.Form):
    username = forms.CharField(max_length=50, required=True)
    password = forms.CharField(max_length=50, widget=PasswordInput(), required=True)

class createBlog(forms.Form):
    title = forms.CharField(max_length=200, required=True)
    content = forms.CharField(max_length=1500, required=True)
    blog_photo = forms.ImageField(required=False)
    created_at = forms.DateTimeField(required=True)