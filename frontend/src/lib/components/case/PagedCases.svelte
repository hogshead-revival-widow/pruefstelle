<script lang="ts">
	import type { ps } from '$lib/api';

	import { fly } from 'svelte/transition';

	import { Card, Pagination } from '$lib/components/basic';
	import Case from './Case.svelte';

	export let readPagedCases: ps.PageCaseRead;
	export let title = '';
	export let toPageCase;
	export let filterCases: (readCase: ps.CaseRead) => boolean | undefined = undefined;

	$: noCases =
		readPagedCases.total === 0 ||
		(readPagedCases.items.length === 0 && readPagedCases.total < readPagedCases.size);

	$: if (filterCases !== undefined) {
		readPagedCases.items = readPagedCases.items.filter(filterCases);
		if (readPagedCases.items.length === 0 && readPagedCases.total !== 0) {
			window.location.reload();
		}
	}
</script>

<section>
	{#if noCases}
		<Card isHideable={false} classes={['w-96']}>
			<svelte:fragment slot="title">Keine Fälle gefunden</svelte:fragment>
		</Card>
	{:else}
		<Card isHideable={false} classes={['mb-4', 'justify-center', 'max-w-sm', 'mx-auto', 'w-100']}>
			<svelte:fragment slot="title">
				<div class="mx-auto">
					{@html title}
				</div>
			</svelte:fragment>

			<Pagination
				page={readPagedCases.page}
				size={readPagedCases.size}
				total={readPagedCases.total}
				callback={toPageCase} />
		</Card>
	{/if}

	{#each readPagedCases.items as readCase (readCase.id)}
		<div out:fly|local class="w-98">
			<Case compactView={true} bind:readCase classes={['mb-4']} showQuality={false} />
		</div>
	{/each}

	<Pagination
		page={readPagedCases.page}
		size={readPagedCases.size}
		total={readPagedCases.total}
		callback={toPageCase} />
</section>
