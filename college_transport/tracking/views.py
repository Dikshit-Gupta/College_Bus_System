from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import BusLocation
from .serializers import BusLocationSerializer
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from booking.models import Booking

class BusLocationListCreateView(generics.ListCreateAPIView):
    queryset = BusLocation.objects.all()
    serializer_class = BusLocationSerializer
    permission_classes = [IsAuthenticated]  

    def get_queryset(self):
        user = self.request.user
        student_profile = getattr(user, "student_profile", None)
        if student_profile is None:
            return BusLocation.objects.none()

        trip_id = self.kwargs.get("trip_id")
        return BusLocation.objects.filter(
            trip_bus_assignment__pk=trip_id,
            trip_bus_assignment__bookings__student=student_profile,
        ).distinct()

class BusCurrentLocationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, trip_id):
        # Get the most recent bus location for this trip
        location = BusLocation.objects.filter(
            trip_bus_assignment__pk=trip_id
        ).order_by("-recorded_at").first()

        if location:
            return Response({
                "latitude": location.latitude,
                "longitude": location.longitude,
                "speed": location.speed,
                "timestamp": location.recorded_at
            })
        return Response({"message": "No location data yet"})

class DriverStopInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, trip_id):
        # Define seat ranges mapped to stops
        stop_mapping = {
            "Stop A": range(1, 11),
            "Stop B": range(11, 21),
            "Stop C": range(21, 31),
        }

        result = []
        for stop_name, seat_range in stop_mapping.items():
            count = Booking.objects.filter(
                trip_bus_assignment__pk=trip_id,
                seat_id__in=seat_range,
                status="booked"
            ).count()
            result.append({"stop": stop_name, "student_count": count})

        return Response(result)