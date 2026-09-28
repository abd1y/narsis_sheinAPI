from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Authention(models.Model):
    user= models.OneToOneField(User,on_delete=models.CASCADE)
    userName=models.CharField(max_length=10,blank=False)
    Password=models.CharField(blank=False)