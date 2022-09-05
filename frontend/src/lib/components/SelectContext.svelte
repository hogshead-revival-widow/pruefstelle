<script lang="ts">
	import { goto } from '$app/navigation';

	import { FAQ } from '$lib/components/faq';
	import Card from '$lib/components/basic/Card.svelte';
	import { page } from '$app/stores';
	import { getShortIfNeeded } from '$lib/utils';
	import { type ps, isText, Pruefstelle } from '$lib/api';
	import { onMount } from 'svelte';

	export let selectFor: ps.DocumentRead | ps.TextRead;
	export let classes = [];
	classes = ['sidebar', ...classes];

	let readDocument: ps.DocumentRead = !isText(selectFor) ? selectFor : undefined;
	let stem = 'document';
	onMount(async () => {
		if (isText(selectFor)) {
			stem = 'text';
			readDocument = await Pruefstelle.readDocument(selectFor.document_id);
		}
	});

	let currentContext = $page.url.pathname;
	let caseID = $page.url.pathname.includes('context')
		? $page.url.pathname.split('/')[$page.url.pathname.split('/').length - 1]
		: undefined;

	let path: string;
	const changeContext = (path) => {
		goto(path);
	};

	let currentCaseIDTitle = undefined;
	if (caseID !== undefined && readDocument !== undefined) {
		currentCaseIDTitle = readDocument.cases.find((caseIDTitle) => caseIDTitle.id === caseID);
	}
</script>

{#if readDocument !== undefined}
	<Card isHideable={false} {classes}>
		<svelte:fragment slot="title"><FAQ forTerm="context">Bezugsfall</FAQ></svelte:fragment>
		<article class="form-control">
			<div class="input-group">
				<select id="select-context" class="select select-bordered" bind:value={path}>
					{#if currentCaseIDTitle != undefined}
						<option value={$page.url.pathname} title={currentCaseIDTitle.title}>
							{getShortIfNeeded(currentCaseIDTitle.title, 20)}</option>
						<option value="/dashboard/{stem}/{selectFor.id}">ohne Bezugsfall</option>
					{:else}
						<option value={$page.url.pathname}>ohne Bezugsfall</option>
					{/if}
					{#each readDocument.cases as caseIDTitle}
						{#if `/dashboard/${stem}/${selectFor.id}/context/${caseIDTitle.id}` !== $page.url.pathname}
							<option
								value="/dashboard/{stem}/{selectFor.id}/context/{caseIDTitle.id}"
								title={caseIDTitle.title}>
								{getShortIfNeeded(caseIDTitle.title, 20)}
							</option>
						{/if}
					{/each}
				</select>
				<button
					class="btn btn-primary"
					disabled={path === $page.url.pathname}
					on:click={() => changeContext(path)}>Wechseln</button>
			</div>
		</article>
	</Card>
{/if}
