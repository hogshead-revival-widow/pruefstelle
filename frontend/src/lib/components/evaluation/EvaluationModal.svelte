<script lang="ts">
	import { fly } from 'svelte/transition';

	import { Pruefstelle, type ps } from '$lib/api';
	import { Card, Table, Category, Title } from '$lib/components/basic';
	import Modal from '$lib/components/Modal.svelte';
	import { EvaluationItem, type TitleData } from '$lib/scripts/evaluation';
	import { addAlert } from '$lib/scripts/alerts';
	import { closeModal } from '$lib/scripts/modal';
	import { watchSelected } from '$lib/scripts/selectAll';
	import { user } from '$lib/stores';
	import { EvaluationType, NamedEntityType } from '$lib/api';
	import type { RefreshState } from '$lib/scripts/reloader';
	import { object_without_properties } from 'svelte/internal';

	export let readReports: ps.ReportWithPoints[];
	export let batchMode = undefined;
	export let readDocuments: ps.DocumentRead[] | ps.DocumentReadWithoutCases[];
	export let case_id = '';
	export let refreshState: RefreshState;

	let batchGivenScore: 0 | 1 | 2 | undefined = undefined;
	let selector;
	let selected;

	const titles: TitleData[] = readDocuments.flatMap((readDocument) =>
		readDocument.items.map((item) => ({
			item_id: item.id,
			title: readDocument.title,
			document_id: readDocument.id
		}))
	);

	let evaluationQueue = readReports
		.flatMap((report) => report.item_results)
		.filter(
			(item) => !item.evaluations.map((evaluation) => evaluation.creator_id).includes($user.id)
		)
		.map((item) => new EvaluationItem(item, titles, case_id));

	selector = watchSelected({
		idAll: 'all',
		selectionItems: evaluationQueue,
		prefix: 'my-batch-evaluation'
	});
	selected = selector.selected; // returns store

	const hasFilteredBefore = {
		[NamedEntityType.PERSON]: { selected: [], lengthBefore: 0 },
		[NamedEntityType.LOCATION]: { selected: [], lengthBefore: 0 },
		[NamedEntityType.ORGANIZATION]: { selected: [], lengthBefore: 0 },
		keyword: { selected: [], lengthBefore: undefined },
		topic: { selected: [], lengthBefore: undefined }
	};

	const skip = (toSkip: EvaluationItem) => {
		toSkip.showMore = false;
		evaluationQueue = [...evaluationQueue.filter((item) => item.id !== toSkip.id), toSkip];
	};

	const selectItems = (key: ps.NamedEntityType | 'keyword' | 'topic') => {
		const currentSelection = Array.from(selector.getSelection());
		if (
			hasFilteredBefore[key].selected.length > 0 &&
			hasFilteredBefore[key].lengthBefore === currentSelection.length
		) {
			selector.setSelection(
				new Set(currentSelection.filter((item) => !hasFilteredBefore[key].selected.includes(item)))
			);
			hasFilteredBefore[key].selected = [];
			hasFilteredBefore[key].lengthBefore = currentSelection.length;
			return undefined;
		}

		let selected = [];
		if (key === 'keyword') {
			selected = evaluationQueue.filter((item) => item.isKeyword()).map((item) => item.id);
		} else if (key === 'topic') {
			selected = evaluationQueue.filter((item) => item.isTopic()).map((item) => item.id);
		} else {
			selected = evaluationQueue
				.filter((item) => !item.isKeyword() && item.type === key)
				.map((item) => item.id);
		}

		hasFilteredBefore[key].selected = selected;
		selector.setSelection(selected);
	};

	const handleSubmit = async (toEvaluate: EvaluationItem) => {
		const data = toEvaluate.getEvaluationData();
		try {
			const newEvaluation = await Pruefstelle.createEvaluation(toEvaluate.id, data);
			let resultIdx = undefined;
			const reportIdx = readReports.findIndex((report) => {
				resultIdx = report.item_results.findIndex(
					(result) => result.id === newEvaluation.mining_result_id
				);
				return resultIdx !== -1;
			});
			readReports[reportIdx].item_results[resultIdx].evaluations = [
				newEvaluation,
				...readReports[reportIdx].item_results[resultIdx].evaluations
			];

			evaluationQueue = evaluationQueue.filter((evaluated) => evaluated.id !== toEvaluate.id);

			if (evaluationQueue.length === 0) {
				await refreshState();
				closeModal({ id: 'modal-evaluateCards' });
			}
		} catch (error) {
			addAlert({ message: 'Konnte Bewertung nicht speichern', type: 'error' });
		}
	};

	const handleSubmitSelection = async (value: ps.Score) => {
		[...$selected].forEach(async (evaluationItemID) => {
			const toEvaluate = evaluationQueue.find((evaluation) => evaluation.id === evaluationItemID);
			toEvaluate.setValueFromBatch(value);
			await handleSubmit(toEvaluate);
		});

		batchGivenScore = undefined;
	};
</script>

<section>
	<Modal id="modal-evaluateCards" classes={['max-h-full', 'overflow-auto', 'w-100']}>
		{#if batchMode === undefined}
			<Card isHideable={false} classes={['w-96']}>
				<button class="btn-primary btn" on:click|preventDefault={() => (batchMode = false)}>
					Einzeln bewerten
				</button>
				<button class="btn-primary btn" on:click|preventDefault={() => (batchMode = true)}>
					Im Stapel bewerten
				</button>
			</Card>
		{/if}
		{#if batchMode == true}
			<Card isHideable={false} classes={['w-100', 'mt-4', 'mb-4']}>
				<div class="btn-group  mb-2 place-content-end">
					{#if evaluationQueue.filter((item) => item.isTopic()).length > 0}
						<button class="btn-ghost btn btn-xs gap-2" on:click={() => selectItems('topic')}
							><span class="topic" /></button>
					{/if}

					{#if evaluationQueue.filter((item) => item.isKeyword()).length > 0}
						<button class="btn-ghost btn btn-xs gap-2" on:click={() => selectItems('keyword')}
							><span class="keyword" /></button>
					{/if}

					{#if evaluationQueue.filter((item) => !item.isKeyword() && item.type === NamedEntityType.PERSON).length > 0}
						<button
							class="btn-ghost btn btn-xs gap-2"
							on:click={() => selectItems(NamedEntityType.PERSON)}
							><span class="named-entity PERSON" /></button>
					{/if}

					{#if evaluationQueue.filter((item) => !item.isKeyword() && item.type === NamedEntityType.LOCATION).length > 0}
						<button
							class="btn-ghost btn btn-xs gap-2"
							on:click={() => selectItems(NamedEntityType.LOCATION)}
							><span class="named-entity LOCATION" /></button>
					{/if}

					{#if evaluationQueue.filter((item) => !item.isKeyword() && item.type === NamedEntityType.ORGANIZATION).length > 0}
						<button class="btn-ghost btn btn-xs"
							><span
								class="named-entity ORGANIZATION"
								on:click={() => selectItems(NamedEntityType.ORGANIZATION)} /></button>
					{/if}

					<div class="divider divider-horizontal" />

					<button class="btn-ghost btn btn-xs" on:click|preventDefault={() => (batchMode = false)}>
						Einzeln bewerten
					</button>
				</div>
				<div class:mt-8={selected !== undefined && $selected.size === 0} class="mx-auto">
					{#if selected !== undefined && $selected.size > 0}
						{#if evaluationQueue
							.filter((toEvaluate) => $selected.has(toEvaluate.id))
							.every((toEvaluate) => toEvaluate.isKeyword()) || evaluationQueue
								.filter((toEvaluate) => $selected.has(toEvaluate.id))
								.every((toEvaluate) => toEvaluate.isTopic())}
							<div class="btn-group">
								<button
									class="btn btn-sm evaluation-good"
									class:btn-chosen={batchGivenScore === 2}
									on:click|preventDefault={() => {
										handleSubmitSelection(2);
									}}>
									passend
								</button>
								<button
									class="btn btn-sm evaluation-ok"
									class:btn-chosen={batchGivenScore === 1}
									on:click|preventDefault={() => {
										handleSubmitSelection(1);
									}}>
									hilfreich
								</button>
								<button
									class="btn btn-sm evaluation-bad"
									class:btn-primary={batchGivenScore === 0}
									on:click|preventDefault={() => {
										handleSubmitSelection(0);
									}}>
									unpassend
								</button>
							</div>
						{:else if selected !== undefined && evaluationQueue
								.filter((toEvaluate) => $selected.has(toEvaluate.id))
								.every((toEvaluate) => !toEvaluate.isKeyword())}
							<div class="btn-group">
								<button
									class="btn btn-sm evaluation-good"
									class:btn-chosen={batchGivenScore === 2}
									on:click|preventDefault={() => {
										handleSubmitSelection(2);
									}}>
									korrekt
								</button>
								<button
									class="btn btn-sm evaluation-bad"
									class:btn-primary={batchGivenScore === 0}
									on:click|preventDefault={() => {
										handleSubmitSelection(0);
									}}>
									falsch
								</button>
							</div>
						{:else}
							<div class="btn-group">
								<button
									class="btn btn-sm evaluation-good"
									class:btn-chosen={batchGivenScore === 2}
									on:click|preventDefault={() => {
										handleSubmitSelection(2);
									}}>
									passend / korrekt
								</button>
								<button
									class="btn btn-sm evaluation-mixed "
									class:btn-chosen={batchGivenScore === 1}
									on:click|preventDefault={() => {
										handleSubmitSelection(1);
									}}>
									hilfreich / korrekt
								</button>
								<button
									class="btn btn-sm evaluation-bad"
									class:btn-primary={batchGivenScore === 0}
									on:click|preventDefault={() => {
										handleSubmitSelection(0);
									}}>
									unpassend / falsch
								</button>
							</div>
						{/if}
					{/if}
				</div>
				<Table>
					<svelte:fragment slot="header">
						<th>
							<input
								type="checkbox"
								on:change={selector.toggleSelectAll}
								class="checkbox checkbox-sm"
								id="my-batch-evaluation-all" />
						</th>
						<th>Einheit</th>
						<th>Dokument</th>
					</svelte:fragment>

					{#each evaluationQueue as item (item.id)}
						<tr transition:fly|local>
							<td>
								<input
									type="checkbox"
									on:change={selector.toggleSelect}
									class="checkbox checkbox-sm"
									value={item.id}
									id="my-batch-evaluation-{item.id}" />
							</td>
							<td>
								<mark class="{item.getClasses()}  badge-lg" title={item.name}>
									{item.name}
								</mark>
							</td>
							<td> {@html item.getDocumentLink(true)} </td>
						</tr>
					{/each}
				</Table>
			</Card>
		{:else if batchMode === false}
			<article class="stack">
				{#each evaluationQueue as toEvaluate, i (toEvaluate.id)}
					<div out:fly|local class="card mb-2 bg-base-100 {i == 0 ? 'shadow-lg' : 'shadow'} w-98">
						<div class="card-body">
							<div class="btn-group place-content-end mb-0">
								<button
									class="btn btn-ghost btn-xs"
									on:click={() => {
										toEvaluate.showMore = !toEvaluate.showMore;
									}}>
									Meta
								</button>
								{#if evaluationQueue.length > 1}
									<button class="btn btn-xs btn-ghost" on:click={() => skip(toEvaluate)}>
										Überspringen
									</button>
								{/if}
								<div class="divider divider-horizontal" />
								<button
									class="btn-ghost btn btn-xs"
									on:click|preventDefault={() => (batchMode = true)}>
									Im Stapel bewerten
								</button>
							</div>
							<h2 class="card-title mb-2 mt-2">
								Bewertung:
								{#if toEvaluate.isTopic()}Topic{:else}
									<span class={toEvaluate.getClasses()}> {toEvaluate.name}</span>
								{/if}
							</h2>

							<div class="evaluation">
								{#if toEvaluate.getEvaluationType() === EvaluationType.CorrectnessEvaluation}
									<p>Ist</p>
									<p class={toEvaluate.getClasses()}>
										{toEvaluate.name}
									</p>
									<p>{toEvaluate.getTypeName()} dieses Namens?</p>
								{:else}
									<p>
										Wie gut beschreibt {toEvaluate.isKeyword() ? 'das Schlüsselwort' : 'das Topic'}
									</p>

									<p class={toEvaluate.getClasses()}>
										{toEvaluate.name}
									</p>

									<p>das Dokument</p>
									<p><strong>{@html toEvaluate.getDocumentLink(false)}?</strong></p>
								{/if}
							</div>
							<form method="post" name={toEvaluate.id}>
								<div class="card-actions justify-end mt-2">
									<div class="btn-group">
										{#if toEvaluate.getEvaluationType() === EvaluationType.CorrectnessEvaluation}
											<button
												class="btn btn-sm evaluation-good"
												on:click|preventDefault={() => {
													toEvaluate.setValue(true);
													handleSubmit(toEvaluate);
												}}>ja, korrekt</button>
											<button
												class="btn btn-sm evaluation-bad"
												on:click|preventDefault={() => {
													toEvaluate.setValue(false);
													handleSubmit(toEvaluate);
												}}>nein, falsch</button>
										{:else}
											<button
												class="btn btn-sm evaluation-good"
												class:btn-chosen={toEvaluate.score === 2}
												on:click|preventDefault={() => {
													toEvaluate.setValue(2);
													handleSubmit(toEvaluate);
												}}>passend</button>
											<button
												class="btn btn-sm evaluation-ok"
												class:btn-chosen={toEvaluate.score === 1}
												on:click|preventDefault={() => {
													toEvaluate.setValue(1);
													handleSubmit(toEvaluate);
												}}>hilfreich</button>
											<button
												class="btn btn-sm evaluation-bad"
												class:btn-primary={toEvaluate.score === 0}
												on:click|preventDefault={() => {
													toEvaluate.setValue(0);
													handleSubmit(toEvaluate);
												}}>unpassend</button>
										{/if}
									</div>
								</div>
							</form>

							{#if toEvaluate.showMore}
								<div class="prose">
									<div class="divider" />
									{#if toEvaluate.isTopic()}
										<h3>Topic-Mappings</h3>
										<ul>
											{#each readReports
												.flatMap((report) => report.item_results)
												.find((topic) => topic.id === toEvaluate.id)
												.mappings.sort((that, other) => other.score - that.score) as mapping}
												<li>
													<a href={mapping.link} target="new">{mapping.terms} ({mapping.score})</a>
												</li>
											{/each}
										</ul>
									{/if}
									<h3>Bezugsdokument</h3>
									<Category
										compactView={true}
										isSecondary={true}
										category={toEvaluate.getDocument(readDocuments).category} />

									<Category
										compactView={true}
										isSecondary={true}
										category={toEvaluate.getText(readDocuments).source_category} />

									<p>Zum Dokument: {@html toEvaluate.getDocumentLink()}</p>
									<h3>Bezugstext</h3>
									<Category
										compactView={true}
										isSecondary={true}
										category={toEvaluate.getText(readDocuments).category} />
									{#each toEvaluate.getText(readDocuments).content.split('\n') as paragraph}
										<p>{paragraph}</p>
									{/each}
								</div>
							{/if}
						</div>
					</div>
				{/each}
			</article>
		{/if}
	</Modal>
</section>
