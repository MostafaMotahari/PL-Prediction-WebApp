/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./public/**/*.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        darkBlue: '#1d1a53',
        lightBlue: '#3dc7ee',
        supDarkPurple: '#40445a',
        darkPurple: '#725ce0',
        lightPurple: '#628cf6',
        lightWhite: '#f7f8ff',
      },
      boxShadow: {
        'dark': 'inset 5px 8px 5px 1px black',
      }
    },
  },
  plugins: [],
}
