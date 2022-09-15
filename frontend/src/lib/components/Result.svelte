<script lang="ts">
	import { type ps, ResultType } from '$lib/api';
	import FAQ from './faq/FAQ.svelte';

	export let resultRead: ps.AnyResult;
	export let withFAQ = true;

	const renderOptions = {
		[ResultType.Keyword]: {
			toWord: (result: ps.KeywordRead) => result.keyword,
			additionalClasses: (result: ps.KeywordRead) => [],
			faqTerm: (_) => 'keyword'
		},
		[ResultType.NamedEntity]: {
			toWord: (result: ps.NamedEntityRead) => result.label,
			additionalClasses: (result: ps.NamedEntityRead) => [result.type],
			faqTerm: (result: ps.NamedEntityRead) => result.type
		},
		[ResultType.Topic]: {
			toWord: (result: ps.TopicRead) => result.keywords.map((keyword) => keyword.keyword).join('-'),
			additionalClasses: (result: ps.NamedEntityRead) => [],
			faqTerm: (_) => 'keyword'
		}
	};

	let word = '';
	let additionalClasses = [''];
	let faqTerm = '';

	$: {
		const render = renderOptions[resultRead.discriminator];
		// @ts-ignore (result type depends on `resultRead.discriminator`)
		word = render.toWord(resultRead);
		// @ts-ignore
		additionalClasses = render.additionalClasses(resultRead);
		// @ts-ignore
		faqTerm = render.faqTerm(resultRead);
	}
</script>

<span class="{resultRead.discriminator} {additionalClasses.join(' ')}" title={word}>
	{word}
</span>
{#if withFAQ}
	<FAQ forTerm={faqTerm} />
{/if}
