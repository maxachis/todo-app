<script lang="ts">
	import type { Task } from '$lib';
	import { api } from '$lib';
	import {
		timesheetStore,
		loadTimesheet,
		createTimeEntry,
		deleteTimeEntry
	} from '$lib/stores/timesheet';
	import { projectsStore, loadProjects } from '$lib/stores/projects';

	let weekOffset = $state(0);
	let newProjectId = $state<number | null>(null);
	let newDate = $state(today());
	let newDescription = $state('');
	let newTaskIds = $state<number[]>([]);
	let projectTasks = $state<Task[]>([]);

	function today(): string {
		const now = new Date();
		const y = now.getFullYear();
		const m = String(now.getMonth() + 1).padStart(2, '0');
		const d = String(now.getDate()).padStart(2, '0');
		return `${y}-${m}-${d}`;
	}

	function weekStartDate(offset: number): string {
		const d = new Date();
		d.setDate(d.getDate() - d.getDay() + offset * 7);
		const y = d.getFullYear();
		const m = String(d.getMonth() + 1).padStart(2, '0');
		const day = String(d.getDate()).padStart(2, '0');
		return `${y}-${m}-${day}`;
	}

	$effect(() => {
		loadTimesheet(weekStartDate(weekOffset));
		loadProjects();
	});

	$effect(() => {
		if (newProjectId !== null) {
			api.projects.getTasks(newProjectId).then((tasks) => {
				projectTasks = tasks;
			});
		} else {
			projectTasks = [];
		}
	});

	async function handleCreate(event: SubmitEvent): Promise<void> {
		event.preventDefault();
		if (newProjectId === null) return;
		await createTimeEntry({
			project_id: newProjectId,
			date: newDate,
			description: newDescription.trim(),
			task_ids: newTaskIds
		});
		newDescription = '';
		newTaskIds = [];
	}

	async function handleDelete(entryId: number): Promise<void> {
		await deleteTimeEntry(entryId, weekStartDate(weekOffset));
	}

	function formatDate(dateStr: string): string {
		return new Date(dateStr + 'T00:00:00').toLocaleDateString('en-US', {
			weekday: 'short',
			month: 'short',
			day: 'numeric'
		});
	}

	function formatTimeLocal(datetimeStr: string): string {
		return new Date(datetimeStr).toLocaleTimeString([], {
			hour: 'numeric',
			minute: '2-digit'
		});
	}
</script>

<section class="timesheet-page">
	<header>
		<h1>Timesheet</h1>
		<div class="week-nav">
			<button onclick={() => weekOffset--}>&larr; Prev</button>
			<span class="week-label">
				{#if $timesheetStore}
					{formatDate($timesheetStore.week_start)} &mdash; {formatDate($timesheetStore.week_end)}
				{/if}
			</span>
			<button onclick={() => weekOffset++}>Next &rarr;</button>
		</div>
	</header>

	{#if $timesheetStore}
		<div class="summary-bar">
			<span class="total">Total: {$timesheetStore.summary.total_hours}h</span>
			{#each $timesheetStore.summary.per_project as item}
				<span class="project-hours">{item.project_name}: {item.hours}h</span>
			{/each}
		</div>

		<form class="entry-form" onsubmit={handleCreate}>
			<select bind:value={newProjectId}>
				<option value={null}>Select project...</option>
				{#each $projectsStore as project}
					<option value={project.id}>{project.name}</option>
				{/each}
			</select>
			<input type="date" bind:value={newDate} />
			<input bind:value={newDescription} placeholder="Description..." />
			{#if projectTasks.length > 0}
				<select bind:value={newTaskIds} multiple>
					{#each projectTasks as task}
						<option value={task.id}>{task.title}</option>
					{/each}
				</select>
			{/if}
			<button type="submit">+ Entry</button>
		</form>

		<div class="entries">
			{#each Object.entries($timesheetStore.entries_by_date) as [date, entries]}
				<div class="date-group">
					<h3>{formatDate(date)}</h3>
					{#each entries as entry}
						<div class="entry-row">
							<span class="entry-project">{entry.project_name}</span>
							<span class="entry-time">{formatTimeLocal(entry.created_at)}</span>
							{#if entry.description}
								<span class="entry-desc">{entry.description}</span>
							{/if}
							<button class="delete-btn" onclick={() => handleDelete(entry.id)}>&#10005;</button>
						</div>
					{/each}
				</div>
			{/each}
		</div>
	{/if}
</section>

<style>
	.timesheet-page {
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

	header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		flex-wrap: wrap;
		gap: 0.5rem;
	}

	.week-nav {
		display: flex;
		align-items: center;
		gap: 0.5rem;
	}

	.week-nav button {
		border: 1px solid var(--border);
		background: var(--bg-surface);
		border-radius: var(--radius-sm);
		padding: 0.3rem 0.6rem;
		cursor: pointer;
		font-size: 0.78rem;
		font-family: var(--font-body);
		color: var(--text-secondary);
		transition: all var(--transition);
	}

	.week-nav button:hover {
		background: var(--bg-surface-hover);
		border-color: var(--accent);
		color: var(--accent);
	}

	.week-label {
		font-weight: 600;
		font-size: 0.88rem;
		color: var(--text-primary);
	}

	.summary-bar {
		display: flex;
		gap: 1rem;
		padding: 0.65rem 0.85rem;
		background: var(--accent-light);
		border: 1px solid var(--accent-medium);
		border-radius: var(--radius-md);
		font-size: 0.85rem;
	}

	.total {
		font-weight: 700;
		color: var(--accent);
	}

	.project-hours {
		color: var(--text-secondary);
	}

	.entry-form {
		display: flex;
		flex-wrap: wrap;
		gap: 0.35rem;
		align-items: flex-start;
	}

	.entry-form select,
	.entry-form input {
		border: 1px solid var(--border);
		border-radius: var(--radius-sm);
		padding: 0.35rem 0.5rem;
		font-size: 0.85rem;
		font-family: var(--font-body);
		color: var(--text-primary);
		background: var(--bg-input);
	}

	.entry-form select:focus,
	.entry-form input:focus {
		outline: none;
		border-color: var(--border-focus);
	}

	.entry-form select[multiple] {
		min-height: 4rem;
	}

	.entry-form button {
		border: 1px solid var(--border);
		background: var(--bg-surface);
		border-radius: var(--radius-sm);
		padding: 0.35rem 0.7rem;
		cursor: pointer;
		font-family: var(--font-body);
		font-size: 0.82rem;
		color: var(--text-secondary);
		transition: all var(--transition);
	}

	.entry-form button:hover {
		background: var(--accent);
		border-color: var(--accent);
		color: white;
	}

	.entries {
		display: grid;
		gap: 0.75rem;
	}

	.date-group h3 {
		margin: 0;
		font-family: var(--font-display);
		font-size: 0.9rem;
		font-weight: 600;
		color: var(--text-secondary);
		border-bottom: 1px solid var(--border-light);
		padding-bottom: 0.35rem;
	}

	.entry-row {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		padding: 0.35rem 0.45rem;
		border-radius: var(--radius-sm);
		transition: background var(--transition);
	}

	.entry-row:hover {
		background: var(--bg-surface-hover);
	}

	.entry-project {
		font-weight: 600;
		font-size: 0.85rem;
		color: var(--text-primary);
	}

	.entry-time {
		font-size: 0.78rem;
		color: var(--text-tertiary);
	}

	.entry-desc {
		color: var(--text-secondary);
		font-size: 0.85rem;
		flex: 1;
	}

	.delete-btn {
		background: transparent;
		border: none;
		cursor: pointer;
		color: var(--error);
		opacity: 0;
		transition: opacity var(--transition);
	}

	.entry-row:hover .delete-btn {
		opacity: 1;
	}
</style>
