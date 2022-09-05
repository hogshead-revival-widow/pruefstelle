<script>
	import { goto } from '$app/navigation';
	import { isLoggedIn } from '$lib/scripts/auth';

	const redirect = async () => {
		if (!(await isLoggedIn())) {
			goto('/auth');
		}
		goto('/dashboard');
	};

	redirect();
</script>
