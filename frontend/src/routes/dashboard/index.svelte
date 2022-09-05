<script>
	import { Card, ActionBar } from '$lib/components/basic';
	import { FAQ } from '$lib/components/faq/';

	import { focusElement } from '$lib/utils';
</script>

<article>
	<Card isWide={true} isHideable={false}>
		<svelte:fragment slot="title">Übersicht</svelte:fragment>
		<svelte:fragment slot="header">
			<ActionBar>
				<li>
					<button class="action-button" on:click={() => focusElement('search-button')}
						><i class="fas fa-search" />
						Fall Suchen
					</button>
				</li>

				<li>
					<button class="action-button" on:click={() => focusElement('user-button')}>
						<i class="fas fa-user" />Meine Aktionen
					</button>
				</li>
			</ActionBar>
		</svelte:fragment>
		<p class="prose disc-list max-w-md">
			Direkt loslegen: Lege einen <FAQ forTerm="case"
				><a href="/dashboard/new" sveltekit:prefetch>neuen Fall</a></FAQ> an oder schau' dir
			<a href="/dashboard/case" sveltekit:prefetch>bestehende Fälle</a> an.
		</p>

		<p class="text-sm mt-2 prose max-w-md">
			Tipp: Klicke auf das Info-Icon (<i class="fas fa-info-circle text-info m-0 p-0" />), wenn dir
			mal ein Begriff unbekannt vorkommt oder suche
			<button class="link" on:click={() => focusElement('more-button')}> in der FAQ </button>
			danach.
		</p>
		<svelte:fragment slot="footer">
			<a href="/dashboard/new" class="btn btn-primary" sveltekit:prefetch
				><i class="fas fa-plus mr-2" />Neuen Fall anlegen</a>
		</svelte:fragment>
	</Card>
</article>
