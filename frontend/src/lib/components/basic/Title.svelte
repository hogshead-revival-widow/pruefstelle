<script lang="ts">
	import { page } from '$app/stores';
	import { getShortIfNeeded } from '$lib/utils';

	export let id: string;
	export let title: string;
	export let path = '';
	export let withContext: undefined | string = undefined;
	export let shortenIfNeeded = true;
	export let shortenToMaxLength = 20;

	let href = '';
	if (withContext === undefined) {
		href = `/dashboard/${path}/${id}`;
	} else {
		href = `/dashboard/${path}/${id}/context/${withContext}`;
	}
	const emphasiseLink = id != '' && href !== $page.url.pathname;
	const displayTitle = shortenIfNeeded ? getShortIfNeeded(title, shortenToMaxLength) : title;
</script>

{#if path != ''}
	{#if href != ''}
		<a class:note-link={emphasiseLink} {href} sveltekit:prefetch>
			<span {title}>{displayTitle}</span>
		</a>
	{:else}
		<span {title}>{displayTitle}</span>
	{/if}
{:else}
	<span {title}>{displayTitle}</span>
{/if}
