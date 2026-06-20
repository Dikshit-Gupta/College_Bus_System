from rest_framework import serializers

from booking.models import Booking
from .models import BusLocation


class BusLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusLocation
        fields = ["id", "trip_bus_assignment", "latitude", "longitude", "speed", "recorded_at"]
    
    def get_students(self, obj):
        # Get all bookings for this trip assignment
        bookings = Booking.objects.filter(trip_bus_assignment=obj.trip_bus_assignment, status="booked")
        return [
            {
                "student_id": b.student.id,
                "seat_id": b.seat.id,
                "stop": b.seat.stop.name if hasattr(b.seat, "stop") else None
            }
            for b in bookings
        ]