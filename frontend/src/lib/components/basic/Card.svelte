<script>
	export let isWide = false;
	export let isHideable = true;
	export let classes = [];
	export let startHidden = false;
	export let hasBackground = true;
	export let show = true;

	if (hasBackground) {
		classes = ['shadow', 'bg-base-100', ...classes];
	}
	classes = ['card', ...classes];

	if (startHidden) {
		show = false;
		startHidden = false;
	}
</script>

<div class={classes.join(' ')} class:card-compact={!isWide}>
	<div class="card-body">
		{#if $$slots.header || $$slots.title}
			<div class="card-actions justify-end">
				<slot name="header" />
				{#if isHideable}
					<label class="swap swap-flip text-lg">
						<!-- this hidden checkbox controls the state -->
						<input type="checkbox" style="display: none;" bind:checked={show} />
						<div class="swap-on"><i class="fas fa-eye" /></div>
						<div class="swap-off"><i class="fas fa-eye-slash" /></div>
					</label>
				{/if}
			</div>
		{/if}

		{#if $$slots.title}
			<h2 class="card-title"><slot name="title" /></h2>
		{/if}
		{#if show}
			<slot />
		{/if}
		{#if $$slots.footer}
			<div class="mt-4 card-actions justify-end">
				<slot name="footer" />
			</div>
		{/if}
	</div>
</div>
