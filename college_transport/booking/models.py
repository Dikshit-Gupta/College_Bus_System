from django.db import models

# Create your models here.
class Booking(models.Model):
    student = models.ForeignKey("accounts.Student", on_delete=models.CASCADE, related_name="bookings")
    trip_bus_assignment = models.ForeignKey("trip.TripBusAssignment", on_delete=models.CASCADE, related_name="bookings")
    seat = models.ForeignKey("transport.Seat", on_delete=models.CASCADE, related_name="bookings")
    status = models.CharField(max_length=20, choices=[("allocated","Allocated"),("cancelled","Cancelled")])
    allocated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.enrollment_no} → {self.seat.seat_number} ({self.trip_bus_assignment.service_trip.trip_type})"