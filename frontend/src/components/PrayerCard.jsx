import React from 'react';
import { Clock } from 'lucide-react';

const PRAYER_METHODS = {
  muslim_world_league: 'Muslim World League',
  isna: 'ISNA',
  egyptian: 'Egyptian General Authority',
  umm_al_qura: 'Umm Al-Qura',
  dubai: 'Dubai',
  kuwait: 'Kuwait',
  qatar: 'Qatar'
};

function PrayerTime({ name, time, isNext }) {
  return (
    <div className={`flex justify-between items-center py-2 px-3 rounded
                     ${isNext ? 'bg-green-100 dark:bg-green-900/30' : ''}`}>
      <span className={`${isNext ? 'font-bold text-green-700 dark:text-green-400' : 'text-gray-600 dark:text-gray-400'}`}>
        {name}
      </span>
      <span className={`font-semibold ${isNext ? 'text-green-700 dark:text-green-400' : 'text-nav-text dark:text-nav-dark-text'}`}>
        {time}
      </span>
    </div>
  );
}

function getNextPrayer(prayers) {
  if (!prayers) return null;

  const now = new Date();
  const currentTime = now.getHours() * 60 + now.getMinutes();

  const prayerOrder = ['fajr', 'sunrise', 'dhuhr', 'asr', 'maghrib', 'isha'];

  for (const prayer of prayerOrder) {
    const time = prayers[prayer];
    if (time && time !== 'N/A') {
      const [hours, minutes] = time.split(':').map(Number);
      const prayerMinutes = hours * 60 + minutes;
      if (prayerMinutes > currentTime) {
        return prayer;
      }
    }
  }

  return 'fajr'; // Next day's Fajr
}

export function PrayerCard({ data, method, onMethodChange }) {
  if (!data) return null;

  const nextPrayer = getNextPrayer(data);

  return (
    <div className="bg-white dark:bg-nav-dark-card rounded-lg p-4 shadow-md">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <Clock className="w-6 h-6 text-accent-prayer dark:text-accent-prayer-dark" />
          <h3 className="font-bold text-lg text-nav-text dark:text-nav-dark-text">Prayer Times</h3>
        </div>
      </div>

      <div className="space-y-1 mb-4">
        <PrayerTime name="Fajr" time={data.fajr} isNext={nextPrayer === 'fajr'} />
        <PrayerTime name="Sunrise" time={data.sunrise} isNext={nextPrayer === 'sunrise'} />
        <PrayerTime name="Dhuhr" time={data.dhuhr} isNext={nextPrayer === 'dhuhr'} />
        <PrayerTime name="Asr" time={data.asr} isNext={nextPrayer === 'asr'} />
        <PrayerTime name="Maghrib" time={data.maghrib} isNext={nextPrayer === 'maghrib'} />
        <PrayerTime name="Isha" time={data.isha} isNext={nextPrayer === 'isha'} />
      </div>

      <div className="border-t dark:border-gray-700 pt-3">
        <label className="block text-xs text-gray-500 dark:text-gray-400 mb-1">
          Calculation Method
        </label>
        <select
          value={method}
          onChange={(e) => onMethodChange(e.target.value)}
          className="w-full px-3 py-2 rounded-md border border-gray-300 dark:border-gray-600
                     bg-white dark:bg-gray-800 text-nav-text dark:text-nav-dark-text
                     focus:ring-2 focus:ring-accent-prayer dark:focus:ring-accent-prayer-dark outline-none
                     text-sm"
        >
          {Object.entries(PRAYER_METHODS).map(([key, name]) => (
            <option key={key} value={key}>{name}</option>
          ))}
        </select>
      </div>
    </div>
  );
}
