<script lang="ts">
	import { searchStore, performSearch, clearSearch } from '$lib/stores/search';
	import SearchResults from './SearchResults.svelte';

	let query = $state('');
	let debounceTimer: ReturnType<typeof setTimeout> | null = null;
	let showResults = $state(false);

	function handleInput(): void {
		if (debounceTimer) clearTimeout(debounceTimer);
		const q = query.trim();
		if (!q) {
			clearSearch();
			showResults = false;
			return;
		}
		debounceTimer = setTimeout(() => {
			performSearch(q);
			showResults = true;
		}, 300);
	}

	function handleClickOutside(event: MouseEvent): void {
		const target = event.target as HTMLElement;
		if (!target.closest('.search-wrapper')) {
			showResults = false;
		}
	}

	function handleFocus(): void {
		if ($searchStore && $searchStore.total_count > 0) {
			showResults = true;
		}
	}
</script>

<svelte:window onclick={handleClickOutside} />

<div class="search-wrapper">
	<input
		class="search-input"
		bind:value={query}
		oninput={handleInput}
		onfocus={handleFocus}
		placeholder="Search tasks..."
	/>
	{#if showResults && $searchStore}
		<SearchResults
			results={$searchStore}
			onNavigate={() => {
				showResults = false;
				query = '';
				clearSearch();
			}}
		/>
	{/if}
</div>

<style>
	.search-wrapper {
		position: relative;
	}

	.search-input {
		border: 1px solid var(--border-nav);
		background: rgba(255, 255, 255, 0.07);
		color: var(--text-on-dark);
		border-radius: var(--radius-md);
		padding: 0.35rem 0.65rem;
		font-size: 0.82rem;
		font-family: var(--font-body);
		width: 220px;
		transition: all var(--transition);
	}

	.search-input::placeholder {
		color: var(--text-on-dark-muted);
	}

	.search-input:focus {
		outline: none;
		border-color: var(--accent);
		background: rgba(255, 255, 255, 0.12);
		box-shadow: 0 0 0 2px rgba(180, 88, 40, 0.15);
	}
</style>
