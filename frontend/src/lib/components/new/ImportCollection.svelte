<script lang="ts">
	import { fade } from 'svelte/transition';
	import Dropzone from 'svelte-file-dropzone';

	import { getShortIfNeeded } from '$lib/utils';
	import { Pruefstelle, type ps } from '$lib/api';
	import { Card, Table } from '$lib/components/basic';
	import ChooseWorkflow from '$lib/components/new/ChooseWorkflow.svelte';
	import { closeModal } from '$lib/scripts/modal';
	import { addAlert } from '$lib/scripts/alerts';
	import type { Drafts } from '$lib/scripts/new';

	export let modalID;
	export let drafts: Drafts;

	let selectedWorkflows: Record<ps.TextWorkflow, boolean>;
	let atLeastOneWorkflowSelected: boolean;

	let files = {
		accepted: [],
		rejected: []
	};
	const handleFilesSelect = (e) => {
		const { acceptedFiles, fileRejections } = e.detail;
		files.accepted = [...files.accepted, ...acceptedFiles];
		files.rejected = [...files.rejected, ...fileRejections];
	};
	const handleRemoveFile = (e, index) => {
		files.accepted.splice(index, 1);
		files.accepted = [...files.accepted];
	};
	const handleRemoveAll = () => (files.accepted = []);

	const sleep = (milliseconds) => new Promise((resolve) => setTimeout(resolve, milliseconds));

	let uploadStarted = false;

	const handleUploadFiles = async () => {
		uploadStarted = true;
		let importError = false;
		files.accepted.forEach(async (file) => {
			const name = getShortIfNeeded(file.name);
			try {
				const textMiningWorkflows = Object.entries(selectedWorkflows)
					.filter(([_, selected]) => selected)
					.map(([workflow, _]) => workflow as ps.TextWorkflow);

				const services = textMiningWorkflows;
				const excel_collection = file;
				const responseDocuments =
					await Pruefstelle.importDocumentsWithTextsFromFesadExcelCollection(
						{ excel_collection },
						{ services }
					);

				drafts = [...responseDocuments, ...drafts];
			} catch (error) {
				console.error(error);
				const message = `Konnte ${name} nicht importieren`;
				const type = 'error';
				importError = true;
				addAlert({ message, type });
			}
		});
		if (modalID !== undefined) {
			closeModal({ id: modalID });
		}
	};
</script>

<Card classes={['overflow-auto', 'max-h-screen']}>
	<svelte:fragment slot="title">
		<label for="add-from-collection" class="btn btn-sm btn-circle absolute right-2 top-2">✕</label>

		<h2>
			{#if uploadStarted}
				Importiere...
			{:else}
				Importieren
			{/if}
		</h2>
	</svelte:fragment>

	{#if uploadStarted}
		<p>Bitte warte einen kurzen Moment.</p>
		<p>Deine Dokumente werden importiert.</p>

		<progress class="progress w-2/3 mx-auto mt-2 mb-2" />
	{:else}
		{#if files.accepted.length === 0}
			<p>Du kannst hier deine aus FESAD exportieren Excel-Sammelmappe hochladen.</p>

			<Dropzone
				on:drop={handleFilesSelect}
				accept={['application/vnd.ms-excel']}
				containerClasses="custom-dropzone"
				multiple={false}>
				<button>Klicke hier und wähle eine Datei aus</button>
				<p>oder</p>
				<p>ziehe sie hier hin.</p>
			</Dropzone>
		{:else}
			<h3 class="subtitle">Ausgewählte Sammelmappe{files.accepted.length > 1 ? 'n' : ''}</h3>
			<Table classes={['mb-2']}>
				{#each files.accepted as item, index}
					<tr in:fade>
						<td title={item.name}>
							{getShortIfNeeded(item.name, 50)}
						</td>
					</tr>
				{/each}
			</Table>
			<h3 class="subtitle">Import-Einstellungen</h3>
			<ChooseWorkflow bind:selectedWorkflows bind:atLeastOneWorkflowSelected />
		{/if}
		{#if files.accepted.length > 0 && atLeastOneWorkflowSelected}
			<button class="btn btn-primary" in:fade on:click={handleUploadFiles}>So importieren!</button>
			<button
				in:fade
				on:click={handleRemoveAll}
				class="btn btn-outline  btn-sm btn-error text-error-content">Zurücksetzen</button>
		{/if}
	{/if}
</Card>
