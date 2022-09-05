<script lang="ts">
	import type { ps } from '$lib/api';

	export let services: Set<ps.TextWorkflow>;
	export let useList = false;
</script>

{#if useList}
	<ul class="space-y-1">
		{#each [...services] as service}
			<li>
				<span class="service-{service}" />
			</li>
		{/each}
	</ul>
{:else}
	{#each [...services] as service}
		<span class="service-{service} mr-2" />
	{/each}
{/if}
