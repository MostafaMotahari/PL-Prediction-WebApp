/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./public/**/*.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        darkBlue: '#1d1a53',
        lightBlue: '#3dc7ee',
      }
    },
  },
  plugins: [],
}
