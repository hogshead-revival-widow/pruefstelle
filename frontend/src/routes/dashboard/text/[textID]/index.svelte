<script context="module" lang="ts">
	import { makePruefstelle, type ps } from '$lib/api';

	export const load = async ({ fetch, params, url }) => {
		const { textID } = params;
		const pruefstelle = makePruefstelle({ customFetch: fetch });
		const readText = await pruefstelle.readText(textID);

		return { props: { readText } };
	};
</script>

<script lang="ts">
	import Text from '$lib/components/Text.svelte';
	import SelectContext from '$lib/components/SelectContext.svelte';
	export let readText: ps.TextRead;
</script>

<section class="mr-10">
	<Text {readText} />
</section>

<section class="max-w-sm mt-8">
	<SelectContext selectFor={readText} />
</section>
