<script lang="ts">
	import { toastStore } from '$lib/stores/toast';
	import Toast from './Toast.svelte';
</script>

{#if $toastStore.length > 0}
	<div class="toast-container">
		{#each $toastStore as toast (toast.id)}
			<Toast {toast} />
		{/each}
	</div>
{/if}

<style>
	.toast-container {
		position: fixed;
		bottom: 1.5rem;
		right: 1.5rem;
		display: flex;
		flex-direction: column-reverse;
		gap: 0.5rem;
		z-index: 100;
		max-width: min(400px, 90vw);
	}

	@media (max-width: 1023px) {
		.toast-container {
			bottom: 5rem;
			right: 0.75rem;
			left: 0.75rem;
			max-width: none;
		}
	}
</style>
