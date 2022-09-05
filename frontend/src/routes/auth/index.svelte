<script context="module" lang="ts">
	import { makePruefstelle } from '$lib/api';
	import { resetUser, setUser } from '$lib/scripts/auth';
	export const load = async ({ url, fetch }) => {
		const pruefstelle = makePruefstelle({ customFetch: fetch });

		const isLinkLogin = url.searchParams.has('link') && url.searchParams.get('link') != '';
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
				return { props: { isLinkLogin, isLogout, redirect, failed } };
			} catch (error) {
				failed = true;
				return { props: { isLinkLogin, isLogout, redirect, failed } };
			}
		}

		if (isLinkLogin) {
			const link = url.searchParams.get('link');
			try {
				const readUser = await pruefstelle.loginByLink({ token: link });
				setUser(readUser);
				url.searchParams.delete('link');
				goto(redirect);
				return { props: { isLinkLogin, isLogout, redirect, failed } };
			} catch (error) {
				if (error.status !== 401) {
					// only disable in this case
					failed = true;
				}
				return { props: { isLinkLogin, isLogout, redirect, failed } };
			}
		}

		return { props: { isLinkLogin, isLogout, redirect, failed } };
	};
</script>

<script lang="ts">
	import { fade } from 'svelte/transition';
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import { onDestroy } from 'svelte';

	import { LoginByLink, Login } from '$lib/components/login';

	export let isLogout: boolean;
	export let isLinkLogin: boolean;
	export let redirect: string;
	export let failed: boolean;

	let isDisabled = failed;

	let email = '';
	let showPasswordLogin = false;

	const fadeInfo = setTimeout(() => {
		isLogout = false;
		isLinkLogin = false;
	}, 5000);

	onDestroy(() => clearTimeout(fadeInfo));
</script>

{#if isDisabled}
	<p>Diese Aktion ist zur Zeit nicht möglich.</p>
	<p>Bitte versuche es später noch einmal.</p>
{:else}
	{#if isLinkLogin}
		<div out:fade>
			<p>Das hat leider nicht geklappt. Vermutlich ist der Link zu alt.</p>
			<p class="mt-2">Lass dir einen neuen schicken oder wähle dich mit deinem Passwort ein.</p>
		</div>
	{/if}
	{#if isLogout}
		<div out:fade>
			<p>Du hast dich abgemeldet.</p>
		</div>
	{/if}
	{#if showPasswordLogin}
		<Login bind:email bind:isDisabled {redirect} />
	{:else}
		<LoginByLink bind:email bind:isDisabled />
	{/if}
	<a
		href={$page.url.toString()}
		class="btn btn-sm btn-ghost w-full"
		on:click={() => (showPasswordLogin = !showPasswordLogin)}>
		{showPasswordLogin === true ? 'Ohne' : 'Mit'} Passwort anmelden</a>
{/if}
