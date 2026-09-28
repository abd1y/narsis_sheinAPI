from django.db import models

# Create your models here.
class Orders(models.Model):
    number_order=models.IntegerField() # رقم طلب
    order_data=models.DateField() # تاريخ طلب
    Customer_name=models.CharField(blank=False) # اسم زبون
    customer_deposit=models.IntegerField(blank=False)  # عموله الي يدزها عميل
    selling_price=models.IntegerField(blank=False) # سعر معروض للعميل
    cost_price=models.IntegerField(blank=False) # سعر الاصلي
    order_size=models.IntegerField(blank=False) # حجم طلب ب kg
    price_per_km=models.IntegerField(blank=False) # سعر لكل kg
    total_price_per_kg=models.IntegerField(blank=False) # مجموع سعر كامل 
    total_delivery_price=models.IntegerField(blank=False) # سعر توصيل كامل 
    delivery_price=models.IntegerField(blank=False,default=0)# سعر توصيل لزبون
    net_profit=models.IntegerField(blank=False) # الارباح صافيه
    order_total=models.IntegerField(blank=False) #  سعر طلب الاجمالي الي يوصل لبيت زبون
    
    