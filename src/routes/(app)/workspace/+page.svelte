<script lang="ts">
	import { goto } from '$app/navigation';
	import { WEBUI_BASE_PATH } from '$lib/constants';
	import { onMount } from 'svelte';

	onMount(() => {
		goto(`${WEBUI_BASE_PATH}/workspace/models`);
	});
</script>
