<script lang="ts">
	import Modal from '$lib/components/Modal.svelte';
	import Card from '$lib/components/basic/Card.svelte';
	import ImportCollection from '$lib/components/new/ImportCollection.svelte';
	import AddDocument from '$lib/components/new/AddDocument.svelte';
	import AddedDocument from './AddedDocument.svelte';

	import { showModal } from '$lib/scripts/modal';
	import type { Drafts, CategoriesByType } from '$lib/scripts/new';

	export let drafts: Drafts;
	let unique = {};
	let reloadDocument = 0;

	export let readCategories: CategoriesByType;
</script>

<Card classes={['w-96', 'mx-auto']}>
	<button class="btn-primary btn gap-2 btn-lg" on:click={() => showModal({ id: 'add-document' })}
		><i class="fas fa-plus" />Dokument
	</button>

	<button
		class="btn-primary btn gap-2 btn-lg"
		on:click={() => {
			unique = {};
			showModal({ id: 'add-from-collection' });
		}}><i class="fas fa-file-import" />Sammelmappe</button>
</Card>

<Modal id="add-document" showCloseButton={true} wrapInBox={true}>
	<AddDocument bind:drafts modalID="add-document" {readCategories} />
</Modal>

{#key unique}
	<Modal id="add-from-collection" showCloseButton={true}>
		<ImportCollection bind:drafts modalID={'add-from-collection'} />
	</Modal>
{/key}

{#if drafts.length > 0}
	<Card isHideable={false} classes={['mt-4', 'mb-4', 'bg-base-300', 'p-3', 'shadow-lg']}>
		<h1 slot="title">Angelegte Dokumente</h1>

		{#each drafts as readDocument (readDocument.id)}
			{#key reloadDocument}
				<Modal id={`edit-document-${readDocument.id}`} wrapInBox={true}>
					<AddDocument
						bind:reloadDocument
						{readCategories}
						editDocument={readDocument}
						bind:drafts
						modalID={`edit-document-${readDocument.id}`} />
				</Modal>

				<AddedDocument bind:readDocument {readCategories} />
			{/key}
		{/each}
	</Card>
{/if}
