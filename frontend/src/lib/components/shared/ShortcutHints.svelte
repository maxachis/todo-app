<script lang="ts">
	interface Shortcut {
		key: string;
		description: string;
	}

	interface Section {
		title: string;
		shortcuts: Shortcut[];
	}

	let { shortcuts, sections }: { shortcuts?: Shortcut[]; sections?: Section[] } = $props();

	let open = $state(false);

	function handleWindowClick(e: MouseEvent) {
		const target = e.target as HTMLElement;
		if (!target.closest('.shortcut-hints')) {
			open = false;
		}
	}
</script>

<svelte:window onclick={open ? handleWindowClick : undefined} />

<div class="shortcut-hints">
	{#if open}
		<div class="shortcut-popover">
			{#if sections}
				{#each sections as section, i}
					<div class="shortcut-section" class:first={i === 0}>
						<div class="shortcut-section-title">{section.title}</div>
						{#each section.shortcuts as s}
							<div class="shortcut-row">
								<kbd class="shortcut-key">{s.key}</kbd>
								<span class="shortcut-desc">{s.description}</span>
							</div>
						{/each}
					</div>
				{/each}
			{:else if shortcuts}
				<div class="shortcut-popover-title">Keyboard Shortcuts</div>
				{#each shortcuts as s}
					<div class="shortcut-row">
						<kbd class="shortcut-key">{s.key}</kbd>
						<span class="shortcut-desc">{s.description}</span>
					</div>
				{/each}
			{/if}
		</div>
	{/if}
	<button
		class="shortcut-badge"
		onclick={() => (open = !open)}
		aria-label="Keyboard shortcuts"
		title="Keyboard shortcuts"
	>?</button>
</div>

<style>
	.shortcut-hints {
		position: fixed;
		bottom: 1rem;
		right: 1rem;
		z-index: 1000;
	}

	.shortcut-badge {
		width: 32px;
		height: 32px;
		border-radius: 50%;
		border: 1px solid var(--border);
		background: var(--bg-surface);
		color: var(--text-secondary);
		font-size: 0.85rem;
		font-weight: 600;
		font-family: var(--font-body);
		cursor: pointer;
		display: grid;
		place-items: center;
		transition: all var(--transition);
		box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
	}

	.shortcut-badge:hover {
		background: var(--bg-surface-hover);
		border-color: var(--accent);
		color: var(--accent);
	}

	.shortcut-popover {
		position: absolute;
		bottom: calc(100% + 0.5rem);
		right: 0;
		background: var(--bg-surface);
		border: 1px solid var(--border);
		border-radius: var(--radius-md, 6px);
		padding: 0.6rem 0.75rem;
		min-width: 220px;
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
	}

	.shortcut-popover-title {
		font-family: var(--font-display);
		font-size: 0.78rem;
		font-weight: 600;
		color: var(--text-tertiary);
		text-transform: uppercase;
		letter-spacing: 0.04em;
		margin-bottom: 0.4rem;
		padding-bottom: 0.3rem;
		border-bottom: 1px solid var(--border-light);
	}

	.shortcut-section {
		padding-top: 0.4rem;
		margin-top: 0.4rem;
		border-top: 1px solid var(--border-light);
	}

	.shortcut-section.first {
		padding-top: 0;
		margin-top: 0;
		border-top: none;
	}

	.shortcut-section-title {
		font-family: var(--font-display);
		font-size: 0.72rem;
		font-weight: 600;
		color: var(--text-tertiary);
		text-transform: uppercase;
		letter-spacing: 0.04em;
		margin-bottom: 0.25rem;
	}

	.shortcut-row {
		display: flex;
		align-items: center;
		gap: 0.6rem;
		padding: 0.2rem 0;
	}

	.shortcut-key {
		display: inline-block;
		min-width: 4.5rem;
		padding: 0.1rem 0.35rem;
		background: var(--bg-input);
		border: 1px solid var(--border-light);
		border-radius: var(--radius-sm);
		font-family: var(--font-mono, monospace);
		font-size: 0.75rem;
		color: var(--text-primary);
		text-align: center;
		white-space: nowrap;
	}

	.shortcut-desc {
		font-size: 0.8rem;
		color: var(--text-secondary);
		white-space: nowrap;
	}
</style>
