<script>
	import { page } from '$app/stores';
	import Breadcrumbs from '$lib/components/navigation/Breadcrumbs.svelte';
</script>

<div class="relative bg-primary pt-24 pb-24 text-primary-content shadow-lg ">
	<div class="absolute top-0 left-0 w-full flex items-center p-4">
		<div class="w-full mx-auto items-center flex justify-between px-4">
			<Breadcrumbs page={$page} classes={['text-primary-content']} />
		</div>
	</div>
</div>
