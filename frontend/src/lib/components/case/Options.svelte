<script lang="ts">
	import type { RefreshState } from '$lib/scripts/reloader';

	import { fade } from 'svelte/transition';

	import { Card } from '$lib/components/basic';
	import FAQ from '$lib/components/faq/FAQ.svelte';

	import { makeOptions } from '$lib/scripts/option';
	import { Pruefstelle, type ps } from '$lib/api';
	import { addAlert } from '$lib/scripts/alerts';

	export let readProfile: ps.ProfileRead;
	export let classes = [];
	classes = ['sidebar', ...classes];
	export let fromCase = false;
	export let refreshState: RefreshState;

	let startHidden = true;
	let updated = {};
	const handleSubmit = async (event) => {
		const data = {};
		options.forEach((option) => (data[option.key] = option.value));
		try {
			readProfile = await Pruefstelle.updateProfile(readProfile.id, data);
			await refreshState();
			startHidden = false;
			updated = {};
		} catch (error) {
			addAlert({ message: 'Update fehlgeschlagen', type: 'error' });
		}
	};

	const options = makeOptions(readProfile);

	$: optionValueChanged = options.some((option) => option.value !== readProfile[option.key]);
	let wasInformed = false;
	$: if (!wasInformed && !fromCase && optionValueChanged) {
		wasInformed = true;
		addAlert({
			message: 'Nota bene: Eine Änderung des Fallprofils gilt immer für den gesamten Fall.'
		});
	}
</script>

{#key updated}
	<article class={classes.join(' ')} in:fade>
		<Card {startHidden}>
			<svelte:fragment slot="title">
				<FAQ forTerm="options">Fallprofil</FAQ>
			</svelte:fragment>

			<form class="mt-4 form-control" on:submit|preventDefault={handleSubmit}>
				{#each options as option}
					<label class="label cursor-pointer">
						<span class="label-text">
							{@html option.label}
						</span>
						<input
							type="checkbox"
							class="checkbox checkbox-sm"
							bind:checked={option.show}
							on:click={() => option.clicked()} />
					</label>
					{#if option.show}
						<div class="ml-6 mb-2 text-sm w-3/4" in:fade|local>
							<label class="label" for={option.key}
								><span class="label-text">
									{@html option.conditionalLabel(option.value)}
								</span>
							</label>
							<input
								type="range"
								min={option.suggestMin}
								max={option.suggestMax}
								bind:value={option.value}
								class="range range-sm"
								step={option.suggestStep}
								name={option.key} />
						</div>
					{/if}
				{/each}
				{#if optionValueChanged}
					<div class="mx-auto mt-2" in:fade|local>
						<button class="btn btn-primary">Änderungen übernehmen</button>
					</div>
				{/if}
			</form>
		</Card>
	</article>
{/key}
