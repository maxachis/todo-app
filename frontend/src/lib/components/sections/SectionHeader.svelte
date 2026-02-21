<script lang="ts">
	import { dragHandle } from 'svelte-dnd-action';
	import type { Section } from '$lib';

	let {
		section,
		collapsed = false,
		editingSectionId = null,
		onStartEdit = (_id: number) => {},
		onStopEdit = (_id: number) => {},
		onToggleCollapse = () => {},
		onUpdate = (_changes: { name?: string; emoji?: string }) => {},
		onDelete = () => {}
	}: {
		section: Section;
		collapsed?: boolean;
		editingSectionId?: number | null;
		onStartEdit?: (id: number) => void;
		onStopEdit?: (id: number) => void;
		onToggleCollapse?: () => void;
		onUpdate?: (changes: { name?: string; emoji?: string }) => void;
		onDelete?: () => void;
	} = $props();

	let name = $state('');
	let wasEditing = $state(false);

	const editing = $derived(editingSectionId === section.id);

	$effect(() => {
		if (!editing) {
			name = section.name;
		}
	});

	$effect(() => {
		if (editing && !wasEditing) {
			name = section.name;
		}
		if (!editing && wasEditing) {
			commit();
		}
		wasEditing = editing;
	});

	function startEdit(): void {
		onStartEdit(section.id);
	}

	function commit(): void {
		if (name.trim() && name !== section.name) {
			onUpdate({ name: name.trim() });
		}
		onStopEdit(section.id);
	}

	function handleKeydown(event: KeyboardEvent): void {
		if (event.key === 'Enter') commit();
		if (event.key === 'Escape') {
			onStopEdit(section.id);
		}
	}
</script>

<div class="section-header" data-section-id={section.id}>
	<div class="drag-handle" use:dragHandle aria-label="Drag section" role="button" tabindex="0">⋮⋮</div>
	<button class="collapse-toggle" onclick={onToggleCollapse} aria-label={collapsed ? 'Expand section' : 'Collapse section'}>
		<span class="chevron" class:collapsed>{collapsed ? '▶' : '▼'}</span>
	</button>
	{#if section.emoji}
		<span class="emoji">{section.emoji}</span>
	{/if}
	{#if editing}
		<input
			class="name-input"
			bind:value={name}
			onblur={commit}
			onkeydown={handleKeydown}
		/>
	{:else}
		<span class="name" ondblclick={startEdit} role="button" tabindex="0">{section.name}</span>
	{/if}
	<div class="actions">
		<button class="action-btn" onclick={startEdit} aria-label="Edit section">&#9999;&#65039;</button>
		<button class="action-btn" onclick={() => { if (confirm('Delete this section?')) onDelete(); }} aria-label="Delete section">&#10005;</button>
	</div>
</div>

<style>
	.section-header {
		display: flex;
		align-items: center;
		gap: 0.4rem;
		padding: 0.4rem 0;
		border-bottom: 1px solid var(--border-light);
	}

	.drag-handle {
		border: none;
		background: transparent;
		color: var(--text-tertiary);
		font-size: 0.75rem;
		letter-spacing: -0.05em;
		padding: 0.15rem;
		cursor: grab;
		line-height: 1;
	}

	.collapse-toggle {
		background: transparent;
		border: none;
		cursor: pointer;
		padding: 0.15rem;
		font-size: 0.65rem;
		color: var(--text-tertiary);
		transition: color var(--transition);
	}

	.collapse-toggle:hover {
		color: var(--text-secondary);
	}

	.emoji {
		font-size: 1rem;
	}

	.name {
		font-family: var(--font-display);
		font-weight: 600;
		font-size: 1rem;
		flex: 1;
		cursor: default;
		color: var(--text-primary);
	}

	.name-input {
		flex: 1;
		border: 1px solid var(--border-focus);
		border-radius: var(--radius-sm);
		padding: 0.2rem 0.4rem;
		font-size: 0.95rem;
		font-family: var(--font-display);
		color: var(--text-primary);
	}

	.name-input:focus {
		outline: none;
	}

	.actions {
		display: flex;
		gap: 0.15rem;
		opacity: 0;
		transition: opacity var(--transition);
	}

	.section-header:hover .actions {
		opacity: 1;
	}

	.action-btn {
		background: transparent;
		border: none;
		cursor: pointer;
		color: var(--text-tertiary);
		padding: 0.15rem 0.25rem;
		font-size: 0.8rem;
		border-radius: var(--radius-sm);
		transition: all var(--transition);
	}

	.action-btn:hover {
		background: var(--bg-surface-hover);
		color: var(--text-secondary);
	}
</style>
