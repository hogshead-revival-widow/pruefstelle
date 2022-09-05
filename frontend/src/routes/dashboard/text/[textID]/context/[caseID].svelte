<script context="module" lang="ts">
	import { makePruefstelle, Pruefstelle, type ps } from '$lib/api';

	export const load = async ({ fetch, params }) => {
		const { caseID } = params;
		const { textID } = params;
		const pruefstelle = makePruefstelle({ customFetch: fetch });
		const readText = await pruefstelle.readText(textID);
		const readReports = await pruefstelle.readItemReport(textID, caseID);
		const readProfile = await pruefstelle.readProfileFromCase(caseID);
		const readDocument = await pruefstelle.readDocument(readText.document_id);
		return {
			props: { textID, caseID, readText, readReports: [readReports], readProfile, readDocument }
		};
	};
</script>

<script lang="ts">
	import { fade } from 'svelte/transition';
	import { onMount } from 'svelte';

	import Text from '$lib/components/Text.svelte';
	import Options from '$lib/components/case/Options.svelte';
	import Charts from '$lib/components/chart/Charts.svelte';
	import SelectContext from '$lib/components/SelectContext.svelte';

	import { showModal } from '$lib/scripts/modal';

	import EvaluationModal from '$lib/components/evaluation/EvaluationModal.svelte';
	import StatusResearchQuality from '$lib/components/ResearchQuality/StatusResearchQuality.svelte';
	import { reloader } from '$lib/scripts/reloader';
	import { needsReload } from '$lib/api/utils';
	import { getCharts } from '$lib/scripts/charts';

	export let textID: string;
	export let caseID: string;
	export let readText: ps.TextRead;
	export let readReports: ps.ReportWithPoints[];
	export let readProfile: ps.ProfileRead;
	export let readDocument: ps.DocumentRead;

	let showEvaluationClicked = false;
	const showEvaluation = (event) => {
		showEvaluationClicked = true;
		showModal({ id: 'modal-evaluateCards' });
	};

	const refreshState = async (withText = false) => {
		if (withText) {
			readText = await Pruefstelle.readText(textID);
		}
		const readReport = await Pruefstelle.readItemReport(textID, caseID);
		readReports = [readReport];
		readProfile = await Pruefstelle.readProfileFromCase(caseID);

		return readText;
	};

	if (needsReload(readText))
		onMount(async () => await reloader(readText, () => refreshState(true)));

	$: charts = getCharts(readReports);
</script>

{#if showEvaluationClicked === true}
	<EvaluationModal bind:readReports readDocuments={[readDocument]} {refreshState} />
{/if}
<section class="mr-10" in:fade>
	<Text
		bind:readReports
		bind:readProfile
		{readText}
		compactView={false}
		{showEvaluation}
		{caseID} />
</section>

<section class="max-w-sm mt-8" in:fade>
	<StatusResearchQuality item={readText} bind:readProfile bind:readReports asStats={true} />

	<Options bind:readProfile classes={['mt-4']} {refreshState} fromCase={false} />

	<Charts datasets={charts}>Alle Bewertungen in diesem Text</Charts>

	{#if readDocument.cases.length > 1}
		<SelectContext selectFor={readDocument} classes={['mt-4']} />
	{/if}
</section>
