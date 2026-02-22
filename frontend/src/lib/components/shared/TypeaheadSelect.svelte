<script lang="ts">
	let {
		options,
		placeholder = '',
		onSelect,
		value = $bindable<number | null>(null)
	}: {
		options: { id: number; label: string }[];
		placeholder?: string;
		onSelect?: (id: number) => void;
		value?: number | null;
	} = $props();

	let inputText = $state('');
	let isOpen = $state(false);
	let highlightIndex = $state(-1);
	let container: HTMLDivElement;
	let inputEl: HTMLInputElement;

	const isBoundMode = $derived(value !== undefined && onSelect === undefined);

	const filtered = $derived(
		inputText
			? options.filter((o) => o.label.toLowerCase().includes(inputText.toLowerCase()))
			: options
	);

	const selectedLabel = $derived(
		isBoundMode && value != null
			? (options.find((o) => o.id === value)?.label ?? '')
			: ''
	);

	let displayText = $state('');

	$effect(() => {
		if (isBoundMode && !isOpen && selectedLabel) {
			displayText = selectedLabel;
		}
	});

	function open() {
		if (filtered.length > 0) {
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

	function handleInput(e: Event) {
		const target = e.target as HTMLInputElement;
		inputText = target.value;
		displayText = target.value;
		highlightIndex = -1;
		if (inputText && filtered.length > 0) {
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
				highlightIndex = (highlightIndex + 1) % filtered.length;
				break;
			case 'ArrowUp':
				e.preventDefault();
				highlightIndex = (highlightIndex - 1 + filtered.length) % filtered.length;
				break;
			case 'Enter':
				e.preventDefault();
				if (filtered.length > 0) {
					const idx = highlightIndex >= 0 ? highlightIndex : 0;
					selectOption(filtered[idx]);
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
				close();
				break;
		}
	}

	function handleClickOutside(e: MouseEvent) {
		if (container && !container.contains(e.target as Node)) {
			close();
			if (onSelect) {
				inputText = '';
				displayText = '';
			} else if (selectedLabel) {
				displayText = selectedLabel;
				inputText = '';
			}
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
	{#if isOpen && filtered.length > 0}
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
</style>
