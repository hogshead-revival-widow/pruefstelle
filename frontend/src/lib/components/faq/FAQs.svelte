<script>
	import Card from '$lib/components/basic/Card.svelte';
	import { faq } from '$lib/data/faq';
</script>

<Card classes={['max-h-96', 'overflow-auto']} isHideable={false} isWide={true}>
	<sveltekit slot="title"><a href="#faq" id="faq">Häufig gestellte Fragen</a></sveltekit>
	<div class="prose">
		<ul class="text-base">
			{#each Object.entries(faq) as [id, item], i}
				<li>
					<a href="#{id}">{@html item.name}</a>
				</li>
			{/each}
		</ul>
		<dl class="mt-4 text-base">
			{#each Object.entries(faq) as [id, item], i}
				<dt class="lead">
					<a href="#{id}" {id}>{@html item.name} </a>
					<a href="#faq"><icon class="fa fa-chevron-circle-up ml-2 text-sm" /></a>
				</dt>
				<dd>{@html item.text}</dd>
			{/each}
		</dl>
	</div>
</Card>
