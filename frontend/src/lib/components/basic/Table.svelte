<script>
	export let classes = [];
	classes = ['table', ...classes];
	export let isCompact = true;
	export let isZebra = true;
	export let hasHeader = true;

	if (isZebra) {
		classes.push('table-zebra');
	}
	if (isCompact) {
		classes.push('table-compact');
	}
</script>

<table class={classes.join(' ')}>
	{#if hasHeader}
		<thead>
			<tr>
				<slot name="header" />
			</tr>
		</thead>
	{/if}

	<tbody>
		<slot />
	</tbody>
</table>
