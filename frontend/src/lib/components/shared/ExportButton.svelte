<script lang="ts">
	import { api } from '$lib';

	let {
		listId = null,
		label = 'Export'
	}: {
		listId?: number | null;
		label?: string;
	} = $props();

	let showMenu = $state(false);

	async function doExport(format: 'json' | 'csv' | 'markdown'): Promise<void> {
		showMenu = false;
		const blob = listId !== null
			? await api.export.one(listId, format)
			: await api.export.all(format);

		const ext = format === 'markdown' ? 'md' : format;
		const filename = listId !== null ? `list-${listId}.${ext}` : `all-lists.${ext}`;

		const url = URL.createObjectURL(blob);
		const a = document.createElement('a');
		a.href = url;
		a.download = filename;
		a.click();
		URL.revokeObjectURL(url);
	}

	function handleClickOutside(event: MouseEvent): void {
		const target = event.target as HTMLElement;
		if (!target.closest('.export-wrapper')) {
			showMenu = false;
		}
	}
</script>

<svelte:window onclick={handleClickOutside} />

<div class="export-wrapper">
	<button class="export-btn" onclick={() => (showMenu = !showMenu)}>{label}</button>
	{#if showMenu}
		<div class="export-menu">
			<button onclick={() => doExport('json')}>JSON</button>
			<button onclick={() => doExport('csv')}>CSV</button>
			<button onclick={() => doExport('markdown')}>Markdown</button>
		</div>
	{/if}
</div>

<style>
	.export-wrapper {
		position: relative;
		display: inline-block;
	}

	.export-btn {
		border: 1px solid var(--border);
		background: var(--bg-surface);
		border-radius: var(--radius-sm);
		padding: 0.3rem 0.6rem;
		cursor: pointer;
		font-size: 0.78rem;
		font-family: var(--font-body);
		color: var(--text-secondary);
		transition: all var(--transition);
	}

	.export-btn:hover {
		background: var(--bg-surface-hover);
		border-color: var(--accent);
		color: var(--accent);
	}

	.export-menu {
		position: absolute;
		top: 100%;
		right: 0;
		background: var(--bg-surface);
		border: 1px solid var(--border);
		border-radius: var(--radius-md);
		box-shadow: var(--shadow-md);
		z-index: 20;
		margin-top: 0.3rem;
		display: grid;
		min-width: 110px;
		overflow: hidden;
	}

	.export-menu button {
		background: transparent;
		border: none;
		cursor: pointer;
		padding: 0.45rem 0.8rem;
		text-align: left;
		font-size: 0.83rem;
		font-family: var(--font-body);
		color: var(--text-primary);
		transition: background var(--transition);
	}

	.export-menu button:hover {
		background: var(--bg-surface-hover);
	}
</style>
