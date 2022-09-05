<script lang="ts">
	import { fade } from 'svelte/transition';
	import { TextWorkflow } from '$lib/api';
	import FAQ from '../faq/FAQ.svelte';

	import { WORKFLOW_TO_WORD, DEFAULT_WORKFLOWS } from '$lib/data/services';

	export let selectedWorkflows = Object.assign({}, DEFAULT_WORKFLOWS);
	export let atLeastOneWorkflowSelected: boolean;

	$: atLeastOneWorkflowSelected = Object.values(selectedWorkflows).some((value) => value);
</script>

{#if !atLeastOneWorkflowSelected}
	<div class="max-w-sm text-error" transition:fade>
		<p>Bitte wähle mindestens einen Service aus.</p>
	</div>
{/if}

{#each Object.values(TextWorkflow) as workflow}
	<div class="form-control">
		<label class="label cursor-pointer" for="selectedWorkflows[{workflow}]">
			<span class="label-text">
				{WORKFLOW_TO_WORD[workflow]}
				aktivieren?
				<FAQ forTerm={workflow} />
			</span>
			<input
				type="checkbox"
				class="toggle"
				class:input-error={!atLeastOneWorkflowSelected}
				name="selectedWorkflows[{workflow}]"
				bind:checked={selectedWorkflows[workflow]} />
		</label>
	</div>
{/each}
