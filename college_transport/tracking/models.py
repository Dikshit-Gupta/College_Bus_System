from django.db import models

# Create your models here.
class BusLocation(models.Model):
    trip_bus_assignment = models.ForeignKey("trip.TripBusAssignment", on_delete=models.CASCADE, related_name="bus_locations")
    latitude = models.FloatField()
    longitude = models.FloatField()
    speed = models.FloatField(blank=True, null=True)
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.trip_bus_assignment.bus.bus_number} @ {self.latitude}, {self.longitude}"