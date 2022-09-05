<script lang="ts">
	import type { ps } from '$lib/api';
	import { FAQ } from './faq';
	import {
		Card,
		Table,
		ChangeEvaluationButton,
		ActionBar,
		UsedServices,
		Category,
		Title,
		ExportButton,
		EvaluateButton
	} from '$lib/components/basic';
	import StatusResearchQuality from '$lib/components/ResearchQuality/StatusResearchQuality.svelte';
	import { hasFinished } from '$lib/api/utils';

	export let readDocument: ps.DocumentRead;
	export let isHideable = false;
	export let startHidden = false;
	export let classes = [];
	export let showEvaluation: (event) => void | undefined = undefined;
	export let readReports: ps.ReportWithPoints[] = undefined;
	export let readProfile: ps.ProfileRead = undefined;
	export let caseID = undefined;
	export let noTexts = 'Dieses Dokument hat keine Texte';

	export let compactView = false;

	let hasEvaluationData = readReports !== undefined && readProfile !== undefined;
	$: showEvaluateButton =
		hasFinished(readDocument) && showEvaluation !== undefined && readReports !== undefined;
</script>

<article>
	<Card {isHideable} {startHidden} {classes}>
		<svelte:fragment slot="title">
			<Title id={readDocument.id} title={readDocument.title} path="document" withContext={caseID} />

			<Category category={readDocument.category} />

			{#if hasEvaluationData && compactView}
				<StatusResearchQuality item={readDocument} {readReports} {readProfile} />
			{/if}
		</svelte:fragment>

		{#if caseID !== undefined}
			<Title id={caseID} title="Bezugsfall" path="case" />
		{/if}

		<header slot="header">
			<ActionBar>
				{#if hasEvaluationData}
					<li>
						<ExportButton
							title={readDocument.title}
							toExport={[readReports, readProfile]}
							id={readDocument.id} />
					</li>
				{/if}

				{#if showEvaluateButton}
					<EvaluateButton {readReports} {showEvaluation} />
				{/if}

				{#if hasEvaluationData}
					<ChangeEvaluationButton {readReports} forItem={readDocument} />
				{/if}
			</ActionBar>
		</header>

		{#if readDocument.items.length > 0}
			<Table classes={['overflow-x-auto', 'w-full', 'mt-4']}>
				<svelte:fragment slot="header">
					<th>Text</th>
					<th>Kategorie</th>
					<th>Quelle</th>
					<th title="Genutzte Mining-Dienste"
						>Dienste <FAQ forTerm={'services'} classes={['mr-1', 'ml-1']} />
					</th>
					{#if hasEvaluationData}<th>Güte</th>{/if}
				</svelte:fragment>
				{#each readDocument.items as readItem}
					{#if readItem.discriminator === 'text'}
						<tr>
							<td>
								<Title id={readItem.id} title={readItem.title} path="text" withContext={caseID} />
							</td>
							<td><Category category={readItem.category} isSecondary={true} /> </td>
							<td><Category category={readItem.source_category} isSecondary={true} /> </td>

							<td>
								<UsedServices services={new Set(readItem.mining_jobs.map((job) => job.service))} />
							</td>

							{#if hasEvaluationData}
								<td>
									<StatusResearchQuality
										item={readItem}
										readReports={[readReports.find((report) => report.item_id === readItem.id)]}
										{readProfile} />
								</td>
							{/if}
						</tr>
					{/if}
				{/each}
			</Table>
		{:else}
			<p class="prose">{noTexts}</p>
		{/if}
	</Card>
</article>
