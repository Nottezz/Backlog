/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        display: ['"Plus Jakarta Sans"', 'system-ui', 'sans-serif'],
        body: ['"Inter"', 'system-ui', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'monospace'],
      },
      colors: {
        // Dark slate base — modern, neutral, premium
        base: {
          50:  '#f8f9fc',
          100: '#f0f2f8',
          200: '#dde2ef',
          300: '#c1c9df',
          400: '#9aa4c0',
          500: '#6b7899',
          600: '#4f5c7e',
          700: '#3a4564',
          800: '#27314e',
          900: '#171e35',
          950: '#0d1121',
        },
        // Vibrant violet-indigo accent
        accent: {
          50:  '#eef2ff',
          100: '#e0e7ff',
          200: '#c7d2fe',
          300: '#a5b4fc',
          400: '#818cf8',
          DEFAULT: '#6366f1',
          600: '#4f46e5',
          700: '#4338ca',
          dark:   '#3730a3',
        },
        // Warm surface tones
        surface: {
          DEFAULT: '#ffffff',
          soft:    '#f8f9fc',
          muted:   '#f0f2f8',
          border:  '#e2e8f0',
        },
        // Danger
        danger: {
          DEFAULT: '#ef4444',
          light:   '#fca5a5',
          dark:    '#dc2626',
        },
      },
      animation: {
        'fade-up': 'fadeUp 0.6s ease forwards',
        'fade-in': 'fadeIn 0.5s ease forwards',
      },
      keyframes: {
        fadeUp: {
          '0%':   { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        fadeIn: {
          '0%':   { opacity: '0' },
          '100%': { opacity: '1' },
        },
      },
    },
  },
  plugins: [],
}
