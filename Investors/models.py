from django.db import models

# Create your models here.
class investors(models.Model):
    InvestorsName=models.CharField(blank=False,max_length=50)
    InvestorsUser=models.CharField(blank=False,max_length=10,unique=True)
    profits=models.IntegerField(default=0)
    Customs=models.IntegerField(default=0)
    Withdrawn=models.IntegerField(default=0)
    investedMone=models.IntegerField(blank=False)
    