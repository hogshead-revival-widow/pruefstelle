<script>
	import { onDestroy } from 'svelte';
	import { isDark } from '$lib/stores';

	const schemes = { dark: 'dark', light: 'light' };
	// property value corresponds to daisyUI theme
	const mapSchemeToTheme = { dark: 'dark', light: 'light' };
	const matchDark = '(prefers-color-scheme: dark)';

	const onChange = (event) => {
		$isDark = event.matches ? true : false;
	};
	// observe os-side changes
	window.matchMedia(matchDark).addEventListener('change', onChange);

	// toggle change
	$: {
		const ele = document.querySelector('html');
		const currentScheme = $isDark ? schemes.dark : schemes.light;
		const theme = mapSchemeToTheme[currentScheme];
		ele.setAttribute('data-theme', theme);
	}

	// clenaup
	onDestroy(() => {
		window.matchMedia(matchDark).removeEventListener('change', onChange);
	});
</script>

<label class="swap swap-rotate btn rounded-btn btn-ghost">
	<input type="checkbox" class="hidden" bind:checked={$isDark} />
	<i class="fas fa-moon swap-on" alt="dunkel" />
	<i class="fas fa-sun swap-off " alt="hell (kontrastreicher)" />
</label>
