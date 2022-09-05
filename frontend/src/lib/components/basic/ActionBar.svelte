<script>
	export let classes = [];

	classes = ['menu', 'menu-horizontal', 'rounded-box', 'mb-4', ...classes];
</script>

<ul class={classes.join(' ')}>
	<slot />
</ul>
