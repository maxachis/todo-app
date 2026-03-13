<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import { createNotesEditor, type NotesEditorInstance } from './createNotesEditor';

	let {
		value = '',
		onSave = (_value: string) => {}
	}: {
		value?: string;
		onSave?: (value: string) => void | Promise<void>;
	} = $props();

	let container: HTMLDivElement;
	let editor: NotesEditorInstance | null = null;
	let currentContent = '';
	let lastPropValue = value;

	onMount(() => {
		currentContent = value;
		lastPropValue = value;
		editor = createNotesEditor(container, value, {
			onChange: (content) => {
				currentContent = content;
			},
			onBlur: () => {
				onSave(currentContent);
			}
		});
	});

	onDestroy(() => {
		editor?.destroy();
	});

	// Only sync when the prop value changes externally
	$effect(() => {
		if (editor && value !== lastPropValue) {
			lastPropValue = value;
			currentContent = value;
			editor.setContent(value);
		}
	});
</script>

<div class="notes-editor" bind:this={container}></div>

<style>
	.notes-editor {
		border: 1px solid var(--border);
		border-radius: var(--radius-sm);
		min-height: 80px;
		background: var(--bg-input);
		transition: border-color var(--transition);
	}

	.notes-editor:focus-within {
		border-color: var(--border-focus);
	}

	.notes-editor :global(.cm-editor) {
		height: auto;
		min-height: 80px;
	}

	.notes-editor :global(.cm-content) {
		min-height: 60px;
		padding: 0.5rem 0.6rem;
		font-size: 0.85rem;
	}

	.notes-editor :global(.cm-scroller) {
		overflow: visible;
	}
</style>
