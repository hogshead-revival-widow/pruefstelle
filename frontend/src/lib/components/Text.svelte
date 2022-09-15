<script lang="ts">
	import type { ps } from '$lib/api';
	import { FAQ } from './faq';
	import { fade } from 'svelte/transition';
	import {
		Card,
		ChangeEvaluationButton,
		ActionBar,
		UsedServices,
		Category,
		Title,
		ExportButton,
		EvaluateButton
	} from '$lib/components/basic';
	import StatusResearchQuality from '$lib/components/ResearchQuality/StatusResearchQuality.svelte';
	import { hasFinished, isEntity, isKeyword } from '$lib/api/utils';
	import Result from './Result.svelte';

	export let readText: ps.TextRead;
	export let isHideable = false;
	export let startHidden = false;
	export let classes = [];
	export let showEvaluation: (event) => void | undefined = undefined;
	export let readReports: ps.ReportWithPoints[] = undefined;
	export let readProfile: ps.ProfileRead = undefined;
	export let caseID = undefined;
	export let compactView = false;

	let showResults = false;
	let hasEvaluationData = readReports !== undefined && readProfile !== undefined;

	$: showEvaluateButton =
		hasFinished(readText) && showEvaluation !== undefined && readReports !== undefined;
</script>

<article>
	<Card {isHideable} {startHidden} {classes}>
		<svelte:fragment slot="title">
			<Title id={readText.id} title={readText.title} path="text" withContext={caseID} />

			<Category category={readText.category} />
			<Category category={readText.source_category} />

			{#if hasEvaluationData && compactView}
				<StatusResearchQuality item={readText} {readReports} {readProfile} />
			{/if}
		</svelte:fragment>

		<header slot="header">
			<ActionBar>
				{#if hasEvaluationData}
					<li>
						<ExportButton
							title={readText.title}
							toExport={[readReports, readProfile]}
							id={readText.id} />
					</li>
				{/if}

				{#if showEvaluateButton}
					<EvaluateButton {readReports} {showEvaluation} />
				{/if}

				{#if hasEvaluationData}
					<ChangeEvaluationButton {readReports} forItem={readText} />
				{/if}
			</ActionBar>
		</header>

		{#if caseID !== undefined}
			<Title id={caseID} title="Bezugsfall" path="case" />
		{/if}

		<p>
			Dienste: <UsedServices services={new Set(readText.mining_jobs.map((job) => job.service))} />
			<FAQ forTerm={'services'} />
		</p>

		{#if readText.mining_results.length > 0}
			<div class="mt-2 w-96 italic" in:fade|local>
				<div class="prose">
					<h4 class=" not-italic">Mining-Ergebnisse</h4>
				</div>
				{#each readText.mining_results as result}
					<span
						class="m-1 {isKeyword(result)
							? 'keyword'
							: isEntity(result)
							? `named-entity ${result.type}`
							: 'topic'}"
						id="result-{result.id}"
						>{isKeyword(result)
							? result.keyword
							: isEntity(result)
							? result.label
							: result.keywords.map((keyword) => keyword.keyword).join('-')}</span>
				{/each}
			</div>
		{/if}
		<div class="prose mt-2 w-96 italic">
			<h4 class="not-italic">Text</h4>
			{#each readText.content.split('\n') as paragraph}
				<p class="ml-2 text-sm" in:fade|local>{@html paragraph}</p>
			{/each}
		</div>
	</Card>
</article>
