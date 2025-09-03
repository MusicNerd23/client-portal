/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    './app/templates/**/*.html',
    './app/static/js/**/*.js',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          '600': '#2563eb',
          '700': '#1d4ed8',
        },
        success: '#059669',
        warning: '#f59e0b',
        danger: '#e11d48',
        slate: {
          '900': '#0f172a',
        },
      },
    },
  },
  plugins: [],
}
