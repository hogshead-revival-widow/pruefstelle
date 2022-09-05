<script context="module">
	export const load = ({ error, status }) => {
		return {
			props: {
				error: { message: error.message, status: status }
			}
		};
	};
</script>

<script>
	import Error from '$lib/components/Error.svelte';
	export let error;
</script>

<section class="flex items-center justify-center h-screen auth-background">
	<Error {error} />
</section>
