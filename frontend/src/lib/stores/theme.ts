import { writable, type Writable } from 'svelte/store';

let storedIsDark = localStorage.getItem('isDark');
if (storedIsDark === null) {
	// initial
	if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
		storedIsDark = 'isDark';
	}
}
export const isDark: Writable<boolean> = writable(storedIsDark === 'isDark' ? true : false);
isDark.subscribe((value) => {
	localStorage.setItem('isDark', value === true ? 'isDark' : 'isLight');
});