import React from 'react';
import { Moon, ArrowUp, ArrowDown } from 'lucide-react';
import { getMoonEmoji } from '../utils/formatters';

function MoonPhaseVisual({ illumination, phase }) {
  // Create a visual representation of the moon phase
  const isWaning = phase.includes('Waning') || phase === 'Last Quarter';

  return (
    <div className="relative w-16 h-16 mx-auto">
      <div
        className="absolute inset-0 rounded-full bg-gray-300 dark:bg-gray-600"
        style={{
          background: `linear-gradient(${isWaning ? '90deg' : '-90deg'},
            #1a1a1a ${(1 - illumination) * 100}%,
            #e5e7eb ${(1 - illumination) * 100}%)`
        }}
      />
      <div className="absolute inset-0 rounded-full border-2 border-gray-400 dark:border-gray-500" />
    </div>
  );
}

export function MoonCard({ data }) {
  if (!data) return null;

  return (
    <div className="bg-white dark:bg-nav-dark-card rounded-lg p-4 shadow-md">
      <div className="flex items-center gap-2 mb-4">
        <Moon className="w-6 h-6 text-accent-moon dark:text-accent-moon-dark" />
        <h3 className="font-bold text-lg text-nav-text dark:text-nav-dark-text">Moon</h3>
      </div>

      <div className="text-center mb-4">
        <div className="text-4xl mb-2">{getMoonEmoji(data.phase)}</div>
        <p className="font-semibold text-nav-text dark:text-nav-dark-text">{data.phase}</p>
        <p className="text-sm text-gray-500 dark:text-gray-400">
          {Math.round(data.illumination * 100)}% illuminated
        </p>
      </div>

      <div className="grid grid-cols-2 gap-4 mb-4">
        <div className="text-center p-2 bg-gray-50 dark:bg-gray-800 rounded">
          <ArrowUp className="w-4 h-4 mx-auto mb-1 text-accent-moon dark:text-accent-moon-dark" />
          <p className="text-xs text-gray-500 dark:text-gray-400">Moonrise</p>
          <p className="font-semibold text-nav-text dark:text-nav-dark-text">
            {data.moonrise || 'N/A'}
          </p>
        </div>
        <div className="text-center p-2 bg-gray-50 dark:bg-gray-800 rounded">
          <ArrowDown className="w-4 h-4 mx-auto mb-1 text-accent-moon dark:text-accent-moon-dark" />
          <p className="text-xs text-gray-500 dark:text-gray-400">Moonset</p>
          <p className="font-semibold text-nav-text dark:text-nav-dark-text">
            {data.moonset || 'N/A'}
          </p>
        </div>
      </div>

      <div className="border-t dark:border-gray-700 pt-3 space-y-2 text-sm">
        <div className="flex justify-between">
          <span className="text-gray-600 dark:text-gray-400">Next Full Moon</span>
          <span className="text-nav-text dark:text-nav-dark-text">{data.next_full_moon}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-gray-600 dark:text-gray-400">Next New Moon</span>
          <span className="text-nav-text dark:text-nav-dark-text">{data.next_new_moon}</span>
        </div>
      </div>
    </div>
  );
}
