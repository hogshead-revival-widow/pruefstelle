<script>
	/*
		Wrap slotted content in modal
	*/
	export let id;
	export let showCloseButton = false;
	export let wrapInBox = false;
	export let classes = [];
	export let hasFixedWidth = true;

	if (wrapInBox) {
		classes = ['modal-box', ...classes];
	}
	if (hasFixedWidth) classes.push('w-98');
</script>

{#if !showCloseButton}
	<input type="checkbox" {id} class="modal-toggle" />
	<label for={id} class="modal cursor-pointer">
		<label class="{classes.join(' ')} relative" for="">
			<slot />
		</label>
	</label>
{:else}
	<input type="checkbox" {id} class="modal-toggle" />
	<div class="modal">
		<div class="{classes.join(' ')} relative">
			<label for={id} class="btn btn-sm btn-circle absolute right-2 top-2">✕</label>
			<div>
				<slot />
			</div>
		</div>
	</div>
{/if}
