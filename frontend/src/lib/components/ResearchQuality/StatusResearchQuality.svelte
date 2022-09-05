<script lang="ts">
	import FAQ from '../faq/FAQ.svelte';

	import type { ps } from '$lib/api';
	import { user } from '$lib/stores';
	import ResearchQuality from './ResearchQuality.svelte';
	import { fade } from 'svelte/transition';
	import { hasError, hasFinished, needsReload } from '$lib/api/utils';

	export let readReports: ps.ReportWithPoints[];
	export let readProfile: ps.ProfileRead;
	export let item: ps.CaseRead | ps.DocumentRead | ps.TextRead | ps.DocumentReadWithoutCases;
	export let inHeader = true;
	export let asStats = false;

	$: statusError = hasError(item);
	$: statusReload = needsReload(item);
	$: statusFinished = hasFinished(item);

	$: noReports = readReports.length === 0;
	$: totalPoints =
		readReports.map((report) => report.points).reduce((acc, points) => acc + points, 0) /
		(noReports ? 1 : readReports.length);

	$: isGood = totalPoints > readProfile.research_quality_good_threshold;

	$: constraintsFailed = readReports.some((report) =>
		report.item_results_failed_constraints.some((constraint) =>
			constraint.expected_value === 1 ? false : true
		)
	);

	$: failedConstraints = readReports
		.map((report) =>
			report.item_results_failed_constraints.map((constraint) => [
				constraint.found_value,
				constraint.expected_value
			])
		)
		.flat();
	$: noItems = noReports || readReports.some((report) => report.item_results_total === 0);
	$: somethingToEvaluateLeft =
		readReports.some((report) => !report.item_results_all_evaluated) || constraintsFailed;
	$: isDone =
		!somethingToEvaluateLeft &&
		!noItems &&
		readReports.every((report) => report.item_results_all_evaluated);

	let leftToEvaluateByCurrentUser = 0;
	$: if (somethingToEvaluateLeft) {
		leftToEvaluateByCurrentUser = readReports
			.map((report) =>
				report.item_results.map((result) =>
					result.evaluations.some((evaluation) => evaluation.creator_id == $user.id) ? 1 : 0
				)
			)
			.flat()
			// @ts-ignore
			.reduce((pv, cv) => pv + cv);

		leftToEvaluateByCurrentUser =
			readReports.map((report) => report.item_results_total).reduce((pv, cv) => pv + cv) -
			leftToEvaluateByCurrentUser;
	}
</script>

{#if asStats}
	<div class="stats relative shadow bg-base-100" in:fade|local>
		<!-- Research Quality -->

		<div class="stat">
			<div
				class="stat-figure text-5xl"
				class:text-secondary={noItems || somethingToEvaluateLeft || !statusFinished}
				class:text-success={isGood && isDone}
				class:text-warning={!isGood && isDone}>
				<i
					class="fas"
					class:fa-pulse={statusReload}
					class:fa-spinner={statusReload}
					class:fa-star={statusFinished && isGood && isDone}
					class:fa-star-half={statusFinished && !isGood && isDone}
					class:fa-question={statusFinished && (noItems || somethingToEvaluateLeft)} />
			</div>

			{#if statusFinished}
				<div class="stat-title">Recherchegüte</div>
			{/if}

			{#if !statusReload && !statusError}
				<div class="stat-value">
					{#if isDone}
						{totalPoints.toFixed(2).replace('.00', '')} %
					{:else if somethingToEvaluateLeft}
						offen
					{:else if noItems}
						unbekannt
					{/if}
				</div>
			{:else}
				<div class="stat-value">
					{#if statusReload}
						Mining läuft
					{/if}

					{#if statusError}
						<a
							href="mailto:{import.meta.env
								.VITE_MAIL_CONTACT_ERROR}?subject=[Prüfstelle] Fehler ({item.id})&body=Da ist etwas schiefgelaufen."
							>Mining:<br />Fehler</a>
					{/if}
				</div>
			{/if}
		</div>

		{#if !statusReload && !statusError}
			<div class="stat">
				{#if isDone}
					<div class="stat-value text-5xl mt-2">
						<FAQ forTerm="researchQualityContext" fixedSize={false} />
					</div>
				{:else if somethingToEvaluateLeft}
					<div class="stat-value text-5xl mt-2">
						<FAQ forTerm="noResearchQuality" fixedSize={false} />
					</div>
				{/if}
			</div>
		{/if}

		{#if statusError}
			<div class="stat">
				<div class="stat-value text-5xl mt-2 text-secondary">
					<a
						href="mailto:{import.meta.env
							.VITE_MAIL_CONTACT_ERROR}?subject=[Prüfstelle] Fehler ({item.id})&body=Da ist etwas schiefgelaufen."
						><i class="fas fa-share" /></a>
				</div>
			</div>
		{/if}
	</div>

	{#if statusFinished && somethingToEvaluateLeft && (leftToEvaluateByCurrentUser > 0 || constraintsFailed)}
		<div class="stats relative shadow bg-base-100 sidebar mt-4 " transition:fade|local>
			<div class="stat">
				<div class="stat-title mb-4">Das ist offen</div>

				<ul class="list-disc stat-desc ml-4">
					{#if leftToEvaluateByCurrentUser > 0}
						<li>{leftToEvaluateByCurrentUser} Bewertungen <strong>von dir</strong></li>
					{/if}
					{#if constraintsFailed}
						<li>
							Es haben noch nicht genügend ({failedConstraints[0][0]}/{failedConstraints[0][1]})
							<br />
							Nutzer:innen vollständig bewertet (vgl. Fallprofil)
						</li>
					{/if}
				</ul>
			</div>
		</div>
	{/if}
{/if}

<!-- don't render as stat-->
{#if !asStats}
	{#if !statusFinished}
		{#if statusError}
			Fehler
		{:else if statusReload}
			Warte...
		{/if}
	{:else if statusFinished}
		{#if isDone}
			<ResearchQuality {inHeader} points={totalPoints} {isGood} />
		{:else if somethingToEvaluateLeft}
			<div class="badge badge-neutral gap-2" class:badge-outline={!inHeader} in:fade>
				<FAQ forTerm="noResearchQuality">offen</FAQ>
			</div>
		{:else if noItems}
			<div class="badge badge-neutral gap-2" class:badge-outline={!inHeader} in:fade>
				<FAQ forTerm="noResearchQuality">unbekannt</FAQ>
			</div>
		{/if}
	{/if}
{/if}
