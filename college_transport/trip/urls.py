from django.urls import path
from .views import TripListView

urlpatterns = [
    path("", TripListView.as_view(), name="trip_list"),
]