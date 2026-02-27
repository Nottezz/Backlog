/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        display: ['"Playfair Display"', 'Georgia', 'serif'],
        body: ['"DM Sans"', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'monospace'],
      },
      colors: {
        ink: {
          50: '#f5f0eb',
          100: '#e8ddd2',
          200: '#d4bfa8',
          300: '#bb9a7a',
          400: '#a67c58',
          500: '#8b6340',
          600: '#704f33',
          700: '#563d28',
          800: '#3d2c1e',
          900: '#261b12',
          950: '#140e09',
        },
        parchment: {
          50: '#fdfaf5',
          100: '#f9f2e4',
          200: '#f2e4c8',
          300: '#e8d0a3',
        },
        accent: {
          DEFAULT: '#c9463a',
          light: '#e05a4e',
          dark: '#a33529',
        }
      },
      backgroundImage: {
        'paper': "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='4' height='4'%3E%3Crect width='4' height='4' fill='%23fdfaf5'/%3E%3Crect x='0' y='0' width='1' height='1' fill='%23f0e8d8' opacity='0.3'/%3E%3C/svg%3E\")",
      },
      animation: {
        'fade-up': 'fadeUp 0.6s ease forwards',
        'fade-in': 'fadeIn 0.5s ease forwards',
      },
      keyframes: {
        fadeUp: {
          '0%': { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
      },
    },
  },
  plugins: [],
}
