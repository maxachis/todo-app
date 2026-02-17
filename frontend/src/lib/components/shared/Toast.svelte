<script lang="ts">
	import type { Toast } from '$lib/stores/toast';
	import { dismissToast } from '$lib/stores/toast';

	let {
		toast
	}: {
		toast: Toast;
	} = $props();

	const typeClass = $derived(toast.type ?? 'info');
</script>

<div class="toast {typeClass}">
	<span class="message">{toast.message}</span>
	{#if toast.actionLabel && toast.onAction}
		<button class="action" onclick={() => { toast.onAction?.(); dismissToast(toast.id); }}>
			{toast.actionLabel}
		</button>
	{/if}
	<button class="dismiss" onclick={() => dismissToast(toast.id)} aria-label="Dismiss">✕</button>
</div>

<style>
	.toast {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		padding: 0.65rem 0.85rem;
		border-radius: var(--radius-lg);
		font-size: 0.85rem;
		font-family: var(--font-body);
		box-shadow: var(--shadow-lg);
		animation: slide-in 0.25s ease;
	}

	.info {
		background: var(--bg-nav);
		color: var(--text-on-dark);
	}

	.success {
		background: var(--success);
		color: #f0fdf4;
	}

	.error {
		background: var(--error);
		color: #fef2f2;
	}

	.message {
		flex: 1;
	}

	.action {
		background: rgba(255, 255, 255, 0.18);
		border: 1px solid rgba(255, 255, 255, 0.25);
		color: inherit;
		border-radius: var(--radius-sm);
		padding: 0.22rem 0.5rem;
		cursor: pointer;
		font-size: 0.78rem;
		font-weight: 600;
		font-family: var(--font-body);
		transition: background var(--transition);
	}

	.action:hover {
		background: rgba(255, 255, 255, 0.3);
	}

	.dismiss {
		background: transparent;
		border: none;
		color: inherit;
		cursor: pointer;
		opacity: 0.5;
		padding: 0.1rem;
		transition: opacity var(--transition);
	}

	.dismiss:hover {
		opacity: 1;
	}

	@keyframes slide-in {
		from {
			transform: translateY(0.75rem);
			opacity: 0;
		}
		to {
			transform: translateY(0);
			opacity: 1;
		}
	}
</style>
