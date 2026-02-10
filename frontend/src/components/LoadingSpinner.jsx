import React from 'react';
import { Loader2 } from 'lucide-react';

export function LoadingSpinner() {
  return (
    <div className="flex items-center justify-center p-8">
      <Loader2 className="w-8 h-8 animate-spin text-accent-sun dark:text-accent-sun-dark" />
      <span className="ml-2 text-nav-text dark:text-nav-dark-text">Loading navigation data...</span>
    </div>
  );
}
