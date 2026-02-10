import React from 'react';
import { Cloud, Wind, Thermometer, Eye } from 'lucide-react';

function WindDirectionArrow({ direction }) {
  const directionMap = {
    'N': 180, 'NNE': 202.5, 'NE': 225, 'ENE': 247.5,
    'E': 270, 'ESE': 292.5, 'SE': 315, 'SSE': 337.5,
    'S': 0, 'SSW': 22.5, 'SW': 45, 'WSW': 67.5,
    'W': 90, 'WNW': 112.5, 'NW': 135, 'NNW': 157.5
  };

  const rotation = directionMap[direction] || 0;

  return (
    <div
      className="inline-block transform"
      style={{ transform: `rotate(${rotation}deg)` }}
    >
      ↓
    </div>
  );
}

function getBeaufortScale(knots) {
  if (knots < 1) return { scale: 0, description: 'Calm' };
  if (knots < 4) return { scale: 1, description: 'Light Air' };
  if (knots < 7) return { scale: 2, description: 'Light Breeze' };
  if (knots < 11) return { scale: 3, description: 'Gentle Breeze' };
  if (knots < 17) return { scale: 4, description: 'Moderate Breeze' };
  if (knots < 22) return { scale: 5, description: 'Fresh Breeze' };
  if (knots < 28) return { scale: 6, description: 'Strong Breeze' };
  if (knots < 34) return { scale: 7, description: 'Near Gale' };
  if (knots < 41) return { scale: 8, description: 'Gale' };
  if (knots < 48) return { scale: 9, description: 'Strong Gale' };
  if (knots < 56) return { scale: 10, description: 'Storm' };
  if (knots < 64) return { scale: 11, description: 'Violent Storm' };
  return { scale: 12, description: 'Hurricane' };
}

export function WeatherCard({ data }) {
  if (!data) return null;

  const beaufort = getBeaufortScale(data.wind.speed_knots);

  return (
    <div className="bg-white dark:bg-nav-dark-card rounded-lg p-4 shadow-md">
      <div className="flex items-center gap-2 mb-4">
        <Cloud className="w-6 h-6 text-accent-weather dark:text-accent-weather-dark" />
        <h3 className="font-bold text-lg text-nav-text dark:text-nav-dark-text">Marine Weather</h3>
      </div>

      {/* Wind Section */}
      <div className="mb-4 p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
        <div className="flex items-center gap-2 mb-2">
          <Wind className="w-4 h-4 text-gray-600 dark:text-gray-400" />
          <span className="font-medium text-nav-text dark:text-nav-dark-text">Wind</span>
        </div>
        <div className="grid grid-cols-3 gap-2 text-center">
          <div>
            <p className="text-2xl font-bold text-nav-text dark:text-nav-dark-text">
              {data.wind.speed_knots}
            </p>
            <p className="text-xs text-gray-500 dark:text-gray-400">knots</p>
          </div>
          <div>
            <p className="text-2xl font-bold text-nav-text dark:text-nav-dark-text">
              <WindDirectionArrow direction={data.wind.direction} /> {data.wind.direction}
            </p>
            <p className="text-xs text-gray-500 dark:text-gray-400">direction</p>
          </div>
          <div>
            <p className="text-2xl font-bold text-nav-text dark:text-nav-dark-text">
              {data.wind.gusts_knots}
            </p>
            <p className="text-xs text-gray-500 dark:text-gray-400">gusts kn</p>
          </div>
        </div>
        <p className="text-xs text-center text-gray-500 dark:text-gray-400 mt-2">
          Beaufort {beaufort.scale}: {beaufort.description}
        </p>
      </div>

      {/* Waves & Swell */}
      <div className="grid grid-cols-2 gap-3 mb-4">
        <div className="p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
          <p className="text-xs text-gray-500 dark:text-gray-400 mb-1">Waves</p>
          <p className="font-bold text-nav-text dark:text-nav-dark-text">{data.waves.height_m}m</p>
          <p className="text-xs text-gray-500 dark:text-gray-400">{data.waves.period_s}s period</p>
        </div>
        <div className="p-3 bg-cyan-50 dark:bg-cyan-900/20 rounded-lg">
          <p className="text-xs text-gray-500 dark:text-gray-400 mb-1">Swell</p>
          <p className="font-bold text-nav-text dark:text-nav-dark-text">{data.swell.height_m}m {data.swell.direction}</p>
          <p className="text-xs text-gray-500 dark:text-gray-400">{data.swell.period_s}s period</p>
        </div>
      </div>

      {/* Temperature & Visibility */}
      <div className="grid grid-cols-2 gap-3">
        <div className="flex items-center gap-2 p-2">
          <Thermometer className="w-4 h-4 text-orange-500" />
          <div>
            <p className="text-xs text-gray-500 dark:text-gray-400">Temp</p>
            <p className="font-semibold text-nav-text dark:text-nav-dark-text">{data.temperature_c}°C</p>
          </div>
        </div>
        <div className="flex items-center gap-2 p-2">
          <Eye className="w-4 h-4 text-purple-500" />
          <div>
            <p className="text-xs text-gray-500 dark:text-gray-400">Visibility</p>
            <p className="font-semibold text-nav-text dark:text-nav-dark-text">{data.visibility_km}km</p>
          </div>
        </div>
      </div>
    </div>
  );
}
