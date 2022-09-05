<script context="module" lang="ts">
	import { makePruefstelle, CategoryType, type ps } from '$lib/api';

	export const load = async ({ fetch }) => {
		const pruefstelle = makePruefstelle({ customFetch: fetch });
		const sorter = (that, other) => that.name.localeCompare(other.name);
		const sort = (item: ps.CategoryRead[]) => item.sort(sorter);

		const readCategories = {
			[CategoryType.CaseCategory]: sort(
				await pruefstelle.listCategories(CategoryType.CaseCategory)
			),
			[CategoryType.DocumentCategory]: sort(
				await pruefstelle.listCategories(CategoryType.DocumentCategory)
			),
			[CategoryType.TextCategory]: sort(
				await pruefstelle.listCategories(CategoryType.TextCategory)
			),
			[CategoryType.SourceCategory]: sort(
				await pruefstelle.listCategories(CategoryType.SourceCategory)
			),
			[CategoryType.ExternalIdCategory]: sort(
				await pruefstelle.listCategories(CategoryType.ExternalIdCategory)
			)
		};

		return { props: { readCategories } };
	};
</script>

<script lang="ts">
	import Card from '$lib/components/basic/Card.svelte';
	import Modal from '$lib/components/Modal.svelte';
	import { showModal } from '$lib/scripts/modal';
	import Welcome from '$lib/components/new/Welcome.svelte';
	import Add from '$lib/components/new/Add.svelte';
	import { Steps, canProceedFrom } from '$lib/scripts/new';
	import { fade } from 'svelte/transition';
	import type { CategoriesByType } from '$lib/api';
	import AddCase from '$lib/components/new/AddCase.svelte';

	export let readCategories: CategoriesByType;
	let drafts = [];
	let currentStep = Steps.START;
	let canProceed = false;
	$: canProceed = canProceedFrom[currentStep](drafts);

	let helpAction: undefined | 'createDocument' | 'importCollection' = undefined;
</script>

{#key currentStep}
	<main class="mt-2 w-100 h-12" in:fade>
		{#if currentStep === Steps.START}
			<Welcome />
		{/if}

		{#if currentStep === Steps.ADD}
			<Add bind:drafts {readCategories} />
		{/if}

		{#if currentStep === Steps.DONE}
			<AddCase {readCategories} bind:drafts />
		{/if}
	</main>
{/key}

<section class="ml-8 mt-2">
	<article>
		<Card>
			{#if currentStep != Steps.DONE && Object.keys(Steps).length >= currentStep + 1}
				<button
					class="btn-primary btn btn-lg gap-2"
					class:btn-disabled={!canProceed}
					on:click={() => (currentStep = currentStep + 1)}>
					<i class="fas fa-step-forward " />
					Weiter
				</button>
			{/if}
			{#if currentStep == Steps.DONE}
				<button class="btn-ghost btn btn-lg gap-2" on:click={() => (currentStep = currentStep - 1)}>
					<i class="fas fa-step-backward" />
					Zurück
				</button>
			{/if}

			{#if currentStep === Steps.ADD}
				<button
					class="btn-ghost btn btn-lg gap-2"
					on:click={() => showModal({ id: `new-help-${Steps.ADD}` })}>
					<i class="fas fa-question" />
					Hilfe
				</button>
			{/if}
		</Card>
	</article>
</section>

<!-- Help -->
<Modal id={`new-help-${Steps.ADD}`}>
	<Card classes={['w-96']} isHideable={false}>
		<svelte:fragment slot="title">Hilfe</svelte:fragment>

		{#if helpAction === undefined}
			<div in:fade|local>
				<p>Was willst Du tun?</p>

				<div class="mt-2 flex flex-col items-center gap-2">
					<button
						class="btn-primary btn btn-block"
						on:click|preventDefault={() => (helpAction = 'createDocument')}
						>Frei Dokumente anlegen</button>
					<button
						class="btn-primary btn btn-block"
						on:click|preventDefault={() => (helpAction = 'importCollection')}
						>Eine Sammelmappe aus FESAD importieren</button>
				</div>
			</div>
		{:else if helpAction === 'createDocument'}
			<div class="prose" in:fade|local>
				<ol>
					<li>
						Klicke auf <strong class="uppercase"><i class="fas fa-plus" /> Dokument</strong>, um ein
						<strong>Dokument hinzufügen.</strong>
					</li>
					<li>
						Wenn Du ein Dokument hinzugefügt hast, kannst Du dem jeweiligen Dokument einen Text
						hinzufügen. Klicke dazu auf den Knopf
						<strong class="uppercase"><i class="fas fa-plus" /> Text</strong>. Wähle den Knopf, der
						<strong>neben dem Dokument</strong> steht, <strong>zu dem dein Text gehört.</strong>
					</li>
					<li>
						Alle Dokumente und Texte angelegt? Dann klicke auf
						<strong class="uppercase">
							<i class="fas fa-forward" /> Weiter
						</strong>. Um fortzufahren, muss:
						<ul class="text-sm">
							<li>mindestens <strong>ein Dokument</strong> vorhanden sein,</li>
							<li>jedem Dokument mindestens <strong>ein Text</strong> hinzugefügt werden.</li>
						</ul>
					</li>
				</ol>

				<p class="text-sm">
					Optional: Wähle mindestens zwei Texte aus, um aus diesen einen Text mit dem kombinierten
					Inhalt der beiden Texte zu generieren.
				</p>
			</div>
		{:else if helpAction === 'importCollection'}
			<div class="prose">
				<ol>
					<li>
						Klicke auf <strong class="uppercase"
							><i class="fas fa-file-import" /> Sammelmappe</strong>
					</li>
					<li>Ziehe deine Sammelmappe in das große graue Feld oder klicke darauf.</li>
					<li>
						Stelle unter <strong>Import-Einstellungen</strong> ein, welche Dienste für alle importierbaren
						Texte aktiviert werden sollen.
					</li>
					<li>
						Klicke auf <strong class="uppercase"> so importieren</strong>
					</li>
					<li>
						Wenn Du einzelne Texte oder Dokumente löschen willst, klicke auf <strong
							><i class="fas fa-edit" /></strong>
					</li>
					<li>
						Wenn Du weitere Texte hinzufügen willst, klicke auf den Knopf
						<strong class="uppercase"><i class="fas fa-plus" /> Text</strong>. Wähle den Knopf, der
						<strong>neben dem Dokument</strong> steht, <strong>zu dem dein Text gehört.</strong>
					</li>
					<li>
						Fertig? Dann klicke auf
						<strong class="uppercase">
							<i class="fas fa-forward" /> Weiter
						</strong>. Um fortzufahren, muss:
						<ul class="text-sm">
							<li>mindestens <strong>ein Dokument</strong> vorhanden sein,</li>
							<li>jedes Dokument mindestens <strong>einen Text</strong> besitzen.</li>
						</ul>
					</li>
				</ol>
			</div>
		{/if}

		{#if helpAction !== undefined}
			<button
				in:fade|local
				class="btn-primary btn btn-block"
				on:click|preventDefault={() => (helpAction = undefined)}>Übersicht</button>
		{/if}
	</Card>
</Modal>
