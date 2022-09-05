<script>
	/*
		Wrapping all alerts, to be used as parent of `Alert`.
	*/
	import { alerts, removeAlert } from '$lib/scripts/alerts';
	import Alert from '$lib/components/alert/Alert.svelte';

	export let classes = [];

	const handleClose = (event) => removeAlert(event.detail);
</script>

<aside class="stack max-w-sm text-sm {classes.join(' ')}">
	{#each $alerts as alert, index (alert.id)}
		<Alert {index} {...alert} on:close={handleClose} />
	{/each}
</aside>
