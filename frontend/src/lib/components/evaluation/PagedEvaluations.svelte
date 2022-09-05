<script lang="ts">
	import { fly } from 'svelte/transition';

	import { Card, Table, Pagination, Title } from '$lib/components/basic';
	import Evaluation from '$lib/components/evaluation/Evaluation.svelte';
	import { Pruefstelle } from '$lib/api';
	import type { ps } from '$lib/api';
	import { watchSelected } from '$lib/scripts/selectAll';
	import { addAlert } from '$lib/scripts/alerts';
	import { EvaluationType } from '$lib/api';

	export let readPagedEvaluations: ps.PageEvaluationRead;
	export let title: { title: string; id: string; path: string } = undefined;
	export let id: string | undefined = undefined;
	export let toPageEvaluation;
	export let fetchDocument = false;

	const promisedDocumentsByMiningResultId: { [key: string]: Promise<ps.DocumentRead> } = {};

	if (fetchDocument === true) {
		const uniqueMiningResultIds = new Set(
			readPagedEvaluations.items.map((evaluation) => evaluation.mining_result_id)
		);
		uniqueMiningResultIds.forEach((miningResultId) => {
			promisedDocumentsByMiningResultId[miningResultId] =
				Pruefstelle.readDocumentFromMiningResult(miningResultId);
		});
	}

	let selector;
	let selected;

	selector = watchSelected({
		idAll: 'all',
		selectionItems: readPagedEvaluations.items,
		prefix: 'my-evaluation'
	});
	selected = selector.selected; // returns store

	let somethingSelected = false;
	let selection;
	$: {
		selection = readPagedEvaluations.items.filter((evaluation) => $selected.has(evaluation.id));
		somethingSelected = selection.length > 0 ? true : false;
	}

	const triggerEditEvaluation = async (value: number) => {
		try {
			const promisedUpdates: Promise<ps.EvaluationRead>[] = selection
				.filter((evaluation) => evaluation.value !== value)
				.map((evaluation: ps.EvaluationRead) => {
					let data = { discriminator: evaluation.discriminator, value: value };

					if (data.discriminator === EvaluationType.CorrectnessEvaluation) {
						//@ts-ignore
						data.value = value > 0 ? true : false;
					}

					//@ts-ignore
					return Pruefstelle.updateEvaluation(evaluation.id, data);
				});
			const readEvaluations = await Promise.all(promisedUpdates);
			const updatedEvaluationsById = readEvaluations.map((evaluation) => evaluation.id);
			const filteredExistingEvaluations = readPagedEvaluations.items.filter(
				(evaluation) => !updatedEvaluationsById.includes(evaluation.id)
			);
			addAlert({
				message: `Bewertung${promisedUpdates.length > 1 ? 'en' : ''} aktualisiert`,
				type: 'success'
			});
			readPagedEvaluations.items = [...readEvaluations, ...filteredExistingEvaluations];
			selector.reset();
		} catch (error) {
			addAlert({ message: 'Aktualisierung fehlgeschlagen', type: 'error' });
		}
	};

	const triggerDeleteEvaluation = async () => {
		try {
			const promisedDeletes: Promise<ps.EvaluationRead>[] = selection.map((evaluation) =>
				Pruefstelle.deleteEvaluation(evaluation.id)
			);
			const readEvaluations = await Promise.all(promisedDeletes);
			const deletedEvaluationsById = readEvaluations.map((evaluation) => evaluation.id);
			const keepEvaluations = readPagedEvaluations.items.filter(
				(evaluation) => !deletedEvaluationsById.includes(evaluation.id)
			);
			addAlert({
				message: `Bewertung${promisedDeletes.length > 1 ? 'en' : ''} gelöscht`,
				type: 'success'
			});
			readPagedEvaluations.items = [...keepEvaluations];
			if (readPagedEvaluations.items.length === 0) {
				window.location.reload();
			}
			selector.reset();
		} catch (error) {
			addAlert({ message: 'Löschen fehlgeschlagen', type: 'error' });
		}
	};

	$: noEvaluations =
		readPagedEvaluations.total === 0 ||
		(readPagedEvaluations.items.length === 0 &&
			readPagedEvaluations.total < readPagedEvaluations.size);
</script>

{#if noEvaluations}
	<Card isHideable={false} classes={['w-96']}>
		<svelte:fragment slot="title"
			>Hier gibt es keine Bewertungen, die angezeigt werden können.
		</svelte:fragment>
	</Card>
{:else}
	<Card isHideable={false} classes={['pb-12', 'w-98']}>
		<Pagination
			{id}
			page={readPagedEvaluations.page}
			size={readPagedEvaluations.size}
			total={readPagedEvaluations.total}
			callback={toPageEvaluation} />
		<h1 slot="title"><Title {...title} /></h1>

		<div class="mb-2" class:mt-8={!somethingSelected}>
			{#if somethingSelected}
				<button
					class="btn btn-error btn-sm text-white gap-2"
					on:click={() => triggerDeleteEvaluation()}
					><i class="fas fa-trash ml-2" />Lösche Auswahl</button>

				<div class="dropdown dropdown-end ">
					<button tabindex="0" class="btn btn-primary gap-2 btn-sm text-white">
						<i class="fas fa-edit ml-2" />Ändere Auswahl
					</button>
					<ul tabindex="0" class=" menu dropdown-content p-2 shadow bg-base-100 rounded-box">
						<li>
							<button class="btn evaluation-good  mb-2" on:click={() => triggerEditEvaluation(2)}>
								auf passend / korrekt
							</button>
						</li>
						<li>
							<button class="btn evaluation-mixed mb-2" on:click={() => triggerEditEvaluation(1)}>
								auf hilfreich / korrekt
							</button>
						</li>
						<li>
							<button class="btn evaluation-bad  mb-2" on:click={() => triggerEditEvaluation(0)}>
								auf unpassend / falsch
							</button>
						</li>
					</ul>
				</div>
			{/if}
		</div>

		<div class="form-control">
			<label class="label cursor-pointer">
				<span class="label-text">Alle angezeigten auswählen</span>

				<input
					type="checkbox"
					on:change={selector.toggleSelectAll}
					class="checkbox checkbox-sm"
					id="my-evaluation-all" />
			</label>
		</div>

		<Table isCompact={true}>
			{#each readPagedEvaluations.items as readEvaluation (readEvaluation.id)}
				<tr out:fly|local>
					<td>
						<input
							type="checkbox"
							on:change={selector.toggleSelect}
							class="checkbox checkbox-sm"
							value={readEvaluation.id}
							id="my-evaluation-{readEvaluation.id}" />
					</td>
					<Evaluation
						{readEvaluation}
						inTableRow={true}
						promisedDocument={promisedDocumentsByMiningResultId[readEvaluation.mining_result_id]} />
				</tr>
			{/each}
		</Table>
		<Pagination
			{id}
			page={readPagedEvaluations.page}
			size={readPagedEvaluations.size}
			total={readPagedEvaluations.total}
			callback={toPageEvaluation} />
	</Card>
{/if}
