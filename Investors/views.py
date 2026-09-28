from .models import investors
from OrderInvestors.models import orders_investors
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
# Create your views here.
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_ALL_investors(req):
    ALL_Investors=investors.objects.all()
    
    data=[]
    for Investors in ALL_Investors:
        invested_orders =orders_investors.objects.filter(invester=Investors,invested=True)
        
        Customs=Investors.Customs
        for orders_investor in invested_orders:
            Customs+=orders_investor.CustomsTotal
        data.append({
            "id":Investors.id,
            "InvestorsName":Investors.InvestorsName,
            "InvestorsUser":Investors.InvestorsUser,
            "profits":Investors.profits,
            "Customs":Customs,
            "Withdrawn":Investors.Withdrawn,
            "investedMone":Investors.investedMone,
        })
    return Response({
        "Investors":data
    })

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def crear_investors(req):
        InvestorsName=req.data.get("InvestorsName")
        InvestorsUser=req.data.get("InvestorsUser")
        investedMone=req.data.get("investedMone")
        Customs = req.data.get("Customs", 0)
        if not InvestorsName or not InvestorsUser or not investedMone:
            return Response({"erorr":"الحقول فارغه مطلوبه"},status=400)
        
        userName=investors.objects.filter(InvestorsUser=InvestorsUser).first()
        if userName:
            return Response({"erorr":"اسم المستخدم موجود بالفعل"},status=400)
        if investedMone <1999 :
            return Response({"erorr":"يجب ان يكون مبلغ مستثمر   20,000 او اكثر"},status=400)
        if Customs <0:
            return Response({"erorr":"يجب ان تكون مدفوعات كمركيه قيمه موجبه"},status=400)
        Investor=investors.objects.create(
            InvestorsName=InvestorsName,
            InvestorsUser=InvestorsUser,
            investedMone=investedMone,
            Customs=Customs,
    )
        return Response({"Investor":{
               "id": Investor.id,
            "InvestorsName": Investor.InvestorsName,
            "InvestorsUser": Investor.InvestorsUser,
            "profits":Investor.profits,
            "Customs": Investor.Customs,
            "Withdrawn":Investor.Withdrawn,
            "investedMone": Investor.investedMone,
        }})
        
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])        
def Remove_investors(req):
    id=req.data.get("id")
    investor=investors.objects.filter(id=id).first()
    if not investor:
        return Response({"Mes":"لا يوجد مستخدم "},status=400)
    
    investor.delete()
    return Response({"Mes":"تم حذف المستثمر بنجاح"},status=200)

@api_view(["POST"])
@permission_classes([IsAuthenticated])    
def Add_invested_money(req):
    id=req.data.get("id")
    amount=req.data.get("amount")
    investor=investors.objects.filter(id=id).first()
    if not investor:
        return Response({"erorr":"المستثمر غير موجود"},status=400)
    if not amount:
        return Response({"erorr":"يرجى ادخال المبلغ المراد ايداعه"},status=400)
    if amount <0:
        return Response({"erorr":"يرجى ايداع مبلغ بالموجب"},status=400)
    investor.investedMone+=amount
    investor.save()
    return Response({
        "Mes":"تم ايداع المبلع بنجاح",
        "investedMone":investor.investedMone
    })
    
@api_view(["POST"])
@permission_classes([IsAuthenticated])    
def withdraw_invested_money(req):
    id=req.data.get("id")
    amount=req.data.get("amount")
    investor=investors.objects.filter(id=id).first()
    if not investor:
        return Response({"erorr":"المستثمر غير موجود"},status=400)
    if not amount:
        return Response({"erorr":"يرجى ادخال المبلغ المراد سحبه"},status=400)
    if amount <= 999:
        return Response({
            "erorr": "اقل مبلغ للسحب هو 1,000 دينار "
        }, status=400)
    if investor.profits < amount:
        remaining=amount - investor.profits
        investor.profits=0
        if remaining > investor.investedMone:
            return Response({ "erorr": "المبلغ المطلوب أكبر من رصيد المستثمر"},status=400)
        investor.investedMone-=remaining
    else:
        investor.profits-=amount
    investor.Withdrawn+=amount 
    investor.save()
    return Response({
        "Mes":f"{amount } تم سحب مبلغ ",
        "investedMone": investor.investedMone,
        "Withdrawn":investor.Withdrawn,
        "profits":investor.profits
    })