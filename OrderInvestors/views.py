from .models import orders_investors
from Orders.models import Orders
from Investors.models import investors
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
@api_view(['GET'])
@permission_classes([AllowAny])
def get_invested(req):
    orders=Orders.objects.all()
    all_investors=investors.objects.all()
    data_order=[]
    for order in orders:


        data_investors=[]
        order_invested = orders_investors.objects.filter(orders=order).first()
        
        if not order_invested:
               continue
        for investor in all_investors:
            invested=orders_investors.objects.filter(invester=investor,orders=order).first()
            if invested:
                status=invested.invested
                
            else:
                status=False
            data_investors.append({
                "InvestorsName":investor.InvestorsName,
                "invested":status
            })

        data_order.append({
                "id":order.id,
                "number_order":order.number_order,
                "invester_counted":order_invested.invester_counted,
                "CustomsTotal":order_invested.CustomsTotal,
                "profit_for_invester":order_invested.profit_for_invester,
                "invester":data_investors,
                
            })
    return Response({"data":data_order})
   
@api_view(['POST'])
@permission_classes([IsAuthenticated])   
def create_invested(req):
    number_order=req.data.get("number_order")
    selsect_invester=req.data.get("investors",[])
    order=Orders.objects.filter(number_order=number_order).first()
    if not order:
        return Response({"erorr":"رقم طلب غير موجود"})
    
    CustomsTotal=order.total_price_per_kg + order.total_delivery_price
    investerCounted=len(selsect_invester)
    existing_order =orders_investors.objects.filter(orders=order).exists()
    if existing_order:
        return Response({"erorr":"  طلب  مضاف سابقا"})
    
    all_investors=investors.objects.all()
    if investerCounted == 0:
        return Response({
            "erorr": "يجب اختيار مستثمر واحد على الأقل"
        })
    profit_for_invester = int(
        order.net_profit / investerCounted
    )
    for investor in all_investors:
        if investor.InvestorsUser in selsect_invester:
           status = True
           investor.profits += profit_for_invester
           investor.save()
        else: 
            status = False 
            

        orders_investors.objects.create(
                orders=order,
                invester=investor,
                CustomsTotal=CustomsTotal,
                invested=status,
                invester_counted=investerCounted,
                profit_for_invester=profit_for_invester
            )

        
    return Response({"Mesg":"تم اضافه التقسيمه بنجاح"})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])  
def delete_invested(req):
    id=req.data.get("id")
    order=Orders.objects.filter(id=id).first()
    if not order:
        return Response({"erorr":"التقسيمه غير موجوده"})
    orders_investors.objects.filter(orders=order).delete()
    
    return Response({"Mesg":"تم حذف التقسيمه بنجاح"})