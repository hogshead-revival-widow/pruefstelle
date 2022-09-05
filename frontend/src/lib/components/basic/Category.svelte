<script lang="ts">
	import type { ps } from '$lib/api';

	export let category: ps.CategoryRead;
	export let compactView = false;
	export let isSecondary = false;

	const categoryClass = isSecondary ? 'other-category' : 'category';
</script>

{#if compactView}
	<span class={categoryClass}>{category.name}</span>
{:else}
	<div class={categoryClass}>
		{category.name}
	</div>

	{#if category?.source}
		<div class="other-category">
			{category.name}
		</div>
	{/if}
{/if}
