<script lang="ts">
	import { FAQ } from '$lib/components/faq';
	import {
		Card,
		Table,
		Title,
		Category,
		ActionBar,
		UsedServices,
		ExportButton,
		ChangeEvaluationButton,
		EvaluateButton
	} from '$lib/components/basic';
	import StatusResearchQuality from '$lib/components/ResearchQuality/StatusResearchQuality.svelte';
	import { user } from '$lib/stores';
	import { Pruefstelle, type ps } from '$lib/api';
	import { addAlert } from '$lib/scripts/alerts';
	import { hasFinished } from '$lib/api/utils';

	export let readCase: ps.CaseRead;
	export let isHideable = false;
	export let startHidden = false;
	export let classes = [];
	export let compactView = false;
	export let showEvaluation: (event) => void | undefined = undefined;
	export let readCaseReports: ps.ReportWithPoints[] = undefined;
	export let showQuality = true;

	let showAllDocuments = !compactView;
	let showDocumentsToggle = !showAllDocuments;
	let showResearchQuality = compactView;

	$: showEvaluateButton =
		hasFinished(readCase) &&
		!compactView &&
		showEvaluation !== undefined &&
		readCaseReports !== undefined;

	$: isWatchingCase = readCase.watchers.map((watcher) => watcher.id).includes($user.id);
</script>

<article>
	<Card {isHideable} {startHidden} {classes}>
		<svelte:fragment slot="title">
			<Title id={readCase.id} title={readCase.title} path="case" />

			<Category category={readCase.category} />

			{#if showResearchQuality && readCaseReports !== undefined}
				<StatusResearchQuality
					item={readCase}
					readReports={readCaseReports}
					readProfile={readCase.profile} />
			{/if}
		</svelte:fragment>

		<header slot="header">
			<ActionBar>
				{#if showDocumentsToggle && readCase.documents.length > 0}
					<li>
						<button class="action-button" on:click={() => (showAllDocuments = !showAllDocuments)}
							><i class="fas {showAllDocuments ? 'fa-eye' : 'fa-eye-slash'}" /> Dokumente
						</button>
					</li>
				{/if}

				{#if readCaseReports !== undefined}
					<li>
						<ExportButton
							title={readCase.title}
							toExport={[readCaseReports, readCase.profile]}
							id={readCase.id} />
					</li>
				{/if}

				<li>
					<button
						class="action-button"
						on:click={async () => {
							try {
								readCase = await Pruefstelle.toggleWatchCase(readCase.id);
							} catch (error) {
								const message = 'Kann Fall nicht beobachten';
								const type = 'error';
								addAlert({ message, type });
							}
						}}>
						<i class="fas fa-star" class:disabled={!isWatchingCase} /> beobachten
					</button>
				</li>

				{#if showEvaluateButton}
					<EvaluateButton readReports={readCaseReports} {showEvaluation} />
				{/if}

				{#if readCaseReports !== undefined}
					<ChangeEvaluationButton readReports={readCaseReports} forItem={readCase} />
				{/if}
			</ActionBar>
		</header>

		{#if showAllDocuments}
			<Table classes={['overflow-x-auto', 'w-full', 'mt-4']}>
				<svelte:fragment slot="header">
					<th>Dokument</th>
					<th>Kategorie</th>
					<th title="Genutzte Mining-Dienste"
						>Dienste <FAQ forTerm={'services'} classes={['mr-1', 'ml-1']} /></th>
					{#if showQuality}
						<th>Güte</th>
					{/if}
				</svelte:fragment>
				{#each readCase.documents as readDocument}
					<tr>
						<td>
							<Title
								id={readDocument.id}
								title={readDocument.title}
								withContext={readCase.id}
								path="document" />
						</td>
						<td>
							<Category category={readDocument.category} isSecondary={true} />
						</td>

						<td>
							<UsedServices
								services={new Set(
									readDocument.items
										.map((item) => item.mining_jobs.map((job) => job.service))
										.flat(2)
								)} />
						</td>

						{#if showQuality}
							<td>
								{#if readCaseReports !== undefined}
									<StatusResearchQuality
										bind:item={readDocument}
										readReports={readCaseReports.filter((report) =>
											readDocument.items.map((item) => item.id).includes(report.item_id)
										)}
										readProfile={readCase.profile} />
								{/if}
							</td>
						{/if}
					</tr>
				{/each}
			</Table>
		{/if}
	</Card>
</article>
