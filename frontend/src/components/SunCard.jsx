import React from 'react';
import { Sun, Sunrise, Sunset } from 'lucide-react';

export function SunCard({ data }) {
  if (!data) return null;

  return (
    <div className="bg-white dark:bg-nav-dark-card rounded-lg p-4 shadow-md">
      <div className="flex items-center gap-2 mb-4">
        <Sun className="w-6 h-6 text-accent-sun dark:text-accent-sun-dark" />
        <h3 className="font-bold text-lg text-nav-text dark:text-nav-dark-text">Sun</h3>
      </div>

      <div className="grid grid-cols-3 gap-4 mb-4">
        <div className="text-center">
          <Sunrise className="w-5 h-5 mx-auto mb-1 text-orange-400" />
          <p className="text-xs text-gray-500 dark:text-gray-400">Sunrise</p>
          <p className="font-semibold text-nav-text dark:text-nav-dark-text">{data.sunrise}</p>
        </div>
        <div className="text-center">
          <Sun className="w-5 h-5 mx-auto mb-1 text-yellow-500" />
          <p className="text-xs text-gray-500 dark:text-gray-400">Noon</p>
          <p className="font-semibold text-nav-text dark:text-nav-dark-text">{data.solar_noon}</p>
        </div>
        <div className="text-center">
          <Sunset className="w-5 h-5 mx-auto mb-1 text-orange-600" />
          <p className="text-xs text-gray-500 dark:text-gray-400">Sunset</p>
          <p className="font-semibold text-nav-text dark:text-nav-dark-text">{data.sunset}</p>
        </div>
      </div>

      <div className="text-center mb-4 py-2 bg-gray-50 dark:bg-gray-800 rounded">
        <p className="text-xs text-gray-500 dark:text-gray-400">Day Length</p>
        <p className="font-semibold text-nav-text dark:text-nav-dark-text">{data.day_length}</p>
      </div>

      <div className="border-t dark:border-gray-700 pt-3">
        <h4 className="text-sm font-semibold text-nav-text dark:text-nav-dark-text mb-2">Twilight</h4>
        <div className="space-y-2 text-sm">
          <div className="flex justify-between items-center">
            <span className="text-gray-600 dark:text-gray-400">Civil</span>
            <span className="text-nav-text dark:text-nav-dark-text">
              {data.twilight.civil.dawn} - {data.twilight.civil.dusk}
            </span>
          </div>
          <div className="flex justify-between items-center bg-blue-50 dark:bg-blue-900/20 -mx-2 px-2 py-1 rounded">
            <span className="text-blue-700 dark:text-blue-300 font-medium">Nautical</span>
            <span className="text-blue-700 dark:text-blue-300 font-medium">
              {data.twilight.nautical.dawn} - {data.twilight.nautical.dusk}
            </span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-gray-600 dark:text-gray-400">Astronomical</span>
            <span className="text-nav-text dark:text-nav-dark-text">
              {data.twilight.astronomical.dawn} - {data.twilight.astronomical.dusk}
            </span>
          </div>
        </div>
        <p className="text-xs text-blue-600 dark:text-blue-400 mt-2">
          Nautical twilight = celestial navigation window
        </p>
      </div>
    </div>
  );
}
