import React from 'react';
import { Waves } from 'lucide-react';

function getTideColor(tendency) {
  if (tendency.includes('Spring')) {
    return 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300';
  } else if (tendency.includes('Neap')) {
    return 'bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-300';
  }
  return 'bg-cyan-100 text-cyan-700 dark:bg-cyan-900/30 dark:text-cyan-300';
}

export function TideCard({ data }) {
  if (!data) return null;

  const tideColorClass = getTideColor(data.tendency);

  return (
    <div className="bg-white dark:bg-nav-dark-card rounded-lg p-4 shadow-md">
      <div className="flex items-center gap-2 mb-4">
        <Waves className="w-6 h-6 text-accent-tide dark:text-accent-tide-dark" />
        <h3 className="font-bold text-lg text-nav-text dark:text-nav-dark-text">Tides</h3>
      </div>

      <div className={`text-center p-4 rounded-lg ${tideColorClass}`}>
        <p className="font-bold text-xl">{data.tendency}</p>
      </div>

      <p className="text-sm text-gray-600 dark:text-gray-400 mt-3 text-center">
        {data.description}
      </p>

      <div className="mt-3 flex justify-center">
        <div className="text-center">
          <p className="text-xs text-gray-500 dark:text-gray-400">Moon Phase Factor</p>
          <p className="font-semibold text-nav-text dark:text-nav-dark-text">
            {Math.round(data.moon_phase_factor * 100)}%
          </p>
        </div>
      </div>
    </div>
  );
}
