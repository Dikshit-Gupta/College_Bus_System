import React, { useState, useEffect, useRef } from "react";
import { Image, View, Text } from "react-native";
import MapView, { Marker, UrlTile, Polyline } from "react-native-maps";

export default function App() {
  const [busLocation, setBusLocation] = useState(null);
  const [stops, setStops] = useState([]);
  const [eta, setEta] = useState(null);
  const mapRef = useRef(null);

  const API = "http://192.168.1.5:8000"; // Replace with your computer IP

  // Helper: calculate distance (Haversine formula)
  function getDistance(lat1, lon1, lat2, lon2) {
    const R = 6371; // km
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;
    const a =
      Math.sin(dLat/2) * Math.sin(dLat/2) +
      Math.cos(lat1 * Math.PI/180) * Math.cos(lat2 * Math.PI/180) *
      Math.sin(dLon/2) * Math.sin(dLon/2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    return R * c; // distance in km
  }

  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const res = await fetch(`${API}/api/tracking/trip/1/current-location/`);
        const data = await res.json();
        if (data.latitude && data.longitude) {
          setBusLocation(data);

          // Auto-follow bus
          mapRef.current?.animateToRegion({
            latitude: data.latitude,
            longitude: data.longitude,
            latitudeDelta: 0.01,
            longitudeDelta: 0.01,
          });

          // Calculate ETA to first stop
          if (stops.length > 0 && data.speed > 0) {
            const nextStop = stops[0];
            const dist = getDistance(
              data.latitude, data.longitude,
              nextStop.latitude, nextStop.longitude
            );
            const timeHours = dist / (data.speed / 60); // speed in km/h → minutes
            setEta(Math.round(timeHours)); // ETA in minutes
          }
        }
      } catch (error) {
        console.log("Error fetching bus location:", error);
      }
    }, 5000);

    (async () => {
      try {
        const res = await fetch(`${API}/api/tracking/trip/1/stops/`);
        const data = await res.json();
        setStops(data);
      } catch (error) {
        console.log("Error fetching stops:", error);
      }
    })();

    return () => clearInterval(interval);
  }, [stops]);

  return (
    <View style={{ flex: 1 }}>
      <MapView
        ref={mapRef}
        style={{ flex: 1 }}
        provider={null}
        initialRegion={{
          latitude: 23.2599,
          longitude: 77.4126,
          latitudeDelta: 0.05,
          longitudeDelta: 0.05,
        }}
      >
        <UrlTile
          urlTemplate="https://tile.openstreetmap.org/{z}/{x}/{y}.png"
          maximumZ={19}
        />

        {/* Bus marker */}
        {busLocation && (
          <Marker
            coordinate={{
              latitude: busLocation.latitude,
              longitude: busLocation.longitude,
            }}
            title="Bus Location"
          >
            <Image
              source={require("./assets/bus.png")}
              style={{ width: 40, height: 40 }}
              resizeMode="contain"
            />
          </Marker>
        )}

        {/* Stop markers */}
        {stops.map((stop, idx) => (
          <Marker
            key={idx}
            coordinate={{
              latitude: stop.latitude,
              longitude: stop.longitude,
            }}
            title={stop.stop}
            description={`${stop.student_count} students`}
          >
            <Image
              source={require("./assets/stop.png")}
              style={{ width: 30, height: 30 }}
              resizeMode="contain"
            />
          </Marker>
        ))}

        {/* Route line */}
        {stops.length > 1 && (
          <Polyline
            coordinates={stops.map(stop => ({
              latitude: stop.latitude,
              longitude: stop.longitude,
            }))}
            strokeColor="#0000FF"
            strokeWidth={4}
          />
        )}
      </MapView>

      {/* Speed + ETA display */}
      {busLocation && (
        <View style={{ padding: 10, backgroundColor: "white" }}>
          <Text>Speed: {busLocation.speed} km/h</Text>
          {eta && <Text>ETA to next stop: {eta} minutes</Text>}
        </View>
      )}
    </View>
  );
}