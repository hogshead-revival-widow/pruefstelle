<script context="module" lang="ts">
	import { makePruefstelle, Pruefstelle, type ps } from '$lib/api';
	import { isValidUUID } from '$lib/utils';

	export const load = async ({ fetch, params }) => {
		const { case_id } = params;

		if (!isValidUUID(case_id)) throw new Error('invalid id');
		const pruefstelle = makePruefstelle({ customFetch: fetch });
		const promisedPagedEvaluations = pruefstelle.readSelfEvaluationsForCase(case_id, {
			size: 50
		});
		const promisedCase = pruefstelle.readCase(case_id);
		return { props: { promisedPagedEvaluations, promisedCase } };
	};
</script>

<script lang="ts">
	import { fade } from 'svelte/transition';
	import PagedEvaluations from '$lib/components/evaluation/PagedEvaluations.svelte';

	export let promisedCase: Promise<ps.CaseRead>;
	export let promisedPagedEvaluations: Promise<ps.PageEvaluationRead>;

	const toPageEvaluation = (case_id, page, size) => {
		const options = { page, size };
		promisedPagedEvaluations = Pruefstelle.readSelfEvaluationsForCase(case_id, options);
		currentPage = page;
	};

	export let currentPage = undefined;
</script>

{#key currentPage}
	<div in:fade class="mt-4 max-w-96">
		{#await Promise.all( [promisedCase, promisedPagedEvaluations] ) then [readCase, readPagedEvaluations]}
			<PagedEvaluations
				id={readCase.id}
				title={{
					title: `Bewertungen in ${readCase.title}`,
					path: `case/${readCase.id}`,
					id: ''
				}}
				{readPagedEvaluations}
				{toPageEvaluation} />
		{/await}
	</div>
{/key}
