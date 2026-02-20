<script lang="ts">
	import {
		projectsStore,
		loadProjects,
		createProject,
		updateProject,
		toggleProject,
		deleteProject
	} from '$lib/stores/projects';

	let newName = $state('');
	let newDescription = $state('');
	let editingId = $state<number | null>(null);
	let editName = $state('');
	let editDescription = $state('');

	$effect(() => {
		loadProjects();
	});

	async function handleCreate(event: SubmitEvent): Promise<void> {
		event.preventDefault();
		if (!newName.trim()) return;
		await createProject({ name: newName.trim(), description: newDescription.trim() });
		newName = '';
		newDescription = '';
	}

	function startEdit(project: { id: number; name: string; description: string }): void {
		editingId = project.id;
		editName = project.name;
		editDescription = project.description;
	}

	async function commitEdit(): Promise<void> {
		if (editingId === null || !editName.trim()) return;
		await updateProject(editingId, { name: editName.trim(), description: editDescription.trim() });
		editingId = null;
	}

	async function handleDelete(id: number): Promise<void> {
		if (!confirm('Delete this project? Lists will be unlinked, not deleted.')) return;
		await deleteProject(id);
	}
</script>

<section class="projects-page">
	<header>
		<h1>Projects</h1>
	</header>

	<form class="create-form" onsubmit={handleCreate}>
		<input bind:value={newName} placeholder="Project name..." />
		<input bind:value={newDescription} placeholder="Description (optional)" />
		<button type="submit">+ Project</button>
	</form>

	<div class="projects-grid">
		{#each $projectsStore as project (project.id)}
			<div class="project-card" class:inactive={!project.is_active}>
				{#if editingId === project.id}
					<input class="edit-input" bind:value={editName} onkeydown={(e) => { if (e.key === 'Enter') commitEdit(); if (e.key === 'Escape') editingId = null; }} />
					<input class="edit-input" bind:value={editDescription} placeholder="Description" />
					<div class="card-actions">
						<button onclick={commitEdit}>Save</button>
						<button onclick={() => (editingId = null)}>Cancel</button>
					</div>
				{:else}
					<h3>{project.name}</h3>
					{#if project.description}
						<p class="description">{project.description}</p>
					{/if}
					<div class="metrics">
						<span>📊 {project.total_hours ?? 0}h logged</span>
						<span>📋 {project.linked_lists_count ?? 0} lists</span>
						<span>✅ {project.completed_tasks ?? 0}/{project.total_tasks ?? 0} tasks</span>
					</div>
					<div class="card-actions">
						<button class="toggle-btn" onclick={() => toggleProject(project.id)}>
							{project.is_active ? '🟢 Active' : '⚪ Inactive'}
						</button>
						<button onclick={() => startEdit(project)}>Edit</button>
						<button class="delete-btn" onclick={() => handleDelete(project.id)}>Delete</button>
					</div>
				{/if}
			</div>
		{/each}
	</div>

	{#if $projectsStore.length === 0}
		<div class="empty-state">
			<p>No projects yet. Create one to get started.</p>
		</div>
	{/if}
</section>

<style>
	.projects-page {
		display: grid;
		gap: 1rem;
	}

	h1 {
		margin: 0;
		font-family: var(--font-display);
		font-size: 1.5rem;
		font-weight: 600;
		color: var(--text-primary);
	}

	.create-form {
		display: grid;
		grid-template-columns: 1fr 1fr auto;
		gap: 0.35rem;
	}

	.create-form input {
		border: 1px solid var(--border);
		border-radius: var(--radius-sm);
		padding: 0.4rem 0.6rem;
		font-family: var(--font-body);
		font-size: 0.85rem;
		color: var(--text-primary);
		background: var(--bg-input);
	}

	.create-form input::placeholder {
		color: var(--text-tertiary);
	}

	.create-form input:focus {
		outline: none;
		border-color: var(--border-focus);
	}

	.create-form button {
		border: 1px solid var(--border);
		background: var(--bg-surface);
		border-radius: var(--radius-sm);
		padding: 0.35rem 0.75rem;
		cursor: pointer;
		font-family: var(--font-body);
		font-size: 0.82rem;
		color: var(--text-secondary);
		transition: all var(--transition);
	}

	.create-form button:hover {
		background: var(--accent);
		border-color: var(--accent);
		color: white;
	}

	.projects-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
		gap: 0.85rem;
	}

	.project-card {
		background: var(--bg-surface);
		border: 1px solid var(--border);
		border-radius: var(--radius-lg);
		padding: 0.95rem;
		display: grid;
		gap: 0.55rem;
		box-shadow: var(--shadow-sm);
		transition: box-shadow var(--transition);
	}

	.project-card:hover {
		box-shadow: var(--shadow-md);
	}

	.project-card.inactive {
		opacity: 0.55;
	}

	h3 {
		margin: 0;
		font-family: var(--font-display);
		font-size: 1.05rem;
		font-weight: 600;
		color: var(--text-primary);
	}

	.description {
		margin: 0;
		color: var(--text-secondary);
		font-size: 0.85rem;
		line-height: 1.5;
	}

	.metrics {
		display: flex;
		gap: 0.75rem;
		font-size: 0.76rem;
		color: var(--text-tertiary);
	}

	.card-actions {
		display: flex;
		gap: 0.35rem;
	}

	.card-actions button {
		border: 1px solid var(--border);
		background: var(--bg-surface);
		border-radius: var(--radius-sm);
		padding: 0.25rem 0.5rem;
		cursor: pointer;
		font-size: 0.78rem;
		font-family: var(--font-body);
		color: var(--text-secondary);
		transition: all var(--transition);
	}

	.card-actions button:hover {
		background: var(--bg-surface-hover);
		border-color: var(--accent);
		color: var(--accent);
	}

	.delete-btn {
		color: var(--error) !important;
	}

	.delete-btn:hover {
		border-color: var(--error) !important;
		background: var(--error-bg) !important;
	}

	.edit-input {
		border: 1px solid var(--border-focus);
		border-radius: var(--radius-sm);
		padding: 0.3rem 0.5rem;
		font-size: 0.88rem;
		font-family: var(--font-body);
		color: var(--text-primary);
	}

	.edit-input:focus {
		outline: none;
	}

	.empty-state {
		border: 2px dashed var(--border);
		border-radius: var(--radius-lg);
		min-height: 120px;
		display: grid;
		place-items: center;
		background: var(--bg-surface-hover);
	}

	.empty-state p {
		color: var(--text-secondary);
		font-weight: 500;
	}
</style>
