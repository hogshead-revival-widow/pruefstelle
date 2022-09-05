<script lang="ts">
	interface ToPageCallbackI {
		(itemId: string | undefined, page: number, size: number): void;
	}

	interface ToPage {
		(itemId: string | undefined, page: number, size: number, callback: ToPageCallbackI): void;
	}

	export let page: number, size: number, total: number;
	export let id: string | undefined = undefined;
	export let callback: ToPageCallbackI;

	const toPage: ToPage = (itemId, page, size, callback) => callback(itemId, page, size);

	const firstPage = 1;
	const lastPage = Math.ceil(total / size);
	const previousPage = page - 1;
	const nextPage = page + 1;

	const pages = [
		{ page: firstPage, show: page !== 1, isInvisible: false, label: firstPage },
		{ page: previousPage, show: true, isInvisible: (page - 1) * size < 1, label: '«' },
		{ page, show: true, isInvisible: false, label: page },
		{ page: nextPage, show: true, isInvisible: total - page * size <= 0, label: '»' },
		{ page: lastPage, show: page !== lastPage, isInvisible: false, label: lastPage }
	];
</script>

{#if size < total}
	<div class="btn-group justify-center gap-1">
		{#each pages.filter((page) => page.show) as thisPage}
			<button
				class="btn-sm rounded"
				class:btn-active={thisPage.page === page}
				class:btn-disabled={thisPage.isInvisible}
				on:click={() => toPage(id, thisPage.page, size, callback)}>{thisPage.label}</button>
		{/each}
	</div>
{/if}
