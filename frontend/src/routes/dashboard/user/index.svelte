<script>
	import { UserActions } from '$lib/components/navigation';
	import Card from '$lib/components/basic/Card.svelte';
</script>

<Card isWide={true} isHideable={false} classes={['h-fit']}>
	<svelte:fragment slot="title">Meine Aktionen</svelte:fragment>
	<UserActions asDropdown={false} />
</Card>
