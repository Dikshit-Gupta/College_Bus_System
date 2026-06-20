from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import ServiceTrip, TripBusAssignment, TravelConfirmation, StopChangeRequest

admin.site.register(ServiceTrip)
admin.site.register(TripBusAssignment)
admin.site.register(TravelConfirmation)
admin.site.register(StopChangeRequest)
