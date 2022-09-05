<script context="module" lang="ts">
	import { makePruefstelle, Pruefstelle, type ps } from '$lib/api';

	export const load = async ({ fetch }) => {
		const pruefstelle = makePruefstelle({ customFetch: fetch });
		const readPagedCases = await pruefstelle.listCases({
			size: 5
		});
		return { props: { readPagedCases } };
	};
</script>

<script lang="ts">
	import { fade } from 'svelte/transition';
	import PagedCases from '$lib/components/case/PagedCases.svelte';

	export let readPagedCases: ps.PageCaseRead;
	export let currentPage = undefined;

	const toPageCase = async (_, page, size) => {
		const options = { page, size };
		readPagedCases = await Pruefstelle.listCases(options);
		currentPage = page;
	};
</script>

{#key currentPage}
	<div in:fade class="mt-4 ">
		<PagedCases title="Alle Fälle" {readPagedCases} {toPageCase} />
	</div>
{/key}
