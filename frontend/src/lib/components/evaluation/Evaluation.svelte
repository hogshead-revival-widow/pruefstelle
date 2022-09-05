<script lang="ts">
	import { fade } from 'svelte/transition';

	import type { ps } from '$lib/api';

	import { Pruefstelle } from '$lib/api';
	import Date from '$lib/components/basic/Date.svelte';
	import Result from '$lib/components/Result.svelte';
	import { getShortIfNeeded } from '$lib/utils';
	import { EvaluationType } from '$lib/api';

	export let readEvaluation: ps.EvaluationRead;
	export let inTableRow = false;
	export let promisedDocument: Promise<ps.DocumentRead> | undefined = undefined;

	let promisedResult = undefined;
	if (inTableRow) promisedResult = Pruefstelle.readResult(readEvaluation.mining_result_id);

	const renderOptions = {
		[EvaluationType.ScoredEvaluation]: {
			isGreen: (value: number) => value === 2,
			isYellow: (value: number) => value === 1,
			isRed: (value: number) => value === 0,
			toWord: (value: number) => {
				if (value === 0) return 'unpassend';
				if (value === 1) return 'hilfreich';
				if (value === 2) return 'passend';
			}
		},
		[EvaluationType.CorrectnessEvaluation]: {
			isGreen: (value: number) => value === 1,
			isYellow: (value: number) => false,
			isRed: (value: number) => value === 0,
			toWord: (value: number) => (value === 0 ? 'falsch' : 'korrekt')
		}
	};

	let isGreen = false,
		isYellow = false,
		isRed = false;

	let word = '';

	$: {
		const render = renderOptions[readEvaluation.discriminator];
		isGreen = render.isGreen(readEvaluation.value);
		isYellow = render.isYellow(readEvaluation.value);
		isRed = render.isRed(readEvaluation.value);
		word = render.toWord(readEvaluation.value);
	}
</script>

{#if inTableRow}
	{#key readEvaluation.value}
		<td in:fade>
			<div
				class="badge rounded-none border-none"
				class:evaluation-good={isGreen}
				class:evaluation-ok={isYellow}
				class:evaluation-bad={isRed}>
				{word}
			</div>
		</td>
	{/key}
	<td>
		{#await promisedResult then resultRead}
			<Result {resultRead} />
		{/await}
	</td>

	{#key readEvaluation.date}
		<td in:fade>
			<Date date={readEvaluation.date} />
		</td>
	{/key}

	{#if promisedDocument !== undefined}
		{#await promisedDocument then readDocument}
			<td>
				in:
				<a href="/dashboard/document/{readDocument.id}" sveltekit:prefetch class="text-ellipsis"
					>{getShortIfNeeded(readDocument.title)}</a>
			</td>
		{/await}
	{/if}
{/if}
