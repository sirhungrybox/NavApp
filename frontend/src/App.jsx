import React, { useState, useEffect } from 'react';
import { format } from 'date-fns';
import { Compass, RefreshCw, MapPin } from 'lucide-react';

import { CoordinateInput } from './components/CoordinateInput';
import { MapPicker } from './components/MapPicker';
import { DatePicker } from './components/DatePicker';
import { SunCard } from './components/SunCard';
import { MoonCard } from './components/MoonCard';
import { PrayerCard } from './components/PrayerCard';
import { TideCard } from './components/TideCard';
import { WeatherCard } from './components/WeatherCard';
import { DarkModeToggle } from './components/DarkModeToggle';
import { LoadingSpinner } from './components/LoadingSpinner';
import { ErrorMessage } from './components/ErrorMessage';
import { useNavData } from './hooks/useNavData';
import { formatCoordinate } from './utils/formatters';

function App() {
  // Load saved preferences
  const [isDarkMode, setIsDarkMode] = useState(() => {
    const saved = localStorage.getItem('navapp-darkmode');
    return saved !== null ? JSON.parse(saved) : true; // Default to dark mode
  });

  const [lat, setLat] = useState(() => {
    const saved = localStorage.getItem('navapp-lat');
    return saved !== null ? parseFloat(saved) : 25.2770;
  });

  const [lng, setLng] = useState(() => {
    const saved = localStorage.getItem('navapp-lng');
    return saved !== null ? parseFloat(saved) : 55.2962;
  });

  const [date, setDate] = useState(() => format(new Date(), 'yyyy-MM-dd'));

  const [prayerMethod, setPrayerMethod] = useState(() => {
    const saved = localStorage.getItem('navapp-prayer-method');
    return saved || 'muslim_world_league';
  });

  const [showMap, setShowMap] = useState(false);

  // Fetch navigation data
  const { data, loading, error, refetch } = useNavData(lat, lng, date, prayerMethod);

  // Apply dark mode
  useEffect(() => {
    if (isDarkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
    localStorage.setItem('navapp-darkmode', JSON.stringify(isDarkMode));
  }, [isDarkMode]);

  // Save coordinates
  useEffect(() => {
    if (lat !== null) localStorage.setItem('navapp-lat', lat.toString());
    if (lng !== null) localStorage.setItem('navapp-lng', lng.toString());
  }, [lat, lng]);

  // Save prayer method
  useEffect(() => {
    localStorage.setItem('navapp-prayer-method', prayerMethod);
  }, [prayerMethod]);

  const handleCoordinatesChange = (newLat, newLng) => {
    setLat(newLat);
    setLng(newLng);
  };

  const toggleDarkMode = () => {
    setIsDarkMode(prev => !prev);
  };

  return (
    <div className="min-h-screen bg-nav-bg dark:bg-nav-dark-bg transition-colors">
      {/* Header */}
      <header className="bg-white dark:bg-nav-dark-card shadow-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 py-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Compass className="w-8 h-8 text-accent-sun dark:text-accent-sun-dark" />
              <div>
                <h1 className="text-xl font-bold text-nav-text dark:text-nav-dark-text">
                  NavApp
                </h1>
                <p className="text-xs text-gray-500 dark:text-gray-400">
                  Ocean Navigator
                </p>
              </div>
            </div>

            <div className="flex items-center gap-3">
              {/* Current Position Display */}
              {lat !== null && lng !== null && (
                <div className="hidden md:flex items-center gap-2 px-3 py-1 bg-gray-100 dark:bg-gray-700 rounded-full">
                  <MapPin className="w-4 h-4 text-accent-sun dark:text-accent-sun-dark" />
                  <span className="text-sm text-nav-text dark:text-nav-dark-text">
                    {lat.toFixed(4)}°, {lng.toFixed(4)}°
                  </span>
                </div>
              )}

              {/* Refresh Button */}
              <button
                onClick={refetch}
                disabled={loading}
                className="p-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-700
                           text-nav-text dark:text-nav-dark-text
                           disabled:opacity-50 min-w-[44px] min-h-[44px]
                           flex items-center justify-center"
                aria-label="Refresh data"
              >
                <RefreshCw className={`w-5 h-5 ${loading ? 'animate-spin' : ''}`} />
              </button>

              <DarkModeToggle isDark={isDarkMode} onToggle={toggleDarkMode} />
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-6">
        {/* Input Section */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-6">
          <CoordinateInput
            lat={lat}
            lng={lng}
            onCoordinatesChange={handleCoordinatesChange}
          />

          <DatePicker
            date={date}
            onDateChange={setDate}
          />

          {/* Map Toggle for Mobile */}
          <div className="lg:hidden">
            <button
              onClick={() => setShowMap(!showMap)}
              className="w-full px-4 py-3 bg-white dark:bg-nav-dark-card rounded-lg shadow-md
                         text-nav-text dark:text-nav-dark-text font-medium
                         flex items-center justify-center gap-2"
            >
              <MapPin className="w-5 h-5" />
              {showMap ? 'Hide Map' : 'Show Map'}
            </button>
          </div>

          <div className={`${showMap ? 'block' : 'hidden'} lg:block`}>
            <MapPicker
              lat={lat}
              lng={lng}
              onCoordinatesChange={handleCoordinatesChange}
            />
          </div>
        </div>

        {/* Data Section */}
        {loading && !data && <LoadingSpinner />}

        {error && !data && (
          <ErrorMessage message={error} onRetry={refetch} />
        )}

        {data && (
          <>
            {/* Timezone Info */}
            <div className="mb-4 text-center">
              <span className="text-sm text-gray-500 dark:text-gray-400">
                Timezone: {data.timezone}
              </span>
              {loading && (
                <span className="ml-2 text-xs text-accent-sun dark:text-accent-sun-dark">
                  Updating...
                </span>
              )}
            </div>

            {/* Dashboard Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <SunCard data={data.solar} />
              <MoonCard data={data.lunar} />
              <PrayerCard
                data={data.prayer}
                method={prayerMethod}
                onMethodChange={setPrayerMethod}
              />
              <TideCard data={data.tides} />
              <div className="md:col-span-2">
                <WeatherCard data={data.weather} />
              </div>
            </div>
          </>
        )}

        {/* No Coordinates Message */}
        {lat === null && lng === null && !loading && !error && (
          <div className="text-center py-12">
            <MapPin className="w-16 h-16 mx-auto text-gray-300 dark:text-gray-600 mb-4" />
            <h2 className="text-xl font-semibold text-nav-text dark:text-nav-dark-text mb-2">
              Set Your Position
            </h2>
            <p className="text-gray-500 dark:text-gray-400">
              Enter coordinates manually, use GPS, or click on the map to get started.
            </p>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="mt-8 py-4 text-center text-sm text-gray-500 dark:text-gray-400">
        <p>NavApp - Ocean Navigator Daily Productivity</p>
        <p className="text-xs mt-1">
          Weather data from Open-Meteo | Map tiles from OpenStreetMap
        </p>
      </footer>
    </div>
  );
}

export default App;
