<script>
	import { page, navigating } from '$app/stores';

	import ChooseTheme from '$lib/components/ChooseTheme.svelte';
	import UserActions from '$lib/components/navigation/UserActions.svelte';
	import { showModal } from '$lib/scripts/modal';
	import SearchBox from '$lib/components/SearchBox.svelte';
</script>

<nav class="navbar flex justify-end">
	<section class="flex-1 justify-start">
		<a
			sveltekit:prefetch
			href="/dashboard"
			class="btn btn-ghost normal-case text-xl gap-2"
			class:btn-ghost={$page.url.pathname !== '/dashboard'}
			class:btn-primary={$page.url.pathname === '/dashboard'}>
			<i class="fas fa-gavel" class:fa-spinner={$navigating} class:fa-pulse={$navigating} />
			prüfstelle
		</a>
	</section>

	<SearchBox />

	<ul class="menu menu-horizontal p-0 ">
		<li>
			<a
				href="/dashboard/new"
				class="gap-2"
				class:active={$page.url.pathname.includes('/dashboard/new')}
				sveltekit:prefetch>
				<i class="fas fa-plus" />
				Fall
			</a>
		</li>
		<li>
			<a
				href="/dashboard/case"
				class="gap-2"
				class:active={$page.url.pathname === '/dashboard/case'}
				sveltekit:prefetch>
				<i class="fas fa-boxes" />
				Alle
			</a>
		</li>
		<UserActions />

		<div class="dropdown dropdown-end">
			<button id="more-button" tabindex="0" class="btn btn-ghost normal-case rounded-btn gap-2 ">
				<i class="fas fa-archive" />
			</button>
			<ul tabindex="0" class="menu dropdown-content p-2 shadow bg-base-100 rounded-box">
				<li>
					<a href={`${import.meta.env.VITE_API_DOCS_URL}`} rel="external" target="new">
						<i class="fas fa-server" />
						API
					</a>
				</li>

				<li>
					<button
						class="btn btn-ghost rounded-btn gap-2"
						on:click={() => showModal({ id: 'modal-faqs' })}>
						<i class="fas fa-info-circle" /> FAQ
					</button>
				</li>
			</ul>
			<ChooseTheme />
		</div>
	</ul>
</nav>
