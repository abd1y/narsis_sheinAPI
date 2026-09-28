from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
# Create your views here.
@api_view(["POST"])
@permission_classes([AllowAny])
def Login(req):
    username= req.data.get("username")
    Password= req.data.get("Password")
    authention=authenticate(username=username,password=Password)
    if  authention is None:
      return  Response({"error":"المعلومات المدخله خاطئ"}, status=402)
    token,created =Token.objects.get_or_create(user=authention)
    return Response({"Token":token.key}, status=200)