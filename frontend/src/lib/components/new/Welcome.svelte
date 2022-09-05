<script>
	import Card from '$lib/components/basic/Card.svelte';
	import { focusElement } from '$lib/utils';
</script>

<Card isHideable={false} isWide={true} classes={['w-96', 'mx-auto']}>
	<svelte:fragment slot="title">Neuen Fall hinzufügen</svelte:fragment>

	<div class="prose">
		<ul>
			<li>
				Klicke rechts auf <strong class="uppercase"><i class="fas fa-forward" /> Weiter</strong>, um
				loszulegen.
			</li>
			<li>
				Dieser Assistent führt dich durch alle Schritte. Wenn Du mal nicht weiter weißt, klicke
				rechts auf <strong class="uppercase"><i class="fas fa-question" /> Hilfe</strong>.
			</li>
			<li>
				Damit gleich alles flott geht, werden vorab ein paar Daten geladen. Das kann einen kurzen
				Moment (wenige Sekunden) dauern.
			</li>
		</ul>
		<p class="text-sm mt-2 prose">
			Besonders umfangreiche Fälle lassen sich alternativ auch
			<button class="link" on:click={() => focusElement('more-button')}>
				programmatisch einspielen.
			</button>
		</p>
	</div>
</Card>
