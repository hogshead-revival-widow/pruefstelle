<script context="module" lang="ts">
	import { makePruefstelle, Pruefstelle, type ps } from '$lib/api';

	import { isValidUUID } from '$lib/utils';

	export const load = async ({ fetch, params }) => {
		const { text_id } = params;

		if (!isValidUUID(text_id)) throw new Error('invalid ID');
		const pruefstelle = makePruefstelle({ customFetch: fetch });
		const promisedPagedEvaluations = pruefstelle.readSelfEvaluations({
			size: 50
		});
		return { props: { promisedPagedEvaluations } };
	};
</script>

<script lang="ts">
	import { fade } from 'svelte/transition';
	import PagedEvaluations from '$lib/components/evaluation/PagedEvaluations.svelte';

	export let promisedPagedEvaluations: Promise<ps.PageEvaluationRead>;

	const toPageEvaluation = (_, page, size) => {
		const options = { page, size };
		promisedPagedEvaluations = Pruefstelle.readSelfEvaluations(options);
		currentPage = page;
	};

	export let currentPage = undefined;
</script>

{#key currentPage}
	<div in:fade class="mt-4">
		{#await promisedPagedEvaluations then readPagedEvaluations}
			<PagedEvaluations
				id={undefined}
				fetchDocument={false}
				title={{ title: 'Meine Bewertungen', path: 'user/has/evaluated', id: '' }}
				{readPagedEvaluations}
				{toPageEvaluation} />
		{/await}
	</div>
{/key}
