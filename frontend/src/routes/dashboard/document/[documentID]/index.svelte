<script context="module" lang="ts">
	import { makePruefstelle, Pruefstelle, type ps } from '$lib/api';

	export const load = async ({ fetch, params }) => {
		const { documentID } = params;
		const pruefstelle = makePruefstelle({ customFetch: fetch });
		const readDocument = await pruefstelle.readDocument(documentID);

		return { props: { readDocument } };
	};
</script>

<script lang="ts">
	import Document from '$lib/components/Document.svelte';
	import SelectContext from '$lib/components/SelectContext.svelte';
	import { goto } from '$app/navigation';
	export let readDocument: ps.DocumentRead;

	import { page } from '$app/stores';
	import { onMount } from 'svelte';

	onMount(() => {
		// guess context
		// can't do this in load() as this would trigger goto() while prefetching
		if (!$page.url.searchParams.has('forced') && readDocument.cases.length === 1) {
			const caseID = readDocument.cases[0].id;
			goto(`/dashboard/document/${readDocument.id}/context/${caseID}`);
		}
	});
</script>

<section class="mr-10">
	<Document {readDocument} />
</section>

<section class="max-w-sm mt-8">
	<SelectContext selectFor={readDocument} />
</section>
