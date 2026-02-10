import React, { useEffect, useRef } from 'react';
import { MapContainer, TileLayer, Marker, useMapEvents, useMap } from 'react-leaflet';
import { Map } from 'lucide-react';
import L from 'leaflet';

// Fix for default marker icon
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
});

function MapClickHandler({ onLocationSelect }) {
  useMapEvents({
    click: (e) => {
      onLocationSelect(e.latlng.lat, e.latlng.lng);
    },
  });
  return null;
}

function MapUpdater({ lat, lng }) {
  const map = useMap();
  const prevCoordsRef = useRef({ lat: null, lng: null });

  useEffect(() => {
    if (lat !== null && lng !== null) {
      // Only pan if coordinates changed significantly (not just rounding)
      const prevLat = prevCoordsRef.current.lat;
      const prevLng = prevCoordsRef.current.lng;

      if (prevLat === null || prevLng === null ||
          Math.abs(lat - prevLat) > 0.0001 || Math.abs(lng - prevLng) > 0.0001) {
        map.setView([lat, lng], map.getZoom(), { animate: true });
        prevCoordsRef.current = { lat, lng };
      }
    }
  }, [lat, lng, map]);

  return null;
}

export function MapPicker({ lat, lng, onCoordinatesChange }) {
  const defaultLat = lat ?? 25.2770;
  const defaultLng = lng ?? 55.2962;

  const handleLocationSelect = (newLat, newLng) => {
    onCoordinatesChange(newLat, newLng);
  };

  return (
    <div className="bg-white dark:bg-nav-dark-card rounded-lg p-4 shadow-md">
      <div className="flex items-center gap-2 mb-3">
        <Map className="w-5 h-5 text-accent-tide dark:text-accent-tide-dark" />
        <h3 className="font-semibold text-nav-text dark:text-nav-dark-text">Map Selection</h3>
      </div>

      <div className="h-64 rounded-lg overflow-hidden border border-gray-200 dark:border-gray-700">
        <MapContainer
          center={[defaultLat, defaultLng]}
          zoom={4}
          scrollWheelZoom={true}
          className="h-full w-full"
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          <MapClickHandler onLocationSelect={handleLocationSelect} />
          <MapUpdater lat={lat} lng={lng} />
          {lat !== null && lng !== null && (
            <Marker position={[lat, lng]} />
          )}
        </MapContainer>
      </div>

      <p className="mt-2 text-xs text-gray-500 dark:text-gray-400">
        Click on the map to select a location
      </p>
    </div>
  );
}
