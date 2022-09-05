<script context="module" lang="ts">
	import { makePruefstelle, Pruefstelle, type ps } from '$lib/api';

	export const load = async ({ fetch, params }) => {
		const { caseID } = params;
		const { documentID } = params;
		const pruefstelle = makePruefstelle({ customFetch: fetch });
		const readDocument = await pruefstelle.readDocument(documentID);
		const readReports = await pruefstelle.readDocumentReport(documentID, caseID);
		const readProfile = await pruefstelle.readProfileFromCase(caseID);
		return { props: { documentID, caseID, readDocument, readReports, readProfile } };
	};
</script>

<script lang="ts">
	import { fade } from 'svelte/transition';
	import { onMount } from 'svelte';

	import Document from '$lib/components/Document.svelte';
	import Options from '$lib/components/case/Options.svelte';
	import Charts from '$lib/components/chart/Charts.svelte';
	import SelectContext from '$lib/components/SelectContext.svelte';

	import { showModal } from '$lib/scripts/modal';

	import EvaluationModal from '$lib/components/evaluation/EvaluationModal.svelte';
	import StatusResearchQuality from '$lib/components/ResearchQuality/StatusResearchQuality.svelte';
	import { needsReload } from '$lib/api/utils';
	import { reloader } from '$lib/scripts/reloader';
	import { getCharts } from '$lib/scripts/charts';

	export let documentID: string;
	export let caseID: string;
	export let readDocument: ps.DocumentRead;
	export let readReports: ps.ReportWithPoints[];
	export let readProfile: ps.ProfileRead;

	let showEvaluationClicked = false;
	const showEvaluation = (event) => {
		showEvaluationClicked = true;
		showModal({ id: 'modal-evaluateCards' });
	};

	const refreshState = async (withDocument: boolean = false) => {
		if (withDocument) {
			readDocument = await Pruefstelle.readDocument(documentID);
		}
		readReports = await Pruefstelle.readDocumentReport(documentID, caseID);
		readProfile = await Pruefstelle.readProfileFromCase(caseID);

		return readDocument;
	};

	// Refresh item if it is not fully loaded yet
	if (needsReload(readDocument)) {
		onMount(async () => await reloader(readDocument, () => refreshState(true)));
	}

	$: charts = getCharts(readReports);
</script>

{#if showEvaluationClicked === true}
	<EvaluationModal bind:readReports readDocuments={[readDocument]} {refreshState} />
{/if}
<section class="mr-10" in:fade>
	<Document
		bind:readReports
		bind:readProfile
		{readDocument}
		compactView={false}
		{showEvaluation}
		{caseID} />
</section>

<section class="max-w-sm mt-8" in:fade>
	<StatusResearchQuality item={readDocument} bind:readProfile bind:readReports asStats={true} />

	<Options bind:readProfile classes={['mt-4']} {refreshState} fromCase={false} />

	<Charts datasets={charts}>Alle Bewertungen in diesem Dokument</Charts>

	{#if readDocument.cases.length > 1}
		<SelectContext selectFor={readDocument} classes={['mt-4']} />
	{/if}
</section>
