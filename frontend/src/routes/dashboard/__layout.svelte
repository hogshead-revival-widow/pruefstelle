<script context="module">
	import { goto } from '$app/navigation';
	import { isLoggedIn } from '$lib/scripts/auth';
	export const load = async ({ url }) => {
		if (!(await isLoggedIn())) {
			goto(`/auth?redirect=${url.pathname}`);
		}
		return {};
	};
</script>

<script>
	import { Alerts } from '$lib/components/alert';
	import { Navbar, Header } from '$lib/components/navigation';
	import Modal from '$lib/components/Modal.svelte';
	import { FAQs, SingleFAQModals } from '$lib/components/faq';
</script>

<div class="flex flex-col min-h-screen">
	<header>
		<Navbar />
		<Alerts classes={['absolute', 'right-24', 'top-20']} />
		<Header />
	</header>

	<main class="flex-grow flex justify-center -mt-24">
		<slot />

		<aside class="modal-container">
			<SingleFAQModals />
			<article>
				<Modal id="modal-faqs" hasFixedWidth={false}>
					<FAQs />
				</Modal>
			</article>
		</aside>
	</main>
</div>
