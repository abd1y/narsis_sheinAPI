from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import Orders
from django.db.models import F
from django.utils import timezone
# Create your views here.
@api_view(["GET"])
@permission_classes([AllowAny])
def get_Order(req):
    order=Orders.objects.all().values()
    return Response({
        "orders":order
    })
 
@api_view(["POST"])
@permission_classes([IsAuthenticated])    
def create_order(req): 
    selling_price=req.data.get("selling_price")
    cost_price=req.data.get("cost_price")
    price_per_km=req.data.get("price_per_km")
    total_delivery_price=req.data.get("total_delivery_price")
    delivery_price=req.data.get("delivery_price", 5000)
    customer_deposit=req.data.get("customer_deposit")
    order_size=req.data.get("order_size")
    
    total_price_per_kg=price_per_km * order_size
    net_profit=selling_price - cost_price - total_price_per_kg - total_delivery_price
    order_total=selling_price + delivery_price - customer_deposit
    last_order=Orders.objects.order_by("-number_order").first()
    
    if last_order:
        numberOrder = last_order.number_order + 1
    else:
        numberOrder = 1
        
    order=Orders.objects.create(
        number_order=numberOrder,
        order_data=timezone.now().date(),
        Customer_name=req.data.get("Customer_name"),
        customer_deposit=customer_deposit,
        selling_price=selling_price,
        cost_price=cost_price,
        order_size=order_size,
        price_per_km=price_per_km,
        total_price_per_kg=total_price_per_kg,
        total_delivery_price=total_delivery_price,
        delivery_price=delivery_price,
          net_profit=net_profit,
    order_total=order_total,
    )
    return Response({
        "id":order.id,
        "number_order":order.number_order,
        "Customer_name":order.Customer_name,
        "customer_deposit":order.customer_deposit,
        "selling_price":order.selling_price,
        "cost_price":order.cost_price,
        "order_size":order.order_size,
        "price_per_km":order.price_per_km,
        "total_price_per_kg":order.total_price_per_kg,
        "total_delivery_price":order.total_delivery_price,
        "delivery_price":order.delivery_price,
        "net_profit":order.net_profit,
        "order_total":order.order_total
        
    })
    
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])  
def delete_order(req):
    id=req.data.get('id')
    order=Orders.objects.filter(id=id).first()
    if not order:
        return Response({
            "erorr":"الطلب غير موجود"
        })
    delete_number_order = order.number_order
    order.delete()
    Orders.objects.filter(number_order__gt=delete_number_order).update(
        number_order=F("number_order") -1
    )
    return Response({
        "Mes":"تم حذف الطلب"
    })
 
@api_view(["PUT"])
@permission_classes([IsAuthenticated])  
def ubdate_order(req):
    id=req.data.get('id')
    order=Orders.objects.filter(id=id).first()
    if not order:
        return Response({
            "erorr":"الطلب غير موجود"
        })
    for keys,value in req.data.items():
        if keys !="id"  and keys !="number_order":
            setattr(order,keys,value)
    order.save()
    return Response({
        "Msg":"تم تحديث بيانات "
    })