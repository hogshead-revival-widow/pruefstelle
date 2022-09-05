<script lang="ts">
	import { fade } from 'svelte/transition';
	export let isGood: boolean;
	export let points: number;
	export let inHeader: boolean;
</script>

{#if !inHeader}
	<div
		in:fade|local
		class="badge border-none"
		class:research-quality-good={isGood}
		class:research-quality-okay={!isGood}>
		Recherchegüte: {points.toFixed(2).replace('.00', '')} %
	</div>
{:else}
	<span
		class:other-research-quality-okay={!isGood}
		class:other-research-quality-good={isGood}
		in:fade>
		{points.toFixed(2).replace('.00', '')} %
	</span>
{/if}
