from django.urls import path
from .views import BusCurrentLocationView, BusLocationListCreateView, DriverStopInfoView

urlpatterns = [
    path("trip/<int:trip_id>/locations/", BusLocationListCreateView.as_view(), name="bus_locations"),
    path("trip/<int:trip_id>/stops/", DriverStopInfoView.as_view(), name="driver_stop_info"),
    path("trip/<int:trip_id>/current-location/", BusCurrentLocationView.as_view(), name="bus_current_location"),
]