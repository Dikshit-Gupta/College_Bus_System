from rest_framework import serializers
from .models import ServiceTrip

class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceTrip
        fields = ["id", "bus", "route", "date", "departure_time", "arrival_time"]