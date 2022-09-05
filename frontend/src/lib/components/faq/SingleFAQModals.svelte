<script>
	import { faq } from '$lib/data/faq';
</script>

{#each Object.entries(faq) as [key, question]}
	<article>
		<input type="checkbox" id="faq-{key}" class="modal-toggle" />
		<label for="faq-{key}" class="modal cursor-pointer">
			<label class="modal-box relative" for="faq-{key}">
				<h3 class="text-lg font-bold">{@html question.name}</h3>
				<p class="py-4 prose">
					{@html question.text}
				</p>
			</label>
		</label>
	</article>
{/each}
