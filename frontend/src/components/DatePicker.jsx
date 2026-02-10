import React from 'react';
import { Calendar, ChevronLeft, ChevronRight } from 'lucide-react';
import { format, addDays, subDays } from 'date-fns';

export function DatePicker({ date, onDateChange }) {
  const handlePrevDay = () => {
    const currentDate = new Date(date);
    onDateChange(format(subDays(currentDate, 1), 'yyyy-MM-dd'));
  };

  const handleNextDay = () => {
    const currentDate = new Date(date);
    onDateChange(format(addDays(currentDate, 1), 'yyyy-MM-dd'));
  };

  const handleToday = () => {
    onDateChange(format(new Date(), 'yyyy-MM-dd'));
  };

  const handleInputChange = (e) => {
    onDateChange(e.target.value);
  };

  const displayDate = new Date(date + 'T00:00:00');

  return (
    <div className="bg-white dark:bg-nav-dark-card rounded-lg p-4 shadow-md">
      <div className="flex items-center gap-2 mb-3">
        <Calendar className="w-5 h-5 text-accent-prayer dark:text-accent-prayer-dark" />
        <h3 className="font-semibold text-nav-text dark:text-nav-dark-text">Date</h3>
      </div>

      <div className="flex items-center gap-2">
        <button
          onClick={handlePrevDay}
          className="p-2 rounded-md hover:bg-gray-100 dark:hover:bg-gray-700
                     text-nav-text dark:text-nav-dark-text min-w-[44px] min-h-[44px]
                     flex items-center justify-center"
          aria-label="Previous day"
        >
          <ChevronLeft className="w-5 h-5" />
        </button>

        <input
          type="date"
          value={date}
          onChange={handleInputChange}
          className="flex-1 px-3 py-2 rounded-md border border-gray-300 dark:border-gray-600
                     bg-white dark:bg-gray-800 text-nav-text dark:text-nav-dark-text
                     focus:ring-2 focus:ring-accent-prayer dark:focus:ring-accent-prayer-dark outline-none
                     text-center"
        />

        <button
          onClick={handleNextDay}
          className="p-2 rounded-md hover:bg-gray-100 dark:hover:bg-gray-700
                     text-nav-text dark:text-nav-dark-text min-w-[44px] min-h-[44px]
                     flex items-center justify-center"
          aria-label="Next day"
        >
          <ChevronRight className="w-5 h-5" />
        </button>
      </div>

      <div className="mt-2 flex justify-between items-center">
        <p className="text-sm text-gray-500 dark:text-gray-400">
          {format(displayDate, 'EEEE, MMMM d, yyyy')}
        </p>
        <button
          onClick={handleToday}
          className="text-xs px-2 py-1 rounded bg-gray-100 dark:bg-gray-700
                     text-gray-600 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600"
        >
          Today
        </button>
      </div>
    </div>
  );
}
