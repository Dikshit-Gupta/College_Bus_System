from django.db import models

# Create your models here.
class ServiceTrip(models.Model):
    route = models.ForeignKey("transport.Route", on_delete=models.CASCADE, related_name="service_trips")
    trip_date = models.DateField()
    trip_type = models.CharField(max_length=20, choices=[("morning","Morning"),("evening","Evening"),("special","Special")])
    status = models.CharField(max_length=20, choices=[("scheduled","Scheduled"),("completed","Completed"),("cancelled","Cancelled")])
    created_at = models.DateTimeField(auto_now_add=True)

class TripBusAssignment(models.Model):
    service_trip = models.ForeignKey(ServiceTrip, on_delete=models.CASCADE, related_name="bus_assignments")
    bus = models.ForeignKey("transport.Bus", on_delete=models.CASCADE, related_name="trip_assignments")
    driver = models.ForeignKey("accounts.Driver", on_delete=models.CASCADE, related_name="trip_assignments")
    allocated_capacity = models.IntegerField()
    status = models.CharField(max_length=20, choices=[("assigned","Assigned"),("completed","Completed")])
    created_at = models.DateTimeField(auto_now_add=True)

class TravelConfirmation(models.Model):
    student = models.ForeignKey("accounts.Student", on_delete=models.CASCADE, related_name="travel_confirmations")
    service_trip = models.ForeignKey(ServiceTrip, on_delete=models.CASCADE, related_name="travel_confirmations")
    status = models.CharField(max_length=20, choices=[("pending","Pending"),("confirmed","Confirmed"),("declined","Declined"),("auto_confirmed","Auto Confirmed")])
    responded_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class StopChangeRequest(models.Model):
    student = models.ForeignKey("accounts.Student", on_delete=models.CASCADE, related_name="stop_change_requests")
    service_trip = models.ForeignKey(ServiceTrip, on_delete=models.CASCADE, related_name="stop_change_requests")
    from_stop = models.ForeignKey("transport.Stop", on_delete=models.CASCADE, related_name="from_stop_requests")
    requested_stop = models.ForeignKey("transport.Stop", on_delete=models.CASCADE, related_name="requested_stop_requests")
    status = models.CharField(max_length=20, choices=[("pending","Pending"),("approved","Approved"),("rejected","Rejected")])
    reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)