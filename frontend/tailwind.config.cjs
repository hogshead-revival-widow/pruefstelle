const typography = require('@tailwindcss/typography');
const forms = require('@tailwindcss/forms');
const daisy = require('daisyui');

const secondary = 'rgba(50, 176, 246)';
const primary = 'rgb(9, 131, 198)';
const info = secondary;

const config = {
	content: ['./src/**/*.{html,js,svelte,ts}'],

	theme: {
		extend: {}
	},

	plugins: [forms, typography, daisy],
	daisyui: {
		themes: [
			{
				light: {
					...require('daisyui/src/colors/themes')['[data-theme=light]'],
					primary,
					secondary,
					info
				},
				dark: {
					...require('daisyui/src/colors/themes')['[data-theme=dark]'],
					primary,
					secondary,
					info
				}
			}
		]
	}
};

module.exports = config;
