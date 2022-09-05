<script>
	/*
		User-related navigational elements
	*/
	import { page } from '$app/stores';
	export let asDropdown = true;

	const items = [
		{
			label: ' beobachtet',
			icon: 'fa-star',
			target: '/dashboard/user/has/onwatch'
		},
		{
			label: 'bewertet',
			icon: 'fa-gavel',
			target: '/dashboard/user/has/evaluated'
		},
		{
			label: 'Mail ändern',
			icon: 'fa-envelope',
			target: '/dashboard/user/mail'
		},
		{
			label: 'Passwort ändern',
			icon: 'fa-key',
			target: '/dashboard/user/password'
		},
		{ isLink: true, label: 'Abmelden', icon: 'fa-sign-out', target: '/auth?logout' }
	];
</script>

{#if asDropdown}
	<div class="dropdown dropdown-end">
		<button
			tabindex="0"
			id="user-button"
			class="btn rounded-btn gap-2 lowercase"
			class:btn-ghost={!$page.url.pathname.includes('/dashboard/user')}
			class:btn-primary={$page.url.pathname.includes('/dashboard/user')}>
			<i class="fas fa-user" />
		</button>
		<ul tabindex="0" class="menu dropdown-content p-2 shadow bg-base-100 rounded-box w-52 ">
			{#each items as item}
				<li>
					<a href={item.target} class:text-error={item.label === 'Abmelden'}>
						{#if 'icon' in item} <i class="fas {item.icon}" />{/if}
						{item.label}
					</a>
				</li>
			{/each}
		</ul>
	</div>
{:else}
	{#each items as item}
		<a
			href={item.target}
			class="btn btn-primary btn-md gap-2"
			class:btn-error={item.label === 'Abmelden'}>
			{#if 'icon' in item} <i class="fas {item.icon}" />{/if}
			{item.label}
		</a>
	{/each}
{/if}
