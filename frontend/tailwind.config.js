/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Light mode
        'nav-bg': '#F8FAFC',
        'nav-card': '#FFFFFF',
        'nav-text': '#0F172A',
        // Dark mode (night watch)
        'nav-dark-bg': '#0A0A0A',
        'nav-dark-card': '#1A1A1A',
        'nav-dark-text': '#FF6B6B',
        // Accents
        'accent-sun': '#F59E0B',
        'accent-moon': '#6366F1',
        'accent-prayer': '#10B981',
        'accent-tide': '#0EA5E9',
        'accent-weather': '#64748B',
        // Dark mode accents
        'accent-sun-dark': '#CC5500',
        'accent-moon-dark': '#8B0000',
        'accent-prayer-dark': '#006400',
        'accent-tide-dark': '#003366',
        'accent-weather-dark': '#4A4A4A',
      }
    },
  },
  plugins: [],
}
