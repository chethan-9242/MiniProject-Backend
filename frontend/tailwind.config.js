/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        ayurveda: {
          50: '#f0f9f0',
          100: '#dcf2dc',
          200: '#bce5bc',
          300: '#8dd38d',
          400: '#5bb85b',
          500: '#369f36',
          600: '#28802a',
          700: '#226622',
          800: '#1f521f',
          900: '#1c441c',
        },
        vata: '#E6F3FF',
        pitta: '#FFE6CC',
        kapha: '#E6FFE6',
      },
      fontFamily: {
        'sans': ['Inter', 'ui-sans-serif', 'system-ui'],
        'serif': ['Playfair Display', 'ui-serif', 'Georgia'],
      }
    },
  },
  plugins: [],
}