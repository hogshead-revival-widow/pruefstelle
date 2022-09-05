<script context="module" lang="ts">
	import { makePruefstelle, Pruefstelle } from '$lib/api';

	export const load = async ({ fetch, params }) => {
		const { id } = params;
		const pruefstelle = makePruefstelle({ customFetch: fetch });
		const readCase = await pruefstelle.readCase(id);
		const readCaseReports = await pruefstelle.readCaseReport(id);
		return { props: { readCase, readCaseReports } };
	};
</script>

<script lang="ts">
	import { fade } from 'svelte/transition';
	import { onMount } from 'svelte';

	import Case from '$lib/components/case/Case.svelte';
	import Options from '$lib/components/case/Options.svelte';
	import Charts from '$lib/components/chart/Charts.svelte';

	import { showModal } from '$lib/scripts/modal';

	import EvaluationModal from '$lib/components/evaluation/EvaluationModal.svelte';
	import StatusResearchQuality from '$lib/components/ResearchQuality/StatusResearchQuality.svelte';
	import type { ps } from '$lib/api';
	import { needsReload } from '$lib/api/utils';
	import { reloader } from '$lib/scripts/reloader';
	import { getCharts } from '$lib/scripts/charts';

	export let readCase: ps.CaseRead;
	export let readCaseReports: ps.ReportWithPoints[];

	const refreshState = async () => {
		readCase = await Pruefstelle.readCase(readCase.id);
		readCaseReports = await Pruefstelle.readCaseReport(readCase.id);

		return readCase;
	};

	// Refresh item if it is not fully loaded yet
	if (needsReload(readCase)) {
		onMount(async () => await reloader(readCase, refreshState));
	}

	let showEvaluationClicked = false;
	const showEvaluation = (event) => {
		showEvaluationClicked = true;
		showModal({ id: 'modal-evaluateCards' });
	};

	$: charts = getCharts(readCaseReports);
</script>

{#if showEvaluationClicked === true}
	<EvaluationModal
		bind:readReports={readCaseReports}
		readDocuments={readCase.documents}
		{refreshState} />
{/if}
<section class="mr-10" in:fade>
	<Case bind:readCaseReports {readCase} compactView={false} {showEvaluation} />
</section>

<section class="max-w-sm mt-8" in:fade>
	{#if readCaseReports !== undefined && readCase !== undefined}
		<StatusResearchQuality
			bind:item={readCase}
			bind:readProfile={readCase.profile}
			bind:readReports={readCaseReports}
			asStats={true} />
	{/if}

	{#if readCase !== undefined}
		<Options
			bind:readProfile={readCase.profile}
			classes={['mt-4']}
			{refreshState}
			fromCase={true} />
	{/if}

	<Charts datasets={charts}>Alle Bewertungen in diesem Fall</Charts>
</section>
