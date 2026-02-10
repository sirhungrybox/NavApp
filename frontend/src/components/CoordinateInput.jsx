import React, { useState } from 'react';
import { MapPin, Navigation, Loader2 } from 'lucide-react';
import { parseCoordinate, formatCoordinate } from '../utils/formatters';
import { useGeolocation } from '../hooks/useGeolocation';

export function CoordinateInput({ lat, lng, onCoordinatesChange }) {
  const [latInput, setLatInput] = useState(lat?.toFixed(6) || '');
  const [lngInput, setLngInput] = useState(lng?.toFixed(6) || '');
  const { getLocation, loading: gpsLoading, error: gpsError } = useGeolocation();

  const handleLatChange = (e) => {
    setLatInput(e.target.value);
    const parsed = parseCoordinate(e.target.value);
    if (parsed !== null && parsed >= -90 && parsed <= 90) {
      onCoordinatesChange(parsed, lng);
    }
  };

  const handleLngChange = (e) => {
    setLngInput(e.target.value);
    const parsed = parseCoordinate(e.target.value);
    if (parsed !== null && parsed >= -180 && parsed <= 180) {
      onCoordinatesChange(lat, parsed);
    }
  };

  const handleLatBlur = () => {
    if (lat !== null) {
      setLatInput(lat.toFixed(6));
    }
  };

  const handleLngBlur = () => {
    if (lng !== null) {
      setLngInput(lng.toFixed(6));
    }
  };

  const handleGpsClick = async () => {
    try {
      const coords = await getLocation();
      setLatInput(coords.lat.toFixed(6));
      setLngInput(coords.lng.toFixed(6));
      onCoordinatesChange(coords.lat, coords.lng);
    } catch (err) {
      console.error('GPS error:', err);
    }
  };

  return (
    <div className="bg-white dark:bg-nav-dark-card rounded-lg p-4 shadow-md">
      <div className="flex items-center gap-2 mb-3">
        <MapPin className="w-5 h-5 text-accent-sun dark:text-accent-sun-dark" />
        <h3 className="font-semibold text-nav-text dark:text-nav-dark-text">Position</h3>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        <div>
          <label className="block text-sm text-gray-600 dark:text-gray-400 mb-1">
            Latitude
          </label>
          <input
            type="text"
            value={latInput}
            onChange={handleLatChange}
            onBlur={handleLatBlur}
            placeholder={'25.2770 or 25° 16\' 37" N'}
            className="w-full px-3 py-2 rounded-md border border-gray-300 dark:border-gray-600
                       bg-white dark:bg-gray-800 text-nav-text dark:text-nav-dark-text
                       focus:ring-2 focus:ring-accent-sun dark:focus:ring-accent-sun-dark outline-none"
          />
          {lat !== null && (
            <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
              {formatCoordinate(lat, 'lat')}
            </p>
          )}
        </div>

        <div>
          <label className="block text-sm text-gray-600 dark:text-gray-400 mb-1">
            Longitude
          </label>
          <input
            type="text"
            value={lngInput}
            onChange={handleLngChange}
            onBlur={handleLngBlur}
            placeholder={'55.2962 or 55° 17\' 46" E'}
            className="w-full px-3 py-2 rounded-md border border-gray-300 dark:border-gray-600
                       bg-white dark:bg-gray-800 text-nav-text dark:text-nav-dark-text
                       focus:ring-2 focus:ring-accent-sun dark:focus:ring-accent-sun-dark outline-none"
          />
          {lng !== null && (
            <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
              {formatCoordinate(lng, 'lng')}
            </p>
          )}
        </div>
      </div>

      <button
        onClick={handleGpsClick}
        disabled={gpsLoading}
        className="mt-3 w-full flex items-center justify-center gap-2 px-4 py-2
                   bg-accent-sun dark:bg-accent-sun-dark text-white rounded-md
                   hover:opacity-90 transition-opacity disabled:opacity-50 min-h-[44px]"
      >
        {gpsLoading ? (
          <>
            <Loader2 className="w-5 h-5 animate-spin" />
            Getting Location...
          </>
        ) : (
          <>
            <Navigation className="w-5 h-5" />
            Use GPS Location
          </>
        )}
      </button>

      {gpsError && (
        <p className="mt-2 text-sm text-red-500 dark:text-red-400">{gpsError}</p>
      )}
    </div>
  );
}
