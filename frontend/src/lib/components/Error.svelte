<script>
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';

	import Card from '$lib/components/basic/Card.svelte';
	import { handleLogout } from '$lib/scripts/auth';

	export let error;

	let message = 'Unbekannter Fehler';
	let status = undefined;
	if (error?.message) {
		const data = JSON.parse(error.message);
		console.error(data);
		if (data?.error) {
			status = 400;
			message = 'Diese Anfrage wurde nicht verstanden. <br /> Bitte melde den Fehler.';
		}
	} else {
		console.error(error);
	}

	const errorContact = import.meta.env.VITE_MAIL_CONTACT_ERROR;
	const mailMessage = `subject=[Fehler (${status !== undefined ? status : ''})]: ${
		$page.url.pathname
	}]&body=${message}`;
</script>

<article class="max-w-lg">
	<Card isWide={true} isHideable={false}>
		<svelte:fragment slot="title">
			<i class="fas fa-exclamation-triangle gap-2" /> Fehler {#if status !== undefined}({status}){/if}
		</svelte:fragment>

		<p class="prose">
			{@html message}
		</p>

		<svelte:fragment slot="footer">
			<button
				on:click|once={() => {
					history.back();
				}}
				class="btn btn-primary gap-2">
				<i class="fas fa-arrow-left" />
				Zurück
			</button>
			<button
				on:click|once={async () => {
					await handleLogout();
					goto('/auth');
				}}
				class="btn btn-primary gap-2">
				<i class="fas fa-sign-in" />
				Neue Anmeldung
			</button>

			<a href="mailto:{errorContact}?{mailMessage}" class="btn  gap-2 "
				><i class="fas fa-envelope" />Melden
			</a>
		</svelte:fragment>
	</Card>
</article>
