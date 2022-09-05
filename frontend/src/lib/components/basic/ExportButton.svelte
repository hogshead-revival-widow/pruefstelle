<script lang="ts">
	import { getShortIfNeeded, makeDataURL } from '$lib/utils';

	export let id: string;
	export let title: string = '';
	export let toExport: any[];

	const placeholder = `#export-${id}`;
	let exportValue = placeholder;

	const saferFileName = getShortIfNeeded(title, 15).replace(/[\W]+/g, '');
</script>

<a
	href={exportValue}
	class="action-button"
	download="Export {saferFileName}.json"
	on:focus={(event) => {
		if (exportValue === placeholder) {
			exportValue = makeDataURL(toExport);
		} else {
			event.preventDefault();
		}
	}}>
	<i class="fas fa-up-right-from-square" />exportieren
</a>
