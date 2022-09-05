<script lang="ts">
	import { fade } from 'svelte/transition';

	import { Card, Pagination } from '$lib/components/basic';
	import Case from './Case.svelte';
	import { Pruefstelle, type ps } from '$lib/api';

	export let readPagedCaseIDs: ps.PageUUID;
	export let toPageSearch;
</script>

<Card isHideable={false} classes={['mt-4', 'mb-4', 'justify-center', 'max-w-sm', 'mx-auto']}>
	<svelte:fragment slot="title">
		<div class="mx-auto">
			{#if readPagedCaseIDs.items.length === 0}
				Leider nichts gefunden.
			{:else}
				Suchergebnisse: {readPagedCaseIDs.items.length} Treffer
			{/if}
		</div>
	</svelte:fragment>

	<Pagination
		page={readPagedCaseIDs.page}
		size={readPagedCaseIDs.size}
		total={readPagedCaseIDs.total}
		callback={toPageSearch} />
</Card>

{#each readPagedCaseIDs.items as readCaseID}
	{#await Pruefstelle.readCase(readCaseID) then readCase}
		<div in:fade>
			<Case {readCase} classes={['mb-4', 'w-98']} compactView={true} />
		</div>
	{/await}
{/each}

<Pagination
	page={readPagedCaseIDs.page}
	size={readPagedCaseIDs.size}
	total={readPagedCaseIDs.total}
	callback={toPageSearch} />
