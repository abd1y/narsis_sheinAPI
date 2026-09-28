from django.db import models
from Orders.models import Orders
from Investors.models import investors
# Create your models here.

class orders_investors(models.Model):
    orders=models.ForeignKey(Orders,on_delete=models.CASCADE)
    invester=models.ForeignKey(investors,on_delete=models.CASCADE)
    CustomsTotal=models.IntegerField()
    invested = models.BooleanField(default=False)
    invester_counted=models.IntegerField(max_length=100)
    profit_for_invester=models.IntegerField()
    