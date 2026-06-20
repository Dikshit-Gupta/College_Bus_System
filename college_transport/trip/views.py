from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import ServiceTrip
from .serializer import TripSerializer

class TripListView(generics.ListAPIView):
    queryset = ServiceTrip.objects.all()
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated]  # ✅ only logged-in users can access