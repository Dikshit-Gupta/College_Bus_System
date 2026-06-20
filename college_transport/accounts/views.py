from django.shortcuts import render

# Create your views here.

# now here we have all the users 
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView
)

# Login → returns access + refresh token
class LoginView(TokenObtainPairView):
    pass

# Refresh → returns new access token
class RefreshView(TokenRefreshView):
    pass

# Logout → blacklists refresh token
class LogoutView(TokenBlacklistView):
    pass


from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializer import RegisterSerializer
from .models import User

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]  # allow anyone to register
    serializer_class = RegisterSerializer