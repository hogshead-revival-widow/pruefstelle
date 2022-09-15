<script lang="ts">
	import { createForm, Form, Field, ErrorMessage, Select } from 'svelte-forms-lib';

	import type { CategoriesByType, Drafts } from '$lib/scripts/new';
	import { closeModal } from '$lib/scripts/modal';
	import { Pruefstelle, type ps } from '$lib/api';
	import { addAlert } from '$lib/scripts/alerts';
	import { addDocumentSchema } from '$lib/data/schemas';

	export let drafts: Drafts;
	export let readCategories: CategoriesByType;
	export let modalID = undefined;
	export let editDocument: ps.DocumentRead = undefined;
	export let reloadDocument = 0;

	let closeAfterSubmit = true;
	const handleSubmit = async ({ title, external_id, external_id_category_id, category_id }) => {
		if (closeAfterSubmit && modalID !== undefined) {
			closeModal({ id: modalID });
		}

		if (editDocument !== undefined) {
			await handleUpdate({ title, external_id, external_id_category_id, category_id });
			return undefined;
		}
		const errorMsg = `Konnte Dokument "${title}" nicht speichern`;
		const data: ps.DocumentCreate = {
			title,
			external_id,
			external_id_category_id,
			category_id,
			cases: []
		};
		try {
			const readDocument = await Pruefstelle.createDocument(data);
			drafts = [readDocument, ...drafts];
		} catch (error) {
			addAlert({ message: errorMsg, type: 'error' });
		}
	};

	const handleDelete = async () => {
		const deletedDocument = await Pruefstelle.deleteDocument(editDocument.id);
		drafts = drafts.filter((draftDocument) => draftDocument.id !== editDocument.id);
	};

	const handleUpdate = async ({ title, external_id, external_id_category_id, category_id }) => {
		const update: ps.DocumentUpdate = {
			title,
			external_id,
			external_id_category_id,
			category_id
		};

		editDocument = await Pruefstelle.updateDocument(editDocument.id, update);
		drafts = [
			editDocument,
			...drafts.filter((draftDocument) => draftDocument.id !== editDocument.id)
		];

		reloadDocument += 1;
	};

	const formProps = {
		initialValues: {
			title: editDocument !== undefined ? editDocument.title : '',
			external_id: editDocument !== undefined ? editDocument.external_id : '',
			category_id: editDocument !== undefined ? editDocument.category.id : '',
			external_id_category_id:
				editDocument !== undefined ? editDocument.external_id_category.id : ''
		},
		validationSchema: addDocumentSchema,
		onSubmit: async (values) => {
			await handleSubmit(values);
		}
	};

	const formContext = createForm(formProps);
	const { errors } = formContext;
</script>

<Form id="addDocument" context={formContext} class="form-control" novalidate>
	<label class="label " for="title">
		<span class="label-text">Kurze Titelnotiz?</span>
		<ErrorMessage class="label-text text-error contrast-200" name="title" />
	</label>
	<Field
		type="text"
		name="title"
		placeholder="z.B. RHTI"
		class="input input-bordered {$errors.title ? 'input-error' : ''}" />

	<label class="label " for="external_id">
		<span class="label-text">Eindeutige externe Referenz?</span>
		<ErrorMessage class="label-text text-error contrast-200" name="external_id" />
	</label>
	<Field
		type="text"
		name="external_id"
		placeholder="z.B. Produktions-ID"
		class="input input-bordered {$errors.external_id ? 'input-error' : ''}" />

	<label class="label " for="external_id_category_id">
		<span class="label-text">Typ der externen Referenz?</span>
		<ErrorMessage class="label-text text-error contrast-200" name="external_id_category_id" />
	</label>
	<Select
		name="external_id_category_id"
		class="select select-bordered {$errors.external_id_category_id ? 'select-error' : ''}">
		<option disabled selected>Auswählen...</option>
		{#each readCategories.external_id_category as external_id_category}
			<option value={external_id_category.id}>{external_id_category.name}</option>
		{/each}
	</Select>

	<label class="label" for="category_id">
		<span class="label-text">Kategorie?</span>
		<ErrorMessage class="label-text text-error contrast-200" name="category_id" />
	</label>
	<Select
		name="category_id"
		class="select select-bordered {$errors.category_id ? 'select-error' : ''}">
		<option disabled selected>Auswählen...</option>
		{#each readCategories.document_category as category}
			<option value={category.id}>{category.name}</option>
		{/each}
	</Select>

	{#if editDocument === undefined}
		{#if modalID === undefined}
			<button type="submit" class="mt-4 btn btn-primary"> Hinzufügen </button>
		{:else}
			<button type="submit" class="mt-4 btn btn-primary" on:click={() => (closeAfterSubmit = true)}>
				Hinzufügen & schließen
			</button>
			<button
				type="submit"
				class="mt-4 btn btn-primary"
				on:click={() => (closeAfterSubmit = false)}>
				Hinzufügen & offen halten
			</button>
		{/if}
	{:else}
		<button type="submit" class="mt-4 btn btn-primary" on:click={() => (closeAfterSubmit = true)}>
			Änderungen übernehmen
		</button>
		<button
			type="submit"
			class="mt-4 btn btn-error"
			on:click|preventDefault={() => {
				closeAfterSubmit = true;
				handleDelete();
			}}>
			Dokument löschen
		</button>
	{/if}
</Form>
