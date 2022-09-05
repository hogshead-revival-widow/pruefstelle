<script lang="ts">
	import { fade } from 'svelte/transition';

	import { user } from '$lib/stores';
	import { isCase, isDocument, isText, type ps } from '$lib/api';
	import type { CaseDocumentText } from '$lib/api/utils';

	export let readReports: ps.ReportWithPoints[];
	export let forItem: CaseDocumentText;
	export let inList = true;

	const { id } = forItem;
	let path: 'case' | 'document' | 'text';

	if (isText(forItem)) {
		path = 'text';
	} else if (isDocument(forItem)) {
		path = 'document';
	} else if (isCase(forItem)) {
		path = 'case';
	}

	$: userHasEvaluations = readReports.some((report) =>
		report.item_results.some((result) =>
			result.evaluations.some((evaluation) => evaluation.creator_id === $user.id)
		)
	);

	const link = `<a href="/dashboard/user/has/evaluated/${path}/${id}" class="action-button" sveltekit:prefetch>
				<span class="note-link" />Bewertungen
			</a>`;
</script>

{#if userHasEvaluations}
	{#if inList}
		<li in:fade|local>
			{@html link}
		</li>
	{:else}
		{@html link}
	{/if}
{/if}
