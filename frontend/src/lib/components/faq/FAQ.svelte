<script>
	export let forTerm;
	export let classes = [];
	export let fixedSize = true;
</script>

<slot />
<label for="faq-{forTerm}" class="modal-button cursor-pointer {classes.join(' ')}">
	<i class="fas fa-info-circle text-info" class:text-sm={fixedSize} />
</label>
