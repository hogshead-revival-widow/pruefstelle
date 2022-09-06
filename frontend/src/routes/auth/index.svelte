<script context="module" lang="ts">
	import { makePruefstelle } from '$lib/api';
	import { resetUser, setUser } from '$lib/scripts/auth';
	export const load = async ({ url, fetch }) => {
		const pruefstelle = makePruefstelle({ customFetch: fetch });

		const isLogout = url.searchParams.has('logout');
		const redirect = url.searchParams.has('redirect')
			? url.searchParams.get('redirect')
			: '/dashboard';
		let failed = false;

		// logout
		if (isLogout) {
			try {
				await pruefstelle.logout();
				resetUser();
				url.searchParams.delete('logout');
				return { props: { isLogout, redirect, failed } };
			} catch (error) {
				failed = true;
				return { props: { isLogout, redirect, failed } };
			}
		}

		return { props: { isLogout, redirect, failed } };
	};
</script>

<script lang="ts">
	import { fade } from 'svelte/transition';
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import { onDestroy } from 'svelte';

	import Login from '$lib/components/Login.svelte';

	export let isLogout: boolean;
	export let redirect: string;
	export let failed: boolean;

	let isDisabled = failed;

	let email = '';
	let showPasswordLogin = true;

	const fadeInfo = setTimeout(() => {
		isLogout = false;
	}, 5000);

	onDestroy(() => clearTimeout(fadeInfo));
</script>

{#if isDisabled}
	<p>Diese Aktion ist zur Zeit nicht möglich.</p>
	<p>Bitte versuche es später noch einmal.</p>
{:else}
	{#if isLogout}
		<div out:fade>
			<p>Du hast dich abgemeldet.</p>
		</div>
	{/if}
	{#if showPasswordLogin}
		<Login bind:email bind:isDisabled {redirect} />
	{/if}
{/if}
