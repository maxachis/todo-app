<script lang="ts">
	import { marked } from 'marked';
	import DOMPurify from 'dompurify';

	let {
		value = '',
		onSave = (_value: string) => {}
	}: {
		value?: string;
		onSave?: (value: string) => void | Promise<void>;
	} = $props();

	let editingIndex = $state<number | null>(null);
	let draft = $state('');

	const blocks = $derived(() => {
		const normalized = value ?? '';
		if (!normalized.trim()) {
			return [''];
		}
		return normalized.split(/\n\s*\n/);
	});

	const isEmpty = $derived(() => {
		const b = blocks();
		return b.length === 1 && !b[0].trim();
	});

	function startEdit(index: number): void {
		editingIndex = index;
		draft = blocks()[index] ?? '';
	}

	async function commit(index: number): Promise<void> {
		const nextBlocks = [...blocks()];
		nextBlocks[index] = draft;
		const nextValue = nextBlocks.join('\n\n').trim();
		editingIndex = null;
		await onSave(nextValue);
	}

	function renderMarkdown(raw: string): string {
		const html = marked.parse(raw || '');
		return DOMPurify.sanitize(typeof html === 'string' ? html : '');
	}
</script>

<div class="markdown-editor">
	{#each blocks() as block, index}
		{#if editingIndex === index}
			<textarea
				class="block-editor"
				bind:value={draft}
				rows="4"
				onblur={() => commit(index)}
				onkeydown={(event) => {
					if (event.key === 'Escape') editingIndex = null;
					if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
						event.preventDefault();
						commit(index);
					}
				}}
			></textarea>
		{:else if isEmpty() && index === 0}
			<div
				class="block-placeholder"
				role="button"
				tabindex="0"
				onclick={() => startEdit(0)}
				onkeydown={(event) => {
					if (event.key === 'Enter' || event.key === ' ') {
						event.preventDefault();
						startEdit(0);
					}
				}}
			>
				Click to add notes...
			</div>
		{:else}
			<div
				class="block-render"
				role="button"
				tabindex="0"
				onclick={() => startEdit(index)}
				onkeydown={(event) => {
					if (event.key === 'Enter' || event.key === ' ') {
						event.preventDefault();
						startEdit(index);
					}
				}}
			>
				{@html renderMarkdown(block)}
			</div>
		{/if}
	{/each}
</div>

<style>
	.markdown-editor {
		display: grid;
		gap: 0.45rem;
	}

	.block-editor {
		width: 100%;
		border: 1px solid var(--border-focus);
		border-radius: var(--radius-sm);
		padding: 0.5rem 0.6rem;
		font-size: 0.85rem;
		font-family: var(--font-mono);
		color: var(--text-primary);
		background: var(--bg-input);
		resize: vertical;
	}

	.block-editor:focus {
		outline: none;
	}

	.block-placeholder {
		border: 1px dashed var(--border-light);
		border-radius: var(--radius-sm);
		padding: 0.45rem 0.55rem;
		cursor: text;
		font-size: 0.88rem;
		line-height: 1.6;
		color: var(--text-muted);
		font-style: italic;
		transition: all var(--transition);
	}

	.block-placeholder:hover,
	.block-placeholder:focus-visible {
		border-color: var(--border-focus);
		background: var(--bg-surface-hover);
		outline: none;
	}

	.block-render {
		position: relative;
		border: 1px solid transparent;
		border-radius: var(--radius-sm);
		padding: 0.45rem 0.55rem;
		cursor: text;
		transition: all var(--transition);
		font-size: 0.88rem;
		line-height: 1.6;
		color: var(--text-primary);
	}

	.block-render::after {
		content: '\270E';
		position: absolute;
		top: 0.3rem;
		right: 0.4rem;
		font-size: 0.75rem;
		color: var(--text-muted);
		opacity: 0;
		transition: opacity var(--transition);
		pointer-events: none;
	}

	.block-render:hover,
	.block-render:focus-visible {
		border-color: var(--border-light);
		background: var(--bg-surface-hover);
		outline: none;
	}

	.block-render:hover::after,
	.block-render:focus-visible::after {
		opacity: 1;
	}

	.block-render :global(p) {
		margin: 0.3rem 0;
	}

	.block-render :global(pre) {
		background: var(--bg-nav);
		color: var(--text-on-dark);
		padding: 0.55rem 0.65rem;
		border-radius: var(--radius-sm);
		overflow-x: auto;
		font-family: var(--font-mono);
		font-size: 0.82rem;
	}

	.block-render :global(code) {
		font-family: var(--font-mono);
		font-size: 0.84em;
	}

	.block-render :global(a) {
		color: var(--accent);
		text-decoration: underline;
		text-underline-offset: 2px;
	}
</style>
