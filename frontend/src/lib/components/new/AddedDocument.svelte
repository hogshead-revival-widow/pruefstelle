<script lang="ts">
	import { fade, fly } from 'svelte/transition';

	import type { ps } from '$lib/api';
	import { Card, Table, ActionBar, UsedServices, Category, Title } from '$lib/components/basic';
	import Modal from '../Modal.svelte';
	import { FAQ } from '../faq';
	import AddText from './AddText.svelte';
	import { showModal } from '$lib/scripts/modal';

	export let readDocument: ps.DocumentRead;
	export let readCategories;
	export let isHideable = true;
	export let startHidden = true;
	export let classes = [];
	export let noTexts = 'Dieses Dokument hat keine Texte';

	const editModalID = `edit-document-${readDocument.id}`;
	let showMore = startHidden;
	const addTextModalID = `add-text-${readDocument.id}`;
	const generateTextModalID = `generate-text-${readDocument.id}`;
</script>

<Modal id={addTextModalID} wrapInBox={true} showCloseButton={true}>
	<AddText modalID={addTextModalID} {readCategories} bind:readDocument />
</Modal>

<Modal id={generateTextModalID} wrapInBox={true} showCloseButton={true}>
	<AddText
		modalID={generateTextModalID}
		{readCategories}
		bind:readDocument
		offerGeneration={true} />
</Modal>

<article>
	<Card {isHideable} {startHidden} {classes} bind:show={showMore}>
		<svelte:fragment slot="title">
			<button
				class="btn btn-ghost"
				title="Dokument ändern"
				on:click={() => showModal({ id: editModalID })}>
				<i class="fa fa-edit  text-lg" />
			</button>
			<Title id={readDocument.id} title={readDocument.title} path="" shortenIfNeeded={false} />
		</svelte:fragment>

		<header slot="header">
			<ActionBar>
				{#if readDocument.items.length > 1}
					<button
						in:fade
						class="btn btn-sm btn-primary gap-2 mr-2 btn-outline"
						on:click={() => {
							showModal({ id: generateTextModalID });
							showMore = true;
						}}>
						<i class="fa fa-plus" /> generieren
					</button>
				{/if}

				<button
					in:fade
					class="btn btn-sm btn-primary gap-2"
					on:click={() => {
						showModal({ id: addTextModalID });
						showMore = true;
					}}><i class="fas fa-plus" />Text</button>

				<div class="divider divider-horizontal" />
			</ActionBar>
		</header>
		<Category category={readDocument.category} />

		{#if readDocument.items.length > 0}
			<Table classes={['overflow-x-auto', 'w-full', 'mt-4']}>
				<svelte:fragment slot="header">
					<th class="text-center">Text</th>
					<th>Kategorie</th>
					<th>Quelle</th>
					<th title="Genutzte Mining-Dienste">
						Dienste <FAQ forTerm={'services'} classes={['mr-1', 'ml-1']} />
					</th>
				</svelte:fragment>

				{#each readDocument.items as readItem (readItem.id)}
					<tr transition:fly|local>
						<td>
							<button
								class="action-button"
								title="Text ändern"
								on:click={() => showModal({ id: `edit-text-${readItem.id}` })}>
								<i class="fa fa-edit  text-lg" />
							</button>
							<Title id={readItem.id} title={readItem.title} path="" shortenToMaxLength={8} />
						</td>
						<td><Category category={readItem.category} isSecondary={true} /> </td>
						<td><Category category={readItem.source_category} isSecondary={true} /> </td>

						<td>
							<UsedServices services={new Set(readItem.mining_jobs.map((job) => job.service))} />
						</td>

						<div>
							<Modal id={`edit-text-${readItem.id}`} wrapInBox={true} showCloseButton={true}>
								<AddText
									modalID={`edit-text-${readItem.id}`}
									editText={readItem}
									{readCategories}
									bind:readDocument />
							</Modal>
						</div>
					</tr>
				{/each}
			</Table>
		{:else}
			<p class="prose">{noTexts}</p>
		{/if}
	</Card>
</article>
