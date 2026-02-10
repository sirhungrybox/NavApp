import React from 'react';
import { Sun, Moon } from 'lucide-react';

export function DarkModeToggle({ isDark, onToggle }) {
  return (
    <button
      onClick={onToggle}
      className="p-3 rounded-full transition-colors min-w-[48px] min-h-[48px]
                 flex items-center justify-center
                 bg-gray-200 dark:bg-gray-700
                 hover:bg-gray-300 dark:hover:bg-gray-600
                 text-gray-700 dark:text-gray-200"
      aria-label={isDark ? 'Switch to light mode' : 'Switch to dark mode'}
    >
      {isDark ? (
        <Sun className="w-6 h-6" />
      ) : (
        <Moon className="w-6 h-6" />
      )}
    </button>
  );
}
