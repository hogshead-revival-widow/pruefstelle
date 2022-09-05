<script lang="ts">
	import type { DatasetWithMeta } from '$lib/scripts/charts';

	import Chart from './BarChart.svelte';
	import Card from '$lib/components/basic/Card.svelte';

	export let classes = [];
	classes = ['mt-4', 'sidebar', ...classes];
	export let datasets: DatasetWithMeta[] | undefined;
</script>

{#if datasets !== undefined && datasets.some((dataset) => dataset.dataset.good.length > 0 || dataset.dataset.bad.length > 0)}
	<article class={classes.join(' ')}>
		<Card startHidden={true}>
			<svelte:fragment slot="title">Verteilung Bewertungen</svelte:fragment>

			<div class="prose">
				<p><slot /></p>
				<p class="text-sm">
					Tipp: Fahre mit deiner Maus über den Farbbalken, um den Bezug der Bewertung zu sehen.
				</p>
			</div>
			{#each datasets as dataset}
				<Chart {...dataset} />
			{/each}
		</Card>
	</article>
{/if}
