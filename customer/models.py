from django.db import models
from django.contrib.auth.models import User



class Userprofile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    pic=models.ImageField(upload_to="profilepics",null=True)
    bio=models.CharField(max_length=200,null=True)

class Categories(models.Model):
    name=models.CharField(max_length=100)
    isactive=models.BooleanField(default=True)

class Products(models.Model):
    name=models.CharField(max_length=200)
    owner=models.ForeignKey(User,on_delete=models.CASCADE)
    description=models.CharField(max_length=200)
    condition=models.CharField(max_length=200,null=True)
    category=models.ForeignKey(Categories,on_delete=models.CASCADE)
    location=models.CharField(max_length=200)
    price=models.PositiveIntegerField()
    options=(
        ("for-sale","for-sale"),
        ("exchange","exchange"),
        ("sold","sold"), 
        ("rent","rent"),
    )

    status=models.CharField(max_length=200,choices=options,default="for-sale")
    date=models.DateTimeField(auto_now_add=True)

class Productimages(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    image=models.ImageField(upload_to="productimg",null=True)
