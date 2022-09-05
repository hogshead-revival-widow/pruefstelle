<script context="module" lang="ts">
	import { makePruefstelle, Pruefstelle, type ps } from '$lib/api';
	export const load = async ({ fetch }) => {
		const pruefstelle = makePruefstelle({ customFetch: fetch });
		let readPagedCases = await pruefstelle.readSelfCases({ size: 5 });
		return { props: { readPagedCases } };
	};
</script>

<script lang="ts">
	import { fade } from 'svelte/transition';
	import PagedCases from '$lib/components/case/PagedCases.svelte';
	import { user } from '$lib/stores';

	export let readPagedCases: ps.PageCaseRead;
	export let currentPage = undefined;

	const toPageCase = async (_, page, size) => {
		const options = { page, size };
		readPagedCases = await Pruefstelle.readSelfCases(options);
		currentPage = page;
	};

	const filterCases = (readCase: ps.CaseRead) =>
		readCase.watchers.map((watcher) => watcher.id).includes($user.id);
</script>

{#key currentPage}
	<div in:fade class="mt-4">
		<PagedCases title="Beobachte Fälle" {readPagedCases} {toPageCase} {filterCases} />
	</div>
{/key}
