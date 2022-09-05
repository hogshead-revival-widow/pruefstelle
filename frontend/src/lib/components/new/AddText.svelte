<script lang="ts">
	/*
		Add new text
	*/
	import { fade } from 'svelte/transition';
	import * as yup from 'yup';
	import { createForm, Form, Field, ErrorMessage, Select, Textarea } from 'svelte-forms-lib';

	import { type ps, TextWorkflow, Pruefstelle } from '$lib/api';
	import { WORKFLOW_TO_WORD } from '$lib/data/services';
	import { FAQ } from '../faq';
	import { watchSelected } from '$lib/scripts/selectAll';
	import { getShortIfNeeded } from '$lib/utils';
	import { closeModal } from '$lib/scripts/modal';
	import { CategoryType } from '$lib/api';
	import type { CategoriesByType } from '$lib/scripts/new';
	import { Title, Category, Table } from '../basic';

	export let modalID;
	export let readDocument: ps.DocumentRead;
	export let readCategories: CategoriesByType;
	export let offerGeneration = false;
	export let editText: ps.TextRead = undefined; // if a value is given, edit mode is assumed

	let closeAfterSubmit = true;

	const handleAddText = async (values, y) => {
		const text: ps.TextCreate = {
			content: values.content,
			category_id: values.category_id,
			source_category_id: values.source_category_id,
			document_id: readDocument.id,
			parents: []
		};
		const services: ps.TextWorkflow[] = Object.entries(values.services)
			.filter(([_, use]) => use)
			.map(([service, _]) => <ps.TextWorkflow>service);

		const newText = await Pruefstelle.createText({ text, services });

		readDocument.items = [newText, ...readDocument.items];
	};

	const handleUpdateText = async (values, y) => {
		const text: ps.TextUpdate = {
			source_category_id: values.source_category_id,
			category_id: values.category_id
		};

		const newText = await Pruefstelle.updateText(editText.id, text);
		readDocument.items = [newText, ...readDocument.items.filter((text) => text.id !== newText.id)];
	};

	const handleDeleteText = async () => {
		const deletedText = await Pruefstelle.deleteText(editText.id);
		readDocument.items = readDocument.items.filter((text) => text.id !== deletedText.id);
	};

	let selector, selected;
	$: ({ selected, ...selector } = watchSelected({
		idAll: 'all',
		selectionItems: readDocument.items.map((text) => text),
		prefix: 'select-generate-text'
	}));

	const source_category_id = yup
		.string()
		.required('Bitte Quelle auswählen')
		.uuid('Bitte Quelle auswählen');

	const category_id = yup
		.string()
		.required('Bitte Kategorie auswählen')
		.uuid('Bitte Kategorie auswählen');

	const schemaNew = yup.object({
		content: yup
			.string()
			.required(offerGeneration ? 'Bitte mindestens zwei Texte auswählen' : 'Bitte Inhalt angeben'),
		category_id,
		source_category_id,
		services: yup
			.object({
				[TextWorkflow.KeywordExtraction]: yup.boolean(),
				[TextWorkflow.NamedEntityRecognition]: yup.boolean()
			})
			.test({
				message: 'Bitte mindestens einen Dienst wählen.',
				test: (workflow) => {
					const isValid = Object.values(workflow).some((value) => value);
					if (isValid) return true;
					return false;
				}
			})
	});

	const schemaEdit = yup.object({
		category_id,
		source_category_id
	});

	const handleSubmit = (values) => {
		selector.reset();

		if (closeAfterSubmit) {
			closeModal({ id: modalID });
		}

		if (editText === undefined) {
			handleAddText(values, { onSuccessDo: handleReset });
		} else {
			handleUpdateText(values, { onSuccessDo: handleReset });
		}
	};

	const formProps = {
		initialValues: {
			category_id: editText === undefined ? undefined : editText.category.id,
			source_category_id: editText === undefined ? undefined : editText.source_category.id,
			content: '',
			services: {
				[TextWorkflow.KeywordExtraction]: true,
				[TextWorkflow.NamedEntityRecognition]: true
			}
		},
		validationSchema: editText === undefined ? schemaNew : schemaEdit,
		onSubmit: (values) => handleSubmit(values)
	};

	const formContext = createForm(formProps);
	const { errors, handleReset, form } = formContext;

	let somethingSelected = false;
	$: somethingSelected = $selected.size > 0;

	$: if (offerGeneration && $selected.size > 1) {
		$form.content = readDocument.items
			.filter((text) => $selected.has(text.id))
			.map((text) => text.content)
			.join(' ');
	} else if (offerGeneration) {
		$form.content = '';
	}
</script>

<Form context={formContext} class="form-control" novalidate>
	<label class="label" for="category_id">
		<span class="label-text">Kategorie?</span>
		<ErrorMessage class="label-text text-error contrast-200" name="category_id" />
	</label>
	<Select
		name="category_id"
		class="select select-bordered {$errors.category_id ? 'select-error' : ''} ">
		<option value={undefined}>Auswählen...</option>
		{#each readCategories[CategoryType.TextCategory] as category}
			<option value={category.id}>{category.name}</option>
		{/each}
	</Select>

	<label class="label" for="source_category_id">
		<span class="label-text">Wo kommt der Text her?</span>
		<ErrorMessage class="label-text text-error contrast-200" name="source_category_id" />
	</label>
	<Select
		name="source_category_id"
		class="select select-bordered  {$errors.source_category_id ? 'select-error' : ''}">
		<option value={undefined}>Auswählen...</option>
		{#each readCategories[CategoryType.SourceCategory] as source}
			<option value={source.id}>{source.name}</option>
		{/each}
	</Select>

	{#if editText === undefined}
		{#each Object.values(TextWorkflow) as workflow}
			<div class="form-control">
				<label class="label cursor-pointer" for="services[{workflow}]">
					<span class="label-text"
						>{WORKFLOW_TO_WORD[workflow]} aktivieren? <FAQ forTerm={'services'} /></span>
					{#if typeof $errors.services === 'string'}
						<ErrorMessage class="label-text text-error contrast-200" name="services" />
					{/if}
					<Field
						type="checkbox"
						class="toggle"
						name="services[{workflow}]"
						checked={$form.services[workflow]} />
				</label>
			</div>
		{/each}

		<label class="label mt-2 max-w-sm" for="content">
			<span class="label-text"
				>{#if offerGeneration}Aus welchen Texten willst Du einen neuen Text generieren lassen?{:else}Inhalt?{/if}</span>
			<ErrorMessage class="label-text text-error contrast-200 ml-1" name="content" />
		</label>

		{#if offerGeneration}
			<Table classes={['mb-2']}>
				<svelte:fragment slot="header">
					<th>
						<input
							type="checkbox"
							class="checkbox checkbox-sm"
							id="select-generate-text-all"
							on:change={selector.toggleSelectAll} />
					</th>
					<th>Textanfang</th>
					<th>Kategorie</th>
					<th>Quelle</th>
				</svelte:fragment>
				{#each readDocument.items as text (text.id)}
					<tr>
						<td
							><input
								type="checkbox"
								class="checkbox checkbox-sm {$errors.content ? 'input-error' : ''}"
								value={text.id}
								id="select-generate-text-{text.id}"
								on:change={selector.toggleSelect} /></td>
						<td>
							<Title id={text.id} title={text.content} shortenToMaxLength={10} path={''} />
						</td>
						<td>
							<Category category={text.category} isSecondary={true} />
						</td>
						<td>
							<Category category={text.source_category} isSecondary={true} />
						</td>
					</tr>
				{/each}
			</Table>

			{#if $form.content !== ''}
				<h3 class="mt-2 mb-1">Vorschau generierter Text</h3>

				<div
					transition:fade
					class="textarea prose text-sm bordered  mb-2 max-w-md "
					readonly
					title={$form.content}>
					{getShortIfNeeded($form.content, 300)}
				</div>
			{/if}
		{:else}
			<Textarea
				name="content"
				class="textarea textarea-bordered {$errors.content ? 'textarea-error' : ''} mb-2" />
		{/if}
	{/if}
	{#if editText === undefined}
		<button type="submit" class="mt-4 btn btn-primary" on:click={() => (closeAfterSubmit = true)}>
			Hinzufügen & schließen
		</button>
		<button type="submit" class="mt-4 btn btn-primary" on:click={() => (closeAfterSubmit = false)}>
			Hinzufügen & offen halten
		</button>
	{:else}
		<button type="submit" class="mt-4 btn btn-primary" on:click={() => (closeAfterSubmit = true)}>
			Änderungen übernehmen
		</button>
		<button
			type="submit"
			class="mt-4 btn btn-error"
			on:click|preventDefault={() => {
				closeAfterSubmit = true;
				handleDeleteText();
			}}>
			Text löschen
		</button>
	{/if}
</Form>
