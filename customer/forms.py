from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from customer.models import Userprofile,Products,Productimages

class RegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=["username","email","password1","password2"]

class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField()

class EditProfileForm(forms.Form):
    class Meta:
        model=Userprofile
        fields=["pic","bio"]


class ProductForm(forms.Form):
    class Meta:
        model=Products
        fields=["name","description","condition","location","price"]

class ProductImageForm(forms.Form):
    class Meta:
        model=Productimages
        fields="__all__"

