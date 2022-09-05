<script context="module" lang="ts">
	import { makePruefstelle, Pruefstelle, type ps } from '$lib/api';
	import { isValidUUID } from '$lib/utils';

	export const load = async ({ fetch, params }) => {
		const { document_id } = params;

		if (!isValidUUID(document_id)) throw new Error('invalid id');
		const pruefstelle = makePruefstelle({ customFetch: fetch });
		const promisedPagedEvaluations = pruefstelle.readSelfEvaluationsForDocument(document_id, {
			size: 50
		});
		const promisedDocument = pruefstelle.readDocument(document_id);
		return { props: { promisedPagedEvaluations, promisedDocument } };
	};
</script>

<script lang="ts">
	import { fade } from 'svelte/transition';
	import PagedEvaluations from '$lib/components/evaluation/PagedEvaluations.svelte';

	export let promisedDocument: Promise<ps.DocumentRead>;
	export let promisedPagedEvaluations: Promise<ps.PageEvaluationRead>;

	const toPageEvaluation = (document_id, page, size) => {
		const options = { page, size };
		promisedPagedEvaluations = Pruefstelle.readSelfEvaluationsForDocument(document_id, options);
		currentPage = page;
	};

	export let currentPage = undefined;
</script>

{#key currentPage}
	<div in:fade class="mt-4 max-w-96">
		{#await Promise.all( [promisedDocument, promisedPagedEvaluations] ) then [readDocument, readPagedEvaluations]}
			<PagedEvaluations
				id={readDocument.id}
				title={{
					title: `Bewertungen in ${readDocument.title}`,
					path: `document/${readDocument.id}`,
					id: ''
				}}
				{readPagedEvaluations}
				{toPageEvaluation} />
		{/await}
	</div>
{/key}
