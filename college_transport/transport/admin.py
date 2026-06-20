from django.contrib import admin

# Register your models here.
from .models import Route, Stop, StudentRouteAssignment, Bus, Seat

admin.site.register(Route)
admin.site.register(Stop)
admin.site.register(StudentRouteAssignment)
admin.site.register(Bus)
admin.site.register(Seat)