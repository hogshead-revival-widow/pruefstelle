<script lang="ts">
	import { createForm, Form, Field, ErrorMessage, Select } from 'svelte-forms-lib';
	import { goto } from '$app/navigation';

	import { Table, Title, Category, Card } from '$lib/components/basic';
	import type { CategoriesByType, Drafts } from '$lib/scripts/new';
	import { Pruefstelle, ps } from '$lib/api';
	import { addCaseSchema } from '$lib/data/schemas';

	export let readCategories: CategoriesByType;
	export let drafts: Drafts;

	const startJobs = (drafts: Drafts) => {
		const jobIDs = drafts.flatMap((draft) =>
			draft.items.flatMap((item) => item.mining_jobs.flatMap((job) => job.id))
		);
		const promisedJobs = jobIDs.map((jobID) => Pruefstelle.startJob(jobID));
		return promisedJobs;
	};
	let successfullySubmitted = false;
	const handleSubmit = async ({ title, category_id }) => {
		const profile: ps.ProfileCreate = {
			keyword_relevance_threshold: 0,
			keyword_confidence_threshold: 0,
			keyword_frequency_threshold: 0,
			keyword_only_top_n_relevance: 0,
			research_quality_constraint_needed_users: 1,
			research_quality_good_threshold: 50
		};
		const documents = drafts.map((document) => document.id);
		const data: ps.CaseCreate = { title, category_id, documents, profile };
		const newCase = await Pruefstelle.createCase(data);
		await Promise.all(startJobs(drafts));
		successfullySubmitted = true;
		goto(`/dashboard/case/${newCase.id}`);
	};

	const formProps = {
		initialValues: {
			title: '',
			category_id: undefined
		},
		validationSchema: addCaseSchema,
		onSubmit: (values) => {
			handleSubmit(values);
		}
	};

	const formContext = createForm(formProps);
	const { errors } = formContext;
</script>

<Card hasBackground={true}>
	{#if successfullySubmitted}
		<span class="loading">Bitte warte einen kurzen Moment.</span>
		<span class="loading">In wenigen Sekunden wirst Du zu deinem neuen Fall weitergeleitet.</span>
	{:else}
		<Form id="addCase" context={formContext} class="form-control" novalidate>
			<label class="label " for="title">
				<span class="label-text">Wie willst Du nach deinem Fall suchen können?</span>
				<ErrorMessage class="label-text text-error contrast-200" name="title" />
			</label>
			<Field
				type="text"
				name="title"
				placeholder="z.B. 'Test: Transkript nicht nutzen?'"
				class="input input-bordered {$errors.title ? 'input-error' : ''}" />

			<label class="label" for="category_id">
				<span class="label-text">Kategorie?</span>
				<ErrorMessage class="label-text text-error contrast-200" name="category_id" />
			</label>
			<Select
				name="category_id"
				class="select select-bordered {$errors.category_id ? 'select-error' : ''}">
				<option value={undefined}>Auswählen...</option>
				{#each readCategories.case_category as category}
					<option value={category.id}>{category.name}</option>
				{/each}
			</Select>

			<Table classes={['mt-6']}>
				<svelte:fragment slot="header">
					<th>Dokument</th>
					<th>Kategorie</th>
					<th>Texte</th>
				</svelte:fragment>

				{#each drafts as readDocument}
					<tr>
						<td>
							<Title id="" path="" title={readDocument.title} />
						</td>
						<td>
							<Category category={readDocument.category} isSecondary={true} />
						</td>
						<td>{readDocument.items.length}</td>
					</tr>
				{/each}
			</Table>
			<button type="submit" class="mt-4 btn btn-primary"> Hinzufügen </button>
		</Form>
	{/if}
</Card>
