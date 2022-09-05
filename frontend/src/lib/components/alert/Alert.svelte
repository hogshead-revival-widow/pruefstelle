<script lang="ts">
	/*
		Single alert component, to be used as child of `Alerts`
		Per default, an alert fades away after `deleteAfter` ms.
	*/
	import { createEventDispatcher, onDestroy } from 'svelte';
	import { fade } from 'svelte/transition';

	import type { AlertType } from '$lib/scripts/alerts';

	export let index: number;
	export let type: AlertType;
	export let message: string;
	export let id: number;
	export let withTimeout = true; // if `true`, delete after `deleteAfter` ms

	const dispatch = createEventDispatcher();
	const deleteAfter = 5000;
	const closeAlert = () => dispatch('close', { id }); // the event is handled by `Alerts`

	if (withTimeout) {
		const timeoutID = setTimeout(closeAlert, deleteAfter);
		onDestroy(() => clearTimeout(timeoutID));
	}

	const shadowSize = {
		0: 'shadow-md',
		1: 'shadow',
		2: 'shadow-sm'
	};

	const color: Record<AlertType, string> = {
		info: 'bg-info',
		success: 'bg-success',
		warning: 'bg-warning',
		error: 'bg-error'
	};
</script>

<article
	class="alert {color[type]} text-primary-content {index <= 0 && index <= 2
		? shadowSize[index]
		: ''} "
	out:fade|local>
	<div>
		<p>
			{#if type === 'error'}Fehler: {/if}{message}
		</p>
	</div>

	<div class="flex-none">
		<button class="btn btn-sm btn-ghost" on:click|once={closeAlert}>X</button>
	</div>
</article>
