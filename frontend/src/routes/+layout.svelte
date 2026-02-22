<script lang="ts">
	import favicon from '$lib/assets/favicon.svg';
	import ListSidebar from '$lib/components/lists/ListSidebar.svelte';
	import TaskDetail from '$lib/components/tasks/TaskDetail.svelte';
	import ToastContainer from '$lib/components/shared/ToastContainer.svelte';
	import SearchBar from '$lib/components/search/SearchBar.svelte';
	import ResizeHandle from '$lib/components/shared/ResizeHandle.svelte';
	import { page } from '$app/stores';
	import { selectedTaskStore } from '$lib/stores/tasks';
	import { sidebarWidth, detailWidth, savePanelWidths, clampWidths } from '$lib/stores/panelWidths';
	import { themePreference, cycleTheme, type ThemePreference } from '$lib/stores/theme';

	const themeIcons: Record<ThemePreference, string> = {
		light: '\u2600\uFE0F',
		system: '\uD83D\uDCBB',
		dark: '\uD83C\uDF19'
	};

	let { children } = $props();
	let sidebarOpen = $state(false);
	let detailOpen = $state(false);
	let innerWidth = $state(typeof window !== 'undefined' ? window.innerWidth : 1200);
	const isTasksRoute = $derived($page.url.pathname === '/');

	const panelGridStyle = $derived(
		isTasksRoute
			? `grid-template-columns: ${$sidebarWidth}px 6px 1fr 6px ${$detailWidth}px`
			: ''
	);

	$effect(() => {
		clampWidths(innerWidth);
	});

	$effect(() => {
		if ($selectedTaskStore !== null) {
			detailOpen = true;
		}
	});

	const tabs = [
		{ href: '/', label: 'Tasks' },
		{ href: '/upcoming', label: 'Upcoming' },
		{ href: '/projects', label: 'Projects' },
		{ href: '/timesheet', label: 'Timesheet' },
		{ href: '/import', label: 'Import' },
		{ href: '/people', label: 'People' },
		{ href: '/organizations', label: 'Orgs' },
		{ href: '/interactions', label: 'Interactions' },
		{ href: '/relationships', label: 'Relationships' },
		{ href: '/graph', label: 'Graph' }
	];
</script>

<svelte:window bind:innerWidth />

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

<div class="app-shell">
	<header class="top-nav">
		<button class="icon-btn mobile-only" onclick={() => (sidebarOpen = !sidebarOpen)} aria-label="Toggle sidebar">
			&#9776;
		</button>
		<nav>
			{#each tabs as tab}
				<a href={tab.href} class:active={$page.url.pathname === tab.href}>{tab.label}</a>
			{/each}
		</nav>
		<div class="nav-spacer"></div>
		{#if isTasksRoute}
			<SearchBar />
		{/if}
		{#if isTasksRoute}
			<button class="icon-btn mobile-only" onclick={() => (detailOpen = true)} aria-label="Open detail panel">
				&#8942;
			</button>
		{/if}
		<button class="theme-toggle" onclick={cycleTheme} aria-label="Theme: {$themePreference}" title="Theme: {$themePreference}">
			{themeIcons[$themePreference]}
		</button>
	</header>

	<main class="panels" class:single-panel={!isTasksRoute} style={panelGridStyle}>
		{#if isTasksRoute}
			<aside id="sidebar" class:open={sidebarOpen}>
				<ListSidebar />
			</aside>
			<ResizeHandle
				onDrag={(delta) => sidebarWidth.update((w) => Math.max(180, w + delta))}
				onDragEnd={savePanelWidths}
			/>
		{/if}

		<section id="center-panel" class="center-panel">
			{@render children()}
		</section>

		{#if isTasksRoute}
			<ResizeHandle
				onDrag={(delta) => detailWidth.update((w) => Math.max(220, w - delta))}
				onDragEnd={savePanelWidths}
			/>
			<section id="detail-panel" class="detail-panel" class:open={detailOpen}>
				<div class="detail-header">
					<strong>Task Detail</strong>
					<button class="icon-btn mobile-only" onclick={() => (detailOpen = false)} aria-label="Close detail panel">
						&#10005;
					</button>
				</div>
				<TaskDetail />
			</section>
		{/if}
	</main>

	<ToastContainer />

	<nav class="mobile-tabs">
		{#each tabs as tab}
			<a href={tab.href} class:active={$page.url.pathname === tab.href}>{tab.label}</a>
		{/each}
	</nav>
</div>

<style>
	:global(:root) {
		--font-display: 'Crimson Pro', Georgia, serif;
		--font-body: 'Plus Jakarta Sans', system-ui, sans-serif;
		--font-mono: 'JetBrains Mono', ui-monospace, monospace;

		--bg-page: #f5f2ec;
		--bg-surface: #ffffff;
		--bg-surface-hover: #f3efe8;
		--bg-surface-active: rgba(180, 88, 40, 0.07);
		--bg-nav: #2c2825;
		--bg-input: #ffffff;

		--text-primary: #2c2825;
		--text-secondary: #6b6560;
		--text-tertiary: #9e9891;
		--text-on-dark: #ede9e1;
		--text-on-dark-muted: #a8a29e;

		--accent: #b45828;
		--accent-hover: #9a4a20;
		--accent-light: rgba(180, 88, 40, 0.07);
		--accent-medium: rgba(180, 88, 40, 0.14);

		--border: #ddd7ce;
		--border-light: #ece7df;
		--border-focus: #b45828;
		--border-nav: rgba(255, 255, 255, 0.1);

		--pinned-bg: rgba(200, 155, 60, 0.08);
		--pinned-border: rgba(200, 155, 60, 0.3);
		--pinned-text: #8a6914;
		--pinned-tag-bg: rgba(200, 155, 60, 0.12);

		--tag-bg: #ece7df;
		--tag-text: #6b6560;

		--success: #3d7a50;
		--success-bg: #eef7f0;
		--success-border: #b6dfc4;
		--error: #b83f3f;
		--error-bg: #fdf0f0;
		--error-border: #f0c4c4;

		--backdrop: rgba(44, 40, 37, 0.4);

		--shadow-sm: 0 1px 3px rgba(60, 50, 40, 0.05);
		--shadow-md: 0 4px 14px rgba(60, 50, 40, 0.07);
		--shadow-lg: 0 8px 28px rgba(60, 50, 40, 0.1);

		--radius-sm: 0.375rem;
		--radius-md: 0.5rem;
		--radius-lg: 0.75rem;
		--radius-xl: 1rem;

		--transition: 0.18s ease;
	}

	:global(:root[data-theme='dark']) {
		--bg-page: #1a1816;
		--bg-surface: #262220;
		--bg-surface-hover: #302c28;
		--bg-surface-active: rgba(212, 117, 62, 0.1);
		--bg-nav: #1a1816;
		--bg-input: #302c28;

		--text-primary: #ede9e1;
		--text-secondary: #a8a29e;
		--text-tertiary: #78716c;
		--text-on-dark: #ede9e1;
		--text-on-dark-muted: #a8a29e;

		--accent: #d4753e;
		--accent-hover: #e08a55;
		--accent-light: rgba(212, 117, 62, 0.1);
		--accent-medium: rgba(212, 117, 62, 0.18);

		--border: #3d3733;
		--border-light: #332e2a;
		--border-focus: #d4753e;
		--border-nav: rgba(255, 255, 255, 0.08);

		--pinned-bg: rgba(200, 155, 60, 0.12);
		--pinned-border: rgba(200, 155, 60, 0.25);
		--pinned-text: #c9a84c;
		--pinned-tag-bg: rgba(200, 155, 60, 0.15);

		--tag-bg: #332e2a;
		--tag-text: #a8a29e;

		--success: #5cb176;
		--success-bg: rgba(92, 177, 118, 0.12);
		--success-border: rgba(92, 177, 118, 0.25);
		--error: #e06060;
		--error-bg: rgba(224, 96, 96, 0.12);
		--error-border: rgba(224, 96, 96, 0.25);

		--backdrop: rgba(0, 0, 0, 0.5);

		--shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.15);
		--shadow-md: 0 4px 14px rgba(0, 0, 0, 0.2);
		--shadow-lg: 0 8px 28px rgba(0, 0, 0, 0.25);
	}

	:global(body) {
		margin: 0;
		font-family: var(--font-body);
		background: var(--bg-page);
		color: var(--text-primary);
		-webkit-font-smoothing: antialiased;
		-moz-osx-font-smoothing: grayscale;
	}

	:global(*, *::before, *::after) {
		box-sizing: border-box;
	}

	:global(::selection) {
		background: var(--accent-medium);
		color: var(--text-primary);
	}

	.app-shell {
		height: 100vh;
		display: grid;
		grid-template-rows: auto 1fr auto;
		overflow: hidden;
	}

	.top-nav {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 0.75rem;
		padding: 0.65rem 1.25rem;
		background: var(--bg-nav);
		border-bottom: 1px solid rgba(255, 255, 255, 0.06);
	}

	.top-nav nav {
		display: flex;
		gap: 0.25rem;
		flex-wrap: wrap;
	}

	a {
		color: var(--text-on-dark-muted);
		text-decoration: none;
		font-weight: 500;
		font-size: 0.875rem;
		padding: 0.35rem 0.65rem;
		border-radius: var(--radius-sm);
		transition: color var(--transition), background var(--transition);
	}

	a:hover {
		color: var(--text-on-dark);
		background: rgba(255, 255, 255, 0.06);
	}

	a.active {
		color: var(--text-on-dark);
		background: rgba(255, 255, 255, 0.1);
		font-weight: 600;
	}

	.theme-toggle {
		background: transparent;
		border: 1px solid var(--border-nav);
		border-radius: var(--radius-sm);
		padding: 0.25rem 0.45rem;
		font-size: 0.9rem;
		cursor: pointer;
		line-height: 1;
		transition: background var(--transition);
	}

	.theme-toggle:hover {
		background: rgba(255, 255, 255, 0.08);
	}

	.nav-spacer {
		flex: 1;
	}

	.panels {
		display: grid;
		column-gap: 0.5rem;
		padding: 0.875rem;
		min-height: 0;
	}

	.panels.single-panel {
		grid-template-columns: 1fr !important;
	}

	aside,
	.center-panel,
	.detail-panel {
		background: var(--bg-surface);
		border: 1px solid var(--border);
		border-radius: var(--radius-xl);
		padding: 1rem;
		box-shadow: var(--shadow-sm);
		min-height: 0;
		overflow-x: hidden;
		overflow-y: auto;
	}

	aside {
		overflow: hidden;
		min-height: 0;
	}

	.icon-btn {
		background: transparent;
		border: 1px solid var(--border-nav);
		color: var(--text-on-dark);
		border-radius: var(--radius-sm);
		padding: 0.25rem 0.5rem;
		cursor: pointer;
		transition: background var(--transition);
	}

	.icon-btn:hover {
		background: rgba(255, 255, 255, 0.08);
	}

	.detail-header strong {
		font-family: var(--font-display);
		font-size: 1.05rem;
		font-weight: 600;
		color: var(--text-primary);
	}

	.mobile-tabs {
		display: none;
	}

	.mobile-only {
		display: none;
	}

	@media (max-width: 1023px) {
		.app-shell {
			height: auto;
			min-height: 100vh;
			overflow: visible;
		}

		.mobile-only {
			display: inline-flex;
		}

		.panels {
			grid-template-columns: 1fr !important;
			padding-bottom: 5rem;
		}

		.panels :global(.resize-handle) {
			display: none;
		}

		aside {
			display: none;
		}

		aside.open {
			display: block;
		}

		.detail-panel {
			position: fixed;
			top: 0;
			right: -100%;
			bottom: 0;
			width: min(92vw, 360px);
			z-index: 30;
			transition: right 0.25s ease;
			border-radius: 0;
			overflow-y: auto;
		}

		.detail-panel.open {
			right: 0;
		}

		.detail-header {
			display: flex;
			align-items: center;
			justify-content: space-between;
		}

		.mobile-tabs {
			position: fixed;
			left: 0;
			right: 0;
			bottom: 0;
			display: flex;
			overflow-x: auto;
			-webkit-overflow-scrolling: touch;
			background: var(--bg-nav);
			border-top: 1px solid rgba(255, 255, 255, 0.08);
			padding: 0.6rem 0.4rem;
		}

		.mobile-tabs a {
			text-align: center;
			font-size: 0.8rem;
			flex: 0 0 auto;
			padding: 0.35rem 0.55rem;
		}
	}
</style>
