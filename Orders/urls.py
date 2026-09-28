from django.urls import path
from . import views
urlpatterns = [
    path("get_order/",views.get_Order),
    path("create_order/",views.create_order),
    path("delete_order/",views.delete_order),
    path("ubdate_order/",views.ubdate_order),
    
]