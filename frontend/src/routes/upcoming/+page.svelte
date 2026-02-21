<script lang="ts">
	import type { UpcomingTask } from '$lib';
	import { upcomingStore, loadUpcoming } from '$lib/stores/upcoming';

	const PRIORITY_LABELS: Record<number, string> = {
		1: 'Low',
		3: 'Med',
		5: 'High'
	};

	const PRIORITY_CLASSES: Record<number, string> = {
		1: 'priority-low',
		3: 'priority-med',
		5: 'priority-high'
	};

	type GroupKey = 'overdue' | 'today' | 'tomorrow' | 'thisWeek' | 'later';

	interface TaskGroup {
		key: GroupKey;
		label: string;
		tasks: UpcomingTask[];
	}

	$effect(() => {
		loadUpcoming();
	});

	const grouped = $derived(groupTasks($upcomingStore));

	function groupTasks(tasks: UpcomingTask[]): TaskGroup[] {
		const now = new Date();
		const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
		const tomorrow = new Date(today);
		tomorrow.setDate(tomorrow.getDate() + 1);
		const dayAfterTomorrow = new Date(today);
		dayAfterTomorrow.setDate(dayAfterTomorrow.getDate() + 2);
		const endOfWeek = new Date(today);
		endOfWeek.setDate(endOfWeek.getDate() + (7 - endOfWeek.getDay()));

		const buckets: Record<GroupKey, UpcomingTask[]> = {
			overdue: [],
			today: [],
			tomorrow: [],
			thisWeek: [],
			later: []
		};

		for (const task of tasks) {
			const d = parseLocalDate(task.due_date);
			if (d < today) {
				buckets.overdue.push(task);
			} else if (d < tomorrow) {
				buckets.today.push(task);
			} else if (d < dayAfterTomorrow) {
				buckets.tomorrow.push(task);
			} else if (d < endOfWeek) {
				buckets.thisWeek.push(task);
			} else {
				buckets.later.push(task);
			}
		}

		const labels: Record<GroupKey, string> = {
			overdue: 'Overdue',
			today: 'Today',
			tomorrow: 'Tomorrow',
			thisWeek: 'This Week',
			later: 'Later'
		};

		const order: GroupKey[] = ['overdue', 'today', 'tomorrow', 'thisWeek', 'later'];
		return order
			.filter((key) => buckets[key].length > 0)
			.map((key) => ({ key, label: labels[key], tasks: buckets[key] }));
	}

	function parseLocalDate(dateStr: string): Date {
		const [y, m, d] = dateStr.split('-').map(Number);
		return new Date(y, m - 1, d);
	}

	function formatDate(dateStr: string): string {
		const d = parseLocalDate(dateStr);
		return d.toLocaleDateString(undefined, { weekday: 'short', month: 'short', day: 'numeric' });
	}

	function formatTime(timeStr: string): string {
		const [h, m] = timeStr.split(':').map(Number);
		const d = new Date();
		d.setHours(h, m);
		return d.toLocaleTimeString(undefined, { hour: 'numeric', minute: '2-digit' });
	}
</script>

<section class="upcoming-page">
	<header>
		<h1>Upcoming</h1>
	</header>

	{#if grouped.length === 0}
		<div class="empty-state">
			<p>No tasks with due dates. Set a due date on a task to see it here.</p>
		</div>
	{:else}
		{#each grouped as group (group.key)}
			<div class="task-group" class:overdue={group.key === 'overdue'}>
				<h2>{group.label}<span class="group-count">{group.tasks.length}</span></h2>
				<div class="task-list">
					{#each group.tasks as task (task.id)}
						<a href="/?list={task.list_id}&task={task.id}" class="task-row">
							<div class="task-main">
								<span class="task-title">{task.title}</span>
								{#if task.priority > 0}
									<span class="priority-badge {PRIORITY_CLASSES[task.priority] ?? ''}">{PRIORITY_LABELS[task.priority] ?? ''}</span>
								{/if}
							</div>
							<div class="task-meta">
								<span class="task-date">
									{formatDate(task.due_date)}{#if task.due_time} at {formatTime(task.due_time)}{/if}
								</span>
								<span class="task-location">{task.list_emoji ? task.list_emoji + ' ' : ''}{task.list_name} / {task.section_name}</span>
							</div>
						</a>
					{/each}
				</div>
			</div>
		{/each}
	{/if}
</section>

<style>
	.upcoming-page {
		display: grid;
		gap: 1.25rem;
	}

	h1 {
		margin: 0;
		font-family: var(--font-display);
		font-size: 1.5rem;
		font-weight: 600;
		color: var(--text-primary);
	}

	h2 {
		margin: 0;
		font-family: var(--font-display);
		font-size: 1.1rem;
		font-weight: 600;
		color: var(--text-primary);
		display: flex;
		align-items: center;
		gap: 0.5rem;
	}

	.group-count {
		font-family: var(--font-body);
		font-size: 0.72rem;
		font-weight: 500;
		color: var(--text-tertiary);
		background: var(--bg-surface-hover);
		border-radius: var(--radius-sm);
		padding: 0.1rem 0.4rem;
	}

	.task-group {
		display: grid;
		gap: 0.5rem;
	}

	.task-group.overdue h2 {
		color: var(--error);
	}

	.task-group.overdue .group-count {
		background: var(--error-bg);
		color: var(--error);
	}

	.task-list {
		display: grid;
		gap: 0.25rem;
	}

	.task-row {
		display: grid;
		grid-template-columns: 1fr auto;
		align-items: center;
		gap: 0.75rem;
		padding: 0.6rem 0.75rem;
		background: var(--bg-surface);
		border: 1px solid var(--border);
		border-radius: var(--radius-md);
		text-decoration: none;
		color: inherit;
		transition: all var(--transition);
	}

	.task-row:hover {
		border-color: var(--accent);
		box-shadow: var(--shadow-sm);
	}

	.task-main {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		min-width: 0;
	}

	.task-title {
		font-size: 0.9rem;
		font-weight: 500;
		color: var(--text-primary);
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}

	.priority-badge {
		flex-shrink: 0;
		font-size: 0.68rem;
		font-weight: 600;
		padding: 0.1rem 0.35rem;
		border-radius: var(--radius-sm);
		text-transform: uppercase;
		letter-spacing: 0.03em;
	}

	.priority-low {
		background: var(--success-bg);
		color: var(--success);
		border: 1px solid var(--success-border);
	}

	.priority-med {
		background: var(--pinned-bg);
		color: var(--pinned-text);
		border: 1px solid var(--pinned-border);
	}

	.priority-high {
		background: var(--error-bg);
		color: var(--error);
		border: 1px solid var(--error-border);
	}

	.task-meta {
		display: flex;
		flex-direction: column;
		align-items: flex-end;
		gap: 0.15rem;
		flex-shrink: 0;
	}

	.task-date {
		font-size: 0.78rem;
		color: var(--text-secondary);
	}

	.overdue .task-date {
		color: var(--error);
		font-weight: 500;
	}

	.task-location {
		font-size: 0.72rem;
		color: var(--text-tertiary);
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
