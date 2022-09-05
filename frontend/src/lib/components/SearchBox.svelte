<script lang="ts">
	import { goto } from '$app/navigation';
	import { focusElement } from '$lib/utils';

	let searchValue = '';
	let oldValue = '';
	const search = ({ forced = false } = {}) => {
		const isValidSearch = searchValue.replace(oldValue, '').length > 2 && searchValue.length >= 3;
		if (forced || isValidSearch) {
			goto(`/dashboard/case/search?title=${searchValue}&category_name=${searchValue}`, {
				keepfocus: true
			});
			oldValue = searchValue;
		}
	};
</script>

<form
	action="/dashboard/case/search"
	method="get"
	on:submit|preventDefault={() => search({ forced: true })}>
	<input
		id="search-button"
		type="text"
		name="title"
		on:keyup={() => search()}
		bind:value={searchValue}
		placeholder="Fall suchen..."
		class="input input-sm input-bordered search" />
	<input type="hidden" id="category_name" name="category_name" bind:value={searchValue} />
	<button
		class="btn btn-square btn-sm btn-ghost"
		on:click|preventDefault={() =>
			searchValue.length >= 3 ? search({ forced: true }) : focusElement('search-button')}>
		<i class="fas fa-search" />
	</button>
</form>
