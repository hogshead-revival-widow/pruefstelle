<script lang="ts">
	import { fade } from 'svelte/transition';

	import { user } from '$lib/stores';
	import type { ps } from '$lib/api';

	export let readReports: ps.ReportWithPoints[];
	export let showEvaluation: (event) => void;
	export let inList = true;

	const RESEARCH_QUALITY_CONSTRAINT_NEEDED_USERS: keyof ps.ProfileRead =
		'research_quality_constraint_needed_users';

	const neededUsersConstraintFailed = (readReports: ps.ReportWithPoints[]) =>
		readReports.some((report) =>
			report.item_results_failed_constraints
				.map((constraint) => constraint.constraint_name)
				.includes(RESEARCH_QUALITY_CONSTRAINT_NEEDED_USERS)
		);

	const currentUserHasNotEvaluatedEverything = (readReports: ps.ReportWithPoints[]) =>
		!readReports.every((report) =>
			report.item_results.every((result) =>
				result.evaluations.some((evaluation) => evaluation.creator_id === $user.id)
			)
		);

	$: notAllEvaluated = readReports.some((report) => !report.item_results_all_evaluated);
	$: itemNeedsEvaluation =
		notAllEvaluated || // have all items at least one evlauation?
		// can the user do something about missing evaluations as enforced by the needed users constraint?
		(currentUserHasNotEvaluatedEverything(readReports) && neededUsersConstraintFailed(readReports));
</script>

{#if itemNeedsEvaluation}
	{#if inList}
		<li in:fade|local>
			<button class="action-button" on:click={showEvaluation}>
				<i class="fas fa-gavel" />
				bewerten
			</button>
		</li>
	{:else}
		<button class="action-button" on:click={showEvaluation}>
			<i class="fas fa-gavel" />
			bewerten
		</button>
	{/if}
{/if}
