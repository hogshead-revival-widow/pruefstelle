<script>
	/*
		Render breadcrumb, cf. match:matchPage
	*/
	import { matchPage, enrichContext } from '$lib/components/navigation/match';
	export let page;
	export let classes = [];

	classes = ['text-sm breadcrumbs', ...classes];

	let crumbs;
	$: {
		const matcher = matchPage(page);
		const fullpath = page.url.pathname;
		crumbs = [];
		const paths = fullpath.split('/');
		let match = undefined;
		paths.shift();
		paths.map((path) => {
			match = matcher
				.filter((matchItem) => !matchItem.matched)
				.find((matchItem) =>
					typeof matchItem.match === 'function' ? matchItem.match(path) : matchItem.match === path
				);
			if (match !== undefined) {
				match.matched = true;
				// This is the actual crumb
				crumbs.push({ label: match.label, icon: match.icon, link: match.getLink() });
			}
		});

		crumbs = enrichContext(page, crumbs);
	}
</script>

<article class={classes.join(' ')}>
	<ul>
		{#each crumbs as crumb}
			<li>
				<a href={crumb.link} sveltekit:prefetch>
					{#if 'icon' in crumb && crumb.icon}<i
							class="fas fa-{crumb.icon} mr-2" />{/if}{@html crumb.label}
				</a>
			</li>
		{/each}
	</ul>
</article>
