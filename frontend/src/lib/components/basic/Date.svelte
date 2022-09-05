<script lang="ts">
	export let date: string;
	const event = new Date(date);
	const readableDate = event.toLocaleDateString('de-DE');
	const readableTime = event.toLocaleTimeString('de-DE');
</script>

<time datetime={readableDate} title={readableTime}>{readableDate}</time>
