<script lang="ts" context="module">
	import { makePruefstelle } from '$lib/api';

	const minQueryLength = 3;

	export const load = async ({ fetch, url }) => {
		let title = url.searchParams.get('title');
		let category_name = url.searchParams.get('category_name');

		if (title !== null && title.length < minQueryLength) {
			title = null;
		}
		if (category_name !== null && category_name.length < minQueryLength) {
			category_name = null;
		}
		if (title === null && category_name === null) {
			throw new Error('invalid search');
		}

		const query = { size: 50 };
		// @ts-ignore
		if (title !== null) query.title = title;
		// @ts-ignore
		if (category_name !== null) query.category_name = category_name;

		const pruefstelle = makePruefstelle({ customFetch: fetch });
		const readPagedCaseIDs = await pruefstelle.searchCases(query);

		return { props: { readPagedCaseIDs, query } };
	};
</script>

<script lang="ts">
	import PagedSearchResult from '$lib/components/case/PagedSearchResult.svelte';
	import { type ps, Pruefstelle } from '$lib/api';

	export let readPagedCaseIDs: ps.PageUUID;
	export let query;

	const toPageSearch = async (_, page, size) => {
		query.page = page;
		query.size = size;
		readPagedCaseIDs = await Pruefstelle.searchCases(query);
		currentPage = page;
	};

	export let currentPage = undefined;
</script>

<section>
	<PagedSearchResult {readPagedCaseIDs} {toPageSearch} />
</section>
