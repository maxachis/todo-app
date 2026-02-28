<script lang="ts">
	import { addToast } from '$lib/stores/toast';

	let {
		options,
		placeholder = '',
		onSelect,
		onCreate,
		value = $bindable<number | null>(null)
	}: {
		options: { id: number; label: string }[];
		placeholder?: string;
		onSelect?: (id: number) => void;
		onCreate?: (name: string) => Promise<{ id: number; label: string }>;
		value?: number | null;
	} = $props();

	let inputText = $state('');
	let isOpen = $state(false);
	let highlightIndex = $state(-1);
	let creating = $state(false);
	let container: HTMLDivElement;
	let inputEl: HTMLInputElement;

	const isBoundMode = $derived(value !== undefined && onSelect === undefined);

	const filtered = $derived(
		inputText
			? options.filter((o) => o.label.toLowerCase().includes(inputText.toLowerCase()))
			: options
	);

	const hasExactMatch = $derived(
		inputText.trim() !== '' &&
			options.some((o) => o.label.toLowerCase() === inputText.trim().toLowerCase())
	);

	const showCreateOption = $derived(
		onCreate !== undefined && inputText.trim() !== '' && !hasExactMatch
	);

	const showNoMatch = $derived(
		onCreate === undefined && inputText.trim() !== '' && filtered.length === 0
	);

	// Total navigable items: filtered options + optional create item
	const totalItems = $derived(filtered.length + (showCreateOption ? 1 : 0));
	const createIndex = $derived(filtered.length); // create item is always last

	const selectedLabel = $derived(
		isBoundMode && value != null
			? (options.find((o) => o.id === value)?.label ?? '')
			: ''
	);

	let displayText = $state('');

	$effect(() => {
		if (isBoundMode && !isOpen) {
			displayText = selectedLabel;
		}
	});

	function open() {
		if (filtered.length > 0 || showCreateOption || showNoMatch) {
			isOpen = true;
			highlightIndex = -1;
		}
	}

	function close() {
		isOpen = false;
		highlightIndex = -1;
	}

	function selectOption(opt: { id: number; label: string }) {
		if (onSelect) {
			onSelect(opt.id);
			inputText = '';
			displayText = '';
		} else {
			value = opt.id;
			displayText = opt.label;
			inputText = '';
		}
		close();
	}

	async function handleCreate() {
		if (!onCreate || !inputText.trim() || creating) return;
		creating = true;
		try {
			const newOpt = await onCreate(inputText.trim());
			selectOption(newOpt);
		} finally {
			creating = false;
		}
	}

	function handleInput(e: Event) {
		const target = e.target as HTMLInputElement;
		inputText = target.value;
		displayText = target.value;
		highlightIndex = -1;
		if (inputText && (filtered.length > 0 || showCreateOption || showNoMatch)) {
			isOpen = true;
		} else if (!inputText && options.length > 0) {
			isOpen = true;
		} else {
			isOpen = false;
		}
	}

	function handleFocus() {
		if (!isOpen) {
			open();
		}
	}

	function handleKeydown(e: KeyboardEvent) {
		if (!isOpen) {
			if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
				open();
				e.preventDefault();
			}
			return;
		}

		switch (e.key) {
			case 'ArrowDown':
				e.preventDefault();
				if (totalItems > 0) {
					highlightIndex = (highlightIndex + 1) % totalItems;
				}
				break;
			case 'ArrowUp':
				e.preventDefault();
				if (totalItems > 0) {
					highlightIndex = (highlightIndex - 1 + totalItems) % totalItems;
				}
				break;
			case 'Enter':
				e.preventDefault();
				if (totalItems > 0) {
					const idx = highlightIndex >= 0 ? highlightIndex : 0;
					if (idx === createIndex && showCreateOption) {
						handleCreate();
					} else if (idx < filtered.length) {
						selectOption(filtered[idx]);
					}
				}
				break;
			case 'Escape':
				e.preventDefault();
				close();
				if (onSelect) {
					inputText = '';
					displayText = '';
				} else if (selectedLabel) {
					displayText = selectedLabel;
					inputText = '';
				}
				break;
			case 'Tab':
				handleBlur();
				break;
		}
	}

	function handleBlur() {
		if (onSelect) {
			// Action mode: clear input
			inputText = '';
			displayText = '';
			close();
			return;
		}

		const trimmed = inputText.trim();

		// Nothing typed or same as current selection — just close
		if (!trimmed || trimmed.toLowerCase() === selectedLabel.toLowerCase()) {
			close();
			return;
		}

		// Exact match with an existing option — auto-select it
		const exactMatch = options.find(
			(o) => o.label.toLowerCase() === trimmed.toLowerCase()
		);
		if (exactMatch) {
			selectOption(exactMatch);
			return;
		}

		// Unmatched text with onCreate available — auto-create
		if (onCreate && !creating) {
			creating = true;
			close();
			onCreate(trimmed)
				.then((newOpt) => {
					selectOption(newOpt);
				})
				.finally(() => {
					creating = false;
				});
			return;
		}

		// Unmatched text, no onCreate — revert with toast
		if (!onCreate) {
			addToast({ message: `No match found for "${trimmed}"`, type: 'info' });
		}
		displayText = selectedLabel;
		inputText = '';
		close();
	}

	function handleClickOutside(e: MouseEvent) {
		if (container && !container.contains(e.target as Node)) {
			handleBlur();
		}
	}

	function optionId(index: number): string {
		return `typeahead-option-${index}`;
	}

	const activeDescendant = $derived(
		isOpen && highlightIndex >= 0 ? optionId(highlightIndex) : undefined
	);
</script>

<svelte:window onclick={handleClickOutside} />

<div class="typeahead" bind:this={container}>
	<input
		type="text"
		class="typeahead-input"
		{placeholder}
		value={displayText}
		oninput={handleInput}
		onfocus={handleFocus}
		onkeydown={handleKeydown}
		bind:this={inputEl}
		role="combobox"
		aria-autocomplete="list"
		aria-expanded={isOpen}
		aria-activedescendant={activeDescendant}
		aria-controls="typeahead-listbox"
		autocomplete="off"
	/>
	{#if isOpen && (filtered.length > 0 || showCreateOption || showNoMatch)}
		<ul class="typeahead-dropdown" role="listbox" id="typeahead-listbox">
			{#each filtered as opt, i (opt.id)}
				<li
					id={optionId(i)}
					class="typeahead-option"
					class:highlighted={i === highlightIndex}
					role="option"
					aria-selected={i === highlightIndex}
					onmousedown={(e) => { e.preventDefault(); selectOption(opt); }}
					onmouseenter={() => (highlightIndex = i)}
				>
					{opt.label}
				</li>
			{/each}
			{#if showCreateOption}
				<li
					id={optionId(createIndex)}
					class="typeahead-option typeahead-create"
					class:highlighted={highlightIndex === createIndex}
					role="option"
					aria-selected={highlightIndex === createIndex}
					onmousedown={(e) => { e.preventDefault(); handleCreate(); }}
					onmouseenter={() => (highlightIndex = createIndex)}
				>
					Create "{inputText.trim()}"
				</li>
			{/if}
			{#if showNoMatch}
				<li class="typeahead-option typeahead-no-match" role="status">
					No match found — add it first
				</li>
			{/if}
		</ul>
	{/if}
</div>

<style>
	.typeahead {
		position: relative;
	}

	.typeahead-input {
		width: 100%;
		box-sizing: border-box;
		font-size: 0.8rem;
		font-family: var(--font-body);
		padding: 0.25rem 0.4rem;
		border: 1px solid var(--border);
		border-radius: var(--radius-sm);
		background: var(--bg-input);
		color: var(--text-primary);
	}

	.typeahead-dropdown {
		position: absolute;
		top: 100%;
		left: 0;
		right: 0;
		z-index: 100;
		margin: 0.15rem 0 0;
		padding: 0;
		list-style: none;
		background: var(--bg-surface);
		border: 1px solid var(--border);
		border-radius: var(--radius-sm);
		box-shadow: var(--shadow-md, 0 4px 12px rgba(0, 0, 0, 0.1));
		max-height: 12rem;
		overflow-y: auto;
	}

	.typeahead-option {
		padding: 0.35rem 0.5rem;
		font-size: 0.8rem;
		cursor: pointer;
		color: var(--text-primary);
	}

	.typeahead-option.highlighted {
		background: var(--accent-light, var(--bg-surface-hover));
		color: var(--text-primary);
	}

	.typeahead-create {
		font-style: italic;
		color: var(--accent);
		border-top: 1px solid var(--border-light, var(--border));
	}

	.typeahead-no-match {
		font-style: italic;
		color: var(--text-muted, #999);
		cursor: default;
	}
</style>
