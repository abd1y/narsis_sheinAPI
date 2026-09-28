from django.urls import path
from . import views

urlpatterns = [
    path("get_invested/",views.get_invested),
    path('create_invested/',views.create_invested),
    path('delete_invested/',views.delete_invested)
]