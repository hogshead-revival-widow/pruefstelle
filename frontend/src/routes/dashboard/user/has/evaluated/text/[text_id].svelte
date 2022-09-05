<script context="module" lang="ts">
	import { makePruefstelle, Pruefstelle, type ps } from '$lib/api';
	import { isValidUUID } from '$lib/utils';

	export const load = async ({ fetch, params }) => {
		const { text_id } = params;

		if (!isValidUUID(text_id)) throw new Error('invalid id');
		const pruefstelle = makePruefstelle({ customFetch: fetch });
		const promisedPagedEvaluations = pruefstelle.readSelfEvaluationsForText(text_id, {
			size: 50
		});
		const promisedText = pruefstelle.readText(text_id);
		return { props: { promisedPagedEvaluations, promisedText } };
	};
</script>

<script lang="ts">
	import { fade } from 'svelte/transition';
	import PagedEvaluations from '$lib/components/evaluation/PagedEvaluations.svelte';

	export let promisedText: Promise<ps.TextRead>;
	export let promisedPagedEvaluations: Promise<ps.PageEvaluationRead>;

	const toPageEvaluation = (text_id, page, size) => {
		const options = { page, size };
		promisedPagedEvaluations = Pruefstelle.readSelfEvaluationsForText(text_id, options);
		currentPage = page;
	};

	export let currentPage = undefined;
</script>

{#key currentPage}
	<div in:fade class="mt-4">
		{#await Promise.all( [promisedText, promisedPagedEvaluations] ) then [readText, readPagedEvaluations]}
			<PagedEvaluations
				id={readText.id}
				title={{
					title: `Bewertungen in ${readText.title}`,
					path: `text/${readText.id}`,
					id: ''
				}}
				{readPagedEvaluations}
				{toPageEvaluation} />
		{/await}
	</div>
{/key}
