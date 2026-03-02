<script lang="ts">
	import { api } from '$lib/api';
	import type { Page, PageListItem, PageBacklink, Person, Organization, Project } from '$lib/api/types';
	import type { Task } from '$lib/api/types';
	import { onMount, onDestroy } from 'svelte';
	import { goto } from '$app/navigation';
	import { page as pageStore } from '$app/stores';
	import { addToast } from '$lib/stores/toast';

	let pages = $state<PageListItem[]>([]);
	let currentPage = $state<Page | null>(null);
	let titleDraft = $state('');
	let contentDraft = $state('');
	let saving = $state(false);
	let saveTimer: ReturnType<typeof setTimeout> | null = null;

	// Sidebar collapse state
	let sidebarCollapsed = $state(
		typeof localStorage !== 'undefined' && localStorage.getItem('notebook-sidebar-collapsed') === 'true'
	);

	$effect(() => {
		localStorage.setItem('notebook-sidebar-collapsed', String(sidebarCollapsed));
	});

	// Typeahead state
	let textareaEl: HTMLTextAreaElement | undefined = $state();
	let typeaheadOpen = $state(false);
	let typeaheadType = $state<'person' | 'entity'>('person');
	let typeaheadQuery = $state('');
	let typeaheadStart = $state(0);
	let typeaheadIndex = $state(0);
	let typeaheadPosition = $state({ top: 0, left: 0 });

	// Entity data for typeahead
	let allPeople = $state<Person[]>([]);
	let allOrgs = $state<Organization[]>([]);
	let allProjects = $state<Project[]>([]);
	let allTasks = $state<{ id: number; title: string }[]>([]);

	interface TypeaheadItem {
		type: string;
		id: number;
		label: string;
	}

	const filteredPeople = $derived<TypeaheadItem[]>(
		typeaheadType === 'person'
			? allPeople
					.filter(
						(p) =>
							`${p.first_name} ${p.last_name}`
								.toLowerCase()
								.includes(typeaheadQuery.toLowerCase())
					)
					.slice(0, 8)
					.map((p) => ({
						type: 'person',
						id: p.id,
						label: `${p.first_name} ${p.last_name}`
					}))
			: []
	);

	const filteredEntities = $derived.by<TypeaheadItem[]>(() => {
		if (typeaheadType !== 'entity') return [];
		const q = typeaheadQuery.toLowerCase();
		const results: TypeaheadItem[] = [];

		for (const pg of pages) {
			if (pg.title.toLowerCase().includes(q)) {
				results.push({ type: 'page', id: pg.id, label: pg.title });
			}
		}
		for (const t of allTasks) {
			if (t.title.toLowerCase().includes(q)) {
				results.push({ type: 'task', id: t.id, label: t.title });
			}
		}
		for (const o of allOrgs) {
			if (o.name.toLowerCase().includes(q)) {
				results.push({ type: 'org', id: o.id, label: o.name });
			}
		}
		for (const p of allProjects) {
			if (p.name.toLowerCase().includes(q)) {
				results.push({ type: 'project', id: p.id, label: p.name });
			}
		}
		return results.slice(0, 12);
	});

	const typeaheadItems = $derived<TypeaheadItem[]>(
		typeaheadType === 'person' ? filteredPeople : filteredEntities
	);

	const typeBadge: Record<string, string> = {
		page: '\u{1F4C4}',
		task: '\u2713',
		org: '\u{1F3E2}',
		project: '\u{1F4CB}',
		person: '\u{1F464}'
	};

	const wikiPages = $derived(pages.filter((p) => p.page_type === 'wiki'));
	const dailyPages = $derived(pages.filter((p) => p.page_type === 'daily'));

	function handleSidebarShortcut(e: KeyboardEvent) {
		if (e.key === '\\' && (e.metaKey || e.ctrlKey)) {
			e.preventDefault();
			sidebarCollapsed = !sidebarCollapsed;
		}
	}

	onMount(async () => {
		document.addEventListener('keydown', handleSidebarShortcut);
		await loadPages();
		await loadEntityData();

		// Check URL hash for slug
		const slug = $pageStore.url.searchParams.get('p');
		if (slug) {
			await openPage(slug);
		}
	});

	onDestroy(() => {
		document.removeEventListener('keydown', handleSidebarShortcut);
	});

	async function loadPages() {
		try {
			pages = await api.notebook.pages.list();
		} catch (e) {
			console.error('Failed to load pages:', e);
			addToast({ message: 'Failed to load notebook pages', type: 'error' });
		}
	}

	async function loadEntityData() {
		try {
			const [people, orgs, projects] = await Promise.all([
				api.people.getAll(),
				api.organizations.getAll(),
				api.projects.getAll()
			]);
			allPeople = people;
			allOrgs = orgs;
			allProjects = projects;

			// Flatten tasks from all lists
			const lists = await api.lists.getAll();
			const tasks: { id: number; title: string }[] = [];
			for (const list of lists) {
				for (const section of list.sections) {
					const collectTasks = (t: Task) => {
						tasks.push({ id: t.id, title: t.title });
						for (const sub of t.subtasks) collectTasks(sub);
					};
					for (const task of section.tasks) collectTasks(task);
				}
			}
			allTasks = tasks;
		} catch (e) {
			console.error('Failed to load entity data:', e);
		}
	}

	async function openPage(slug: string) {
		try {
			currentPage = await api.notebook.pages.get(slug);
			titleDraft = currentPage.title;
			contentDraft = currentPage.content;
			goto(`/notebook?p=${slug}`, { replaceState: true, noScroll: true });
		} catch (e) {
			console.error('Failed to open page:', e);
			addToast({ message: 'Failed to open page', type: 'error' });
		}
	}

	async function createPage() {
		try {
			const created = await api.notebook.pages.create({ title: 'Untitled' });
			await loadPages();
			await openPage(created.slug);
			// Focus title input after tick
			await new Promise((r) => setTimeout(r, 50));
			document.querySelector<HTMLInputElement>('.editor-title')?.select();
		} catch (e) {
			console.error('Failed to create page:', e);
			addToast({ message: 'Failed to create page', type: 'error' });
		}
	}

	async function openToday() {
		try {
			const today = new Date().toISOString().split('T')[0];
			const created = await api.notebook.pages.create({ page_type: 'daily', date: today });
			await loadPages();
			await openPage(created.slug);
		} catch (e) {
			console.error('Failed to open today page:', e);
			addToast({ message: 'Failed to open today page', type: 'error' });
		}
	}

	async function savePage() {
		if (!currentPage || saving) return;
		saving = true;
		try {
			const oldSlug = currentPage.slug;
			const updated = await api.notebook.pages.update(currentPage.slug, {
				title: titleDraft,
				content: contentDraft
			});
			currentPage = updated;
			// Sync local content with server (checkbox-to-task rewrites)
			if (updated.content !== contentDraft) {
				contentDraft = updated.content;
			}
			// Only update sidebar and URL when slug changed (title edits)
			if (updated.slug !== oldSlug) {
				await loadPages();
				goto(`/notebook?p=${updated.slug}`, { replaceState: true, noScroll: true });
			}
		} catch (e) {
			console.error('Failed to save page:', e);
			addToast({ message: 'Failed to save page', type: 'error' });
		}
		saving = false;
	}

	function debouncedSave() {
		if (saveTimer) clearTimeout(saveTimer);
		saveTimer = setTimeout(savePage, 1000);
	}

	function handleTitleBlur() {
		if (saveTimer) clearTimeout(saveTimer);
		savePage();
	}

	function handleContentBlur() {
		if (saving) return;
		if (saveTimer) clearTimeout(saveTimer);
		savePage();
	}

	async function deletePage() {
		if (!currentPage) return;
		if (!confirm(`Delete "${currentPage.title}"?`)) return;
		try {
			await api.notebook.pages.remove(currentPage.slug);
			currentPage = null;
			titleDraft = '';
			contentDraft = '';
			goto('/notebook', { replaceState: true, noScroll: true });
			await loadPages();
		} catch (e) {
			console.error('Failed to delete page:', e);
			addToast({ message: 'Failed to delete page', type: 'error' });
		}
	}

	// Typeahead logic
	function getCaretCoords(textarea: HTMLTextAreaElement, position: number) {
		const div = document.createElement('div');
		const style = getComputedStyle(textarea);
		for (const prop of ['fontFamily', 'fontSize', 'fontWeight', 'letterSpacing', 'lineHeight', 'padding', 'border', 'whiteSpace', 'wordWrap', 'width'] as const) {
			(div.style as unknown as Record<string, string>)[prop] = style.getPropertyValue(
				prop.replace(/[A-Z]/g, (m) => `-${m.toLowerCase()}`)
			);
		}
		div.style.position = 'absolute';
		div.style.visibility = 'hidden';
		div.style.overflow = 'hidden';
		div.style.whiteSpace = 'pre-wrap';
		div.style.wordWrap = 'break-word';

		const text = textarea.value.substring(0, position);
		div.textContent = text;

		const span = document.createElement('span');
		span.textContent = textarea.value.substring(position) || '.';
		div.appendChild(span);

		document.body.appendChild(div);
		const rect = textarea.getBoundingClientRect();
		const spanRect = span.getBoundingClientRect();
		const divRect = div.getBoundingClientRect();

		const top = rect.top + (spanRect.top - divRect.top) - textarea.scrollTop + 20;
		const left = rect.left + (spanRect.left - divRect.left);
		document.body.removeChild(div);
		return { top, left };
	}

	function handleContentInput() {
		debouncedSave();
		checkTypeahead();
	}

	function checkTypeahead() {
		if (!textareaEl) return;
		const pos = textareaEl.selectionStart;
		const text = contentDraft.substring(0, pos);

		// Check for [[ trigger
		const bracketMatch = text.match(/\[\[([^\]]*)$/);
		if (bracketMatch) {
			typeaheadType = 'entity';
			typeaheadQuery = bracketMatch[1];
			typeaheadStart = pos - bracketMatch[0].length;
			typeaheadIndex = 0;
			typeaheadPosition = getCaretCoords(textareaEl, pos);
			typeaheadOpen = true;
			return;
		}

		// Check for @ trigger (word boundary)
		const atMatch = text.match(/(?:^|[\s(])@([a-zA-Z]*)$/);
		if (atMatch) {
			typeaheadType = 'person';
			typeaheadQuery = atMatch[1];
			typeaheadStart = pos - atMatch[0].length + (atMatch[0].startsWith('@') ? 0 : 1);
			typeaheadIndex = 0;
			typeaheadPosition = getCaretCoords(textareaEl, pos);
			typeaheadOpen = true;
			return;
		}

		typeaheadOpen = false;
	}

	function selectTypeaheadItem(item: TypeaheadItem) {
		if (!textareaEl) return;
		const pos = textareaEl.selectionStart;
		const before = contentDraft.substring(0, typeaheadStart);
		const after = contentDraft.substring(pos);

		let insertion: string;
		if (item.type === 'person') {
			insertion = `@[person:${item.id}|${item.label}]`;
		} else {
			const typeKey = item.type === 'organization' ? 'org' : item.type;
			insertion = `[[${typeKey}:${item.id}|${item.label}]]`;
		}

		contentDraft = before + insertion + after;
		typeaheadOpen = false;

		// Restore cursor position
		const newPos = before.length + insertion.length;
		requestAnimationFrame(() => {
			if (textareaEl) {
				textareaEl.focus();
				textareaEl.setSelectionRange(newPos, newPos);
			}
		});
		debouncedSave();
	}

	function handleTextareaKeydown(event: KeyboardEvent) {
		if (!typeaheadOpen) return;

		if (event.key === 'ArrowDown') {
			event.preventDefault();
			typeaheadIndex = Math.min(typeaheadIndex + 1, typeaheadItems.length - 1);
		} else if (event.key === 'ArrowUp') {
			event.preventDefault();
			typeaheadIndex = Math.max(typeaheadIndex - 1, 0);
		} else if (event.key === 'Enter' && typeaheadItems.length > 0) {
			event.preventDefault();
			selectTypeaheadItem(typeaheadItems[typeaheadIndex]);
		} else if (event.key === 'Escape') {
			event.preventDefault();
			typeaheadOpen = false;
		}
	}
</script>

<div class="notebook-layout" class:collapsed={sidebarCollapsed}>
	<aside class="page-sidebar" class:collapsed={sidebarCollapsed}>
		{#if sidebarCollapsed}
			<button
				class="sidebar-toggle"
				onclick={() => (sidebarCollapsed = false)}
				title="Expand sidebar (Ctrl+\)"
			>&#x25B6;</button>
		{:else}
			<div class="sidebar-header">
				<div class="sidebar-actions">
					<button class="btn-primary" onclick={createPage}>+ New Page</button>
					<button class="btn-secondary" onclick={openToday}>Today</button>
				</div>
				<button
					class="sidebar-toggle"
					onclick={() => (sidebarCollapsed = true)}
					title="Collapse sidebar (Ctrl+\)"
				>&#x25C0;</button>
			</div>

		{#if wikiPages.length > 0}
			<div class="sidebar-group">
				<h3 class="sidebar-group-title">Recent</h3>
				{#each wikiPages as pg (pg.id)}
					<button
						class="page-item"
						class:active={currentPage?.id === pg.id}
						onclick={() => openPage(pg.slug)}
					>
						{pg.title}
					</button>
				{/each}
			</div>
		{/if}

		{#if dailyPages.length > 0}
			<div class="sidebar-group">
				<h3 class="sidebar-group-title">Daily</h3>
				{#each dailyPages as pg (pg.id)}
					<button
						class="page-item"
						class:active={currentPage?.id === pg.id}
						onclick={() => openPage(pg.slug)}
					>
						{pg.title}
					</button>
				{/each}
			</div>
		{/if}

		{#if pages.length === 0}
			<p class="empty-hint">No pages yet. Create one to get started.</p>
		{/if}
		{/if}
	</aside>

	<div class="editor-area">
		{#if currentPage}
			<div class="editor-header">
				<input
					class="editor-title"
					type="text"
					bind:value={titleDraft}
					oninput={debouncedSave}
					onblur={handleTitleBlur}
					placeholder="Page title..."
				/>
				<div class="editor-meta">
					<span class="page-type-badge">{currentPage.page_type}</span>
					{#if saving}
						<span class="save-indicator">Saving...</span>
					{/if}
					<button class="btn-danger-sm" onclick={deletePage}>Delete</button>
				</div>
			</div>

			<div class="editor-content-wrapper">
				<textarea
					class="editor-textarea"
					bind:this={textareaEl}
					bind:value={contentDraft}
					oninput={handleContentInput}
					onblur={handleContentBlur}
					onkeydown={handleTextareaKeydown}
					placeholder="Start writing... Use @ to mention people, [[ to link pages, tasks, orgs, or projects."
				></textarea>

				{#if typeaheadOpen && typeaheadItems.length > 0}
					<div
						class="typeahead-dropdown"
						style="top: {typeaheadPosition.top}px; left: {typeaheadPosition.left}px;"
					>
						{#each typeaheadItems as item, i (item.type + item.id)}
							<button
								class="typeahead-item"
								class:highlighted={i === typeaheadIndex}
								onmousedown={(e: MouseEvent) => { e.preventDefault(); selectTypeaheadItem(item); }}
								onmouseenter={() => (typeaheadIndex = i)}
							>
								<span class="type-badge">{typeBadge[item.type] || ''}</span>
								<span class="item-label">{item.label}</span>
								<span class="item-type">{item.type}</span>
							</button>
						{/each}
					</div>
				{/if}
			</div>

			{#if currentPage.backlinks.length > 0}
				<div class="backlinks-section">
					<h3 class="backlinks-title">Backlinks</h3>
					{#each currentPage.backlinks as bl (bl.id)}
						<button class="backlink-item" onclick={() => openPage(bl.slug)}>
							<span class="backlink-page-type">{bl.page_type === 'daily' ? '\u{1F4C5}' : '\u{1F4C4}'}</span>
							<span class="backlink-label">{bl.title}</span>
							<span class="backlink-snippet">{bl.snippet}</span>
						</button>
					{/each}
				</div>
			{/if}
		{:else}
			<div class="empty-state">
				<p>Select a page or create a new one to start writing.</p>
			</div>
		{/if}
	</div>
</div>

<style>
	.notebook-layout {
		display: grid;
		grid-template-columns: 220px 1fr;
		gap: 0.75rem;
		height: 100%;
		min-height: 0;
		transition: grid-template-columns 200ms ease;
	}

	.notebook-layout.collapsed {
		grid-template-columns: 32px 1fr;
		gap: 0;
	}

	.page-sidebar {
		border-right: 1px solid var(--border-light);
		padding-right: 0.75rem;
		overflow-y: auto;
		overflow-x: hidden;
		min-height: 0;
	}

	.page-sidebar.collapsed {
		padding-right: 0;
		overflow: hidden;
		display: flex;
		align-items: flex-start;
		justify-content: center;
		padding-top: 0.35rem;
	}

	.sidebar-header {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
		margin-bottom: 1rem;
	}

	.sidebar-actions {
		display: flex;
		gap: 0.5rem;
	}

	.sidebar-toggle {
		background: transparent;
		border: none;
		color: var(--text-tertiary);
		cursor: pointer;
		padding: 0.2rem 0.4rem;
		font-size: 0.7rem;
		border-radius: var(--radius-sm);
		transition: color var(--transition), background var(--transition);
		align-self: flex-end;
	}

	.sidebar-toggle:hover {
		color: var(--text-primary);
		background: var(--bg-surface-hover);
	}

	.page-sidebar.collapsed .sidebar-toggle {
		align-self: center;
		font-size: 0.75rem;
		padding: 0.3rem;
	}

	.btn-primary {
		flex: 1;
		padding: 0.4rem 0.6rem;
		background: var(--accent);
		color: white;
		border: none;
		border-radius: var(--radius-sm);
		font-size: 0.8rem;
		font-weight: 600;
		cursor: pointer;
		font-family: var(--font-body);
		transition: background var(--transition);
	}

	.btn-primary:hover {
		background: var(--accent-hover);
	}

	.btn-secondary {
		flex: 1;
		padding: 0.4rem 0.6rem;
		background: var(--bg-surface);
		color: var(--text-primary);
		border: 1px solid var(--border);
		border-radius: var(--radius-sm);
		font-size: 0.8rem;
		font-weight: 600;
		cursor: pointer;
		font-family: var(--font-body);
		transition: all var(--transition);
	}

	.btn-secondary:hover {
		background: var(--bg-surface-hover);
	}

	.sidebar-group {
		margin-bottom: 1rem;
	}

	.sidebar-group-title {
		font-family: var(--font-display);
		font-size: 0.75rem;
		font-weight: 600;
		color: var(--text-tertiary);
		text-transform: uppercase;
		letter-spacing: 0.05em;
		margin: 0 0 0.35rem 0;
		padding: 0 0.3rem;
	}

	.page-item {
		display: block;
		width: 100%;
		text-align: left;
		padding: 0.35rem 0.5rem;
		border: none;
		background: transparent;
		border-radius: var(--radius-sm);
		font-size: 0.85rem;
		color: var(--text-primary);
		cursor: pointer;
		font-family: var(--font-body);
		transition: background var(--transition);
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
	}

	.page-item:hover {
		background: var(--bg-surface-hover);
	}

	.page-item.active {
		background: var(--accent-light);
		color: var(--accent);
		font-weight: 600;
	}

	.empty-hint {
		font-size: 0.82rem;
		color: var(--text-tertiary);
		padding: 0.5rem;
		font-style: italic;
	}

	.editor-area {
		display: flex;
		flex-direction: column;
		min-height: 0;
		overflow-y: auto;
	}

	.editor-header {
		margin-bottom: 0.75rem;
	}

	.editor-title {
		width: 100%;
		border: none;
		font-family: var(--font-display);
		font-size: 1.5rem;
		font-weight: 700;
		color: var(--text-primary);
		background: transparent;
		padding: 0;
		margin-bottom: 0.35rem;
	}

	.editor-title:focus {
		outline: none;
	}

	.editor-title::placeholder {
		color: var(--text-tertiary);
	}

	.editor-meta {
		display: flex;
		align-items: center;
		gap: 0.5rem;
	}

	.page-type-badge {
		font-size: 0.72rem;
		font-weight: 600;
		text-transform: uppercase;
		color: var(--text-tertiary);
		background: var(--tag-bg);
		padding: 0.15rem 0.4rem;
		border-radius: var(--radius-sm);
		letter-spacing: 0.03em;
	}

	.save-indicator {
		font-size: 0.75rem;
		color: var(--text-tertiary);
		font-style: italic;
	}

	.btn-danger-sm {
		margin-left: auto;
		padding: 0.2rem 0.5rem;
		background: transparent;
		color: var(--error);
		border: 1px solid var(--error-border);
		border-radius: var(--radius-sm);
		font-size: 0.75rem;
		cursor: pointer;
		font-family: var(--font-body);
		transition: all var(--transition);
	}

	.btn-danger-sm:hover {
		background: var(--error-bg);
	}

	.editor-content-wrapper {
		position: relative;
		flex: 1;
		min-height: 0;
	}

	.editor-textarea {
		width: 100%;
		min-height: 300px;
		height: 100%;
		border: 1px solid var(--border-light);
		border-radius: var(--radius-sm);
		padding: 0.75rem;
		font-family: var(--font-body);
		font-size: 0.9rem;
		line-height: 1.7;
		color: var(--text-primary);
		background: var(--bg-input);
		resize: vertical;
	}

	.editor-textarea:focus {
		outline: none;
		border-color: var(--border-focus);
	}

	.editor-textarea::placeholder {
		color: var(--text-tertiary);
	}

	.typeahead-dropdown {
		position: fixed;
		z-index: 100;
		background: var(--bg-surface);
		border: 1px solid var(--border);
		border-radius: var(--radius-md);
		box-shadow: var(--shadow-lg);
		max-height: 260px;
		overflow-y: auto;
		min-width: 240px;
		max-width: 360px;
	}

	.typeahead-item {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		width: 100%;
		padding: 0.45rem 0.65rem;
		border: none;
		background: transparent;
		cursor: pointer;
		font-family: var(--font-body);
		font-size: 0.85rem;
		color: var(--text-primary);
		text-align: left;
	}

	.typeahead-item.highlighted {
		background: var(--accent-light);
	}

	.typeahead-item:hover {
		background: var(--bg-surface-hover);
	}

	.type-badge {
		font-size: 0.8rem;
		flex-shrink: 0;
	}

	.item-label {
		flex: 1;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}

	.item-type {
		font-size: 0.7rem;
		color: var(--text-tertiary);
		text-transform: uppercase;
	}

	.backlinks-section {
		margin-top: 1.25rem;
		padding-top: 1rem;
		border-top: 1px solid var(--border-light);
	}

	.backlinks-title {
		font-family: var(--font-display);
		font-size: 0.85rem;
		font-weight: 600;
		color: var(--text-secondary);
		margin: 0 0 0.5rem 0;
	}

	.backlink-item {
		display: flex;
		align-items: flex-start;
		gap: 0.5rem;
		width: 100%;
		padding: 0.4rem 0.5rem;
		border: none;
		background: transparent;
		border-radius: var(--radius-sm);
		cursor: pointer;
		text-align: left;
		font-family: var(--font-body);
		transition: background var(--transition);
	}

	.backlink-item:hover {
		background: var(--bg-surface-hover);
	}

	.backlink-page-type {
		font-size: 0.85rem;
		flex-shrink: 0;
	}

	.backlink-label {
		font-size: 0.85rem;
		font-weight: 600;
		color: var(--accent);
		white-space: nowrap;
		flex-shrink: 0;
	}

	.backlink-snippet {
		font-size: 0.78rem;
		color: var(--text-tertiary);
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}

	.empty-state {
		display: flex;
		align-items: center;
		justify-content: center;
		height: 100%;
		color: var(--text-tertiary);
		font-size: 0.9rem;
	}

	@media (max-width: 640px) {
		.notebook-layout {
			grid-template-columns: 1fr;
		}

		.page-sidebar {
			border-right: none;
			border-bottom: 1px solid var(--border-light);
			padding-right: 0;
			padding-bottom: 0.75rem;
			max-height: 200px;
		}
	}
</style>
