from django.db import models

# Create your models here.
class Route(models.Model):
    route_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.route_name

class Stop(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="stops")
    stop_name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    stop_order = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.stop_name} ({self.route.route_name})"

class StudentRouteAssignment(models.Model):
    student = models.ForeignKey("accounts.Student", on_delete=models.CASCADE, related_name="route_assignments")
    stop = models.ForeignKey(Stop, on_delete=models.CASCADE, related_name="student_assignments")
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Bus(models.Model):
    bus_number = models.CharField(max_length=20, unique=True)
    registration_number = models.CharField(max_length=50, unique=True)
    capacity = models.IntegerField()
    status = models.CharField(max_length=20, choices=[("active","Active"),("inactive","Inactive")])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bus {self.bus_number} ({self.capacity} seats)"

class Seat(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name="seats")
    seat_number = models.CharField(max_length=10)
    seat_type = models.CharField(max_length=20, choices=[("regular","Regular"),("reserved","Reserved")])
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.bus.bus_number} - Seat {self.seat_number}"