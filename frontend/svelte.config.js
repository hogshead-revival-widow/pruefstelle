import preprocess from 'svelte-preprocess';
import adapter from '@sveltejs/adapter-static';

const config = {
	kit: {
		adapter: adapter({ fallback: '200.html' }),
		trailingSlash: 'always'
	},
	preprocess: [
		preprocess({
			postcss: true
		})
	]
};

export default config;
