from django.urls import path
from . import views
urlpatterns = [
    path("getInvestors/",views.get_ALL_investors),
    path("crear_investors/",views.crear_investors),
    path("Remove_investors/",views.Remove_investors),
    path("Add_invested_money/",views.Add_invested_money),
    path("withdraw_invested_money/",views.withdraw_invested_money),
]