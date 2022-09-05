<script context="module">
	import { goto } from '$app/navigation';
	import { isLoggedIn } from '$lib/scripts/auth';
	export const load = async ({ url }) => {
		const redirect =
			url.searchParams.has('redirect') && url.searchParams.get('redirect') != ''
				? url.searchParams.get('redirect')
				: '/dashboard';
		const isLogout = url.searchParams.has('logout');
		if (!isLogout && (await isLoggedIn())) {
			goto(redirect);
		}

		return {};
	};
</script>

<script lang="ts">
	import ChooseTheme from '$lib/components/ChooseTheme.svelte';
</script>

<section class=" w-full h-full py-40 min-h-screen text-primary-content">
	<div class="absolute top-0 w-full h-full auth-background">
		<div class="mx-auto max-w-xs mt-20">
			<div class="m-2 grid content-center">
				<h1 class="btn btn-ghost normal-case text-xl gap-2">
					<i class="fas fa-gavel" />prüfstelle
				</h1>
			</div>
			<slot />
			<div class="mt-4 footer-center">
				<ChooseTheme />
			</div>
		</div>
	</div>
</section>
