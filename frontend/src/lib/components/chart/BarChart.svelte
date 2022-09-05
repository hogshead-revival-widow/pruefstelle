<script lang="ts">
	import type { Dataset } from '$lib/scripts/charts';
	import Bar from 'svelte-chartjs/src/Bar.svelte';

	import { isDark } from '$lib/stores';
	import FAQ from '$lib/components/faq/FAQ.svelte';
	import Card from '$lib/components/basic/Card.svelte';

	export let dataset: Dataset;
	export let title: string;
	export let titleClasses: string[];
	export let classes = [];
	export let faqForTerm = undefined;

	$: color = $isDark ? '#A6ADBA' : '#1F2937';

	$: data = {
		datasets: [
			{
				label: 'positiv',
				backgroundColor: '#16a34a', // cf. app.css:evaluation-good
				data: dataset.good,
				barThickness: 8
			},
			{
				label: 'negativ',
				backgroundColor: '#dc2626', // cf. app.css:evaluation-ok
				data: dataset.bad,
				barThickness: 8
			}
		]
	};
	$: options = {
		maintainAspectRatio: false,
		tooltips: {
			mode: 'index',
			intersect: false
		},
		hover: {
			mode: 'nearest',
			intersect: true
		},
		plugins: {
			legend: {
				labels: {
					color: color
				}
			}
		},

		scales: {
			xAxes: {
				display: false,
				stacked: true,
				gridLines: {
					offsetGridLines: true
				},
				ticks: {
					color: color
				}
			},
			yAxes: {
				display: true,
				stacked: true,
				ticks: {
					color: color,
					precision: 0
				}
			}
		}
	};

	$: show = dataset.good.length > 0 || dataset.bad.length > 0;
</script>

{#if show}
	<Card {classes} hasBackground={false}>
		<svelte:fragment slot="title">
			{#if faqForTerm !== undefined}
				<span class={titleClasses.join(' ')} /><FAQ forTerm={faqForTerm}>{title}</FAQ>
			{:else}
				<span class={titleClasses.join(' ')} />{title}
			{/if}
		</svelte:fragment>
		<div>
			<Bar {data} {options} />
		</div>
	</Card>
{/if}
