/** @type {import('tailwindcss').Config} */
module.exports = {
	content: ['./index.html', './assets/css/tw_input.css', './assets/js/main.js'],
	darkMode: ['class', '[data-theme="dark"]'],
	theme: {
		extend: {
			screens: {
				support: { raw: '(hover: hover)' }, // Check for hover support
			},
			colors: {
				iceCold: '#BDF4F9', //  #BDF4F9 , #CAF3EB
			},
		},
	},
};
