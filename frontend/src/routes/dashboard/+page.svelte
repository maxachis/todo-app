<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import * as d3 from 'd3';
	import { api, type UpcomingTask, type TrendsData, type FollowUpDueItem } from '$lib';
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

	const activeTab = $derived($page.url.searchParams.get('tab') ?? 'upcoming');

	let followUpsDue: FollowUpDueItem[] = $state([]);
	let trendsData: TrendsData | null = $state(null);
	let trendsLoaded = $state(false);

	let interactionsChartEl: HTMLDivElement | null = $state(null);
	let tasksChartEl: HTMLDivElement | null = $state(null);
	let themeObserver: MutationObserver | null = null;

	$effect(() => {
		loadUpcoming();
		loadFollowUps();
	});

	$effect(() => {
		if (activeTab === 'trends' && !trendsLoaded) {
			loadTrends();
		}
	});

	$effect(() => {
		if (activeTab === 'trends' && trendsData && interactionsChartEl && tasksChartEl) {
			renderCharts();
		}
	});

	async function loadFollowUps() {
		try {
			followUpsDue = await api.dashboard.followUpsDue();
		} catch {
			followUpsDue = [];
		}
	}

	async function loadTrends() {
		try {
			trendsData = await api.dashboard.trends();
			trendsLoaded = true;
		} catch {
			trendsData = null;
		}
	}

	function setTab(tab: string) {
		const url = new URL($page.url);
		if (tab === 'upcoming') {
			url.searchParams.delete('tab');
		} else {
			url.searchParams.set('tab', tab);
		}
		goto(url.toString(), { replaceState: false, noScroll: true });
	}

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

	function formatWeekLabel(isoDate: string): string {
		const d = parseLocalDate(isoDate);
		return d.toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
	}

	function getThemeColors() {
		const style = getComputedStyle(document.documentElement);
		return {
			accent: style.getPropertyValue('--accent').trim(),
			textPrimary: style.getPropertyValue('--text-primary').trim(),
			textSecondary: style.getPropertyValue('--text-secondary').trim(),
			textTertiary: style.getPropertyValue('--text-tertiary').trim(),
			border: style.getPropertyValue('--border').trim(),
			bgSurface: style.getPropertyValue('--bg-surface').trim(),
			success: style.getPropertyValue('--success').trim()
		};
	}

	function renderBarChart(
		container: HTMLDivElement,
		data: { week_start: string; count: number }[],
		title: string,
		barColor: string
	) {
		container.innerHTML = '';
		const colors = getThemeColors();

		const margin = { top: 32, right: 16, bottom: 40, left: 40 };
		const width = container.clientWidth;
		const height = 220;
		const innerWidth = width - margin.left - margin.right;
		const innerHeight = height - margin.top - margin.bottom;

		const svg = d3
			.select(container)
			.append('svg')
			.attr('width', width)
			.attr('height', height);

		// Title
		svg
			.append('text')
			.attr('x', margin.left)
			.attr('y', 20)
			.attr('font-size', 14)
			.attr('font-weight', 600)
			.attr('font-family', 'var(--font-display)')
			.attr('fill', colors.textPrimary)
			.text(title);

		const g = svg.append('g').attr('transform', `translate(${margin.left},${margin.top})`);

		const x = d3
			.scaleBand()
			.domain(data.map((d) => d.week_start))
			.range([0, innerWidth])
			.padding(0.25);

		const maxCount = d3.max(data, (d) => d.count) ?? 1;
		const y = d3.scaleLinear().domain([0, maxCount]).nice().range([innerHeight, 0]);

		// X axis
		g.append('g')
			.attr('transform', `translate(0,${innerHeight})`)
			.call(
				d3
					.axisBottom(x)
					.tickFormat((d) => formatWeekLabel(d))
					.tickSize(0)
			)
			.call((g) => g.select('.domain').attr('stroke', colors.border))
			.selectAll('text')
			.attr('font-size', 9)
			.attr('fill', colors.textTertiary)
			.attr('transform', 'rotate(-35)')
			.attr('text-anchor', 'end')
			.attr('dx', '-0.3em')
			.attr('dy', '0.5em');

		// Y axis
		g.append('g')
			.call(d3.axisLeft(y).ticks(4).tickSize(-innerWidth))
			.call((g) => g.select('.domain').remove())
			.call((g) => g.selectAll('.tick line').attr('stroke', colors.border).attr('stroke-dasharray', '2,2'))
			.selectAll('text')
			.attr('font-size', 10)
			.attr('fill', colors.textTertiary);

		// Bars
		g.selectAll('rect')
			.data(data)
			.join('rect')
			.attr('x', (d) => x(d.week_start) ?? 0)
			.attr('y', (d) => y(d.count))
			.attr('width', x.bandwidth())
			.attr('height', (d) => innerHeight - y(d.count))
			.attr('fill', barColor)
			.attr('rx', 3);
	}

	function renderCharts() {
		if (!trendsData || !interactionsChartEl || !tasksChartEl) return;
		const colors = getThemeColors();
		renderBarChart(interactionsChartEl, trendsData.interactions_per_week, 'Interactions per Week', colors.accent);
		renderBarChart(tasksChartEl, trendsData.tasks_completed_per_week, 'Tasks Completed per Week', colors.success);
	}

	onMount(() => {
		themeObserver = new MutationObserver((mutations) => {
			for (const m of mutations) {
				if (m.attributeName === 'data-theme') {
					if (activeTab === 'trends' && trendsData) {
						renderCharts();
					}
					break;
				}
			}
		});
		themeObserver.observe(document.documentElement, { attributes: true });
	});

	onDestroy(() => {
		themeObserver?.disconnect();
	});
</script>

<section class="dashboard-page">
	<header>
		<h1>Dashboard</h1>
		<nav class="tab-bar">
			<button class="tab" class:active={activeTab === 'upcoming'} onclick={() => setTab('upcoming')}>Upcoming</button>
			<button class="tab" class:active={activeTab === 'trends'} onclick={() => setTab('trends')}>Trends</button>
		</nav>
	</header>

	{#if activeTab === 'upcoming'}
		{#if followUpsDue.length > 0}
			<div class="follow-ups-group">
				<h2>Follow-ups Due<span class="group-count follow-up-count">{followUpsDue.length}</span></h2>
				<div class="task-list">
					{#each followUpsDue as fu (fu.person_id)}
						<a href="/crm/people?person={fu.person_id}" class="follow-up-row">
							<div class="follow-up-main">
								<span class="follow-up-icon">&#128100;</span>
								<span class="follow-up-name">{fu.first_name} {fu.last_name}</span>
							</div>
							<div class="follow-up-meta">
								<span class="follow-up-overdue">{fu.days_overdue}d overdue</span>
								<span class="follow-up-cadence">
									{#if fu.last_interaction_date}
										{Math.round((Date.now() - new Date(fu.last_interaction_date + 'T00:00:00').getTime()) / 86400000)}d / {fu.follow_up_cadence_days}d cadence
									{:else}
										never / {fu.follow_up_cadence_days}d cadence
									{/if}
								</span>
							</div>
						</a>
					{/each}
				</div>
			</div>
		{/if}

		{#if grouped.length === 0 && followUpsDue.length === 0}
			<div class="empty-state">
				<p>No tasks with due dates and no follow-ups due.</p>
			</div>
		{:else if grouped.length === 0}
			<!-- Follow-ups shown above, no tasks -->
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

	{:else if activeTab === 'trends'}
		{#if trendsData}
			<div class="trends-grid">
				<div class="chart-card">
					<div bind:this={interactionsChartEl} class="chart-container"></div>
				</div>
				<div class="chart-card">
					<div bind:this={tasksChartEl} class="chart-container"></div>
				</div>
				<div class="chart-card compliance-card">
					<h2>Follow-up Compliance</h2>
					{#if trendsData.follow_up_compliance.total === 0}
						<p class="compliance-empty">No follow-up cadences configured</p>
					{:else}
						<div class="compliance-stat">
							<span class="compliance-number">{trendsData.follow_up_compliance.on_track}</span>
							<span class="compliance-label">of {trendsData.follow_up_compliance.total} contacts on track</span>
						</div>
						<div class="compliance-bar">
							<div
								class="compliance-fill"
								style="width: {(trendsData.follow_up_compliance.on_track / trendsData.follow_up_compliance.total) * 100}%"
							></div>
						</div>
						{#if trendsData.follow_up_compliance.overdue_count > 0}
							<p class="compliance-overdue">{trendsData.follow_up_compliance.overdue_count} overdue</p>
						{/if}
					{/if}
				</div>
			</div>
		{:else}
			<div class="empty-state">
				<p>Loading trends...</p>
			</div>
		{/if}
	{/if}
</section>

<style>
	.dashboard-page {
		display: grid;
		gap: 1.25rem;
	}

	header {
		display: flex;
		align-items: center;
		gap: 1.5rem;
		flex-wrap: wrap;
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

	.tab-bar {
		display: flex;
		gap: 0.25rem;
		background: var(--bg-surface-hover);
		border-radius: var(--radius-md);
		padding: 0.2rem;
	}

	.tab {
		border: none;
		background: transparent;
		font-family: var(--font-body);
		font-size: 0.85rem;
		font-weight: 500;
		color: var(--text-secondary);
		padding: 0.35rem 0.75rem;
		border-radius: var(--radius-sm);
		cursor: pointer;
		transition: all var(--transition);
	}

	.tab:hover {
		color: var(--text-primary);
	}

	.tab.active {
		background: var(--bg-surface);
		color: var(--text-primary);
		font-weight: 600;
		box-shadow: var(--shadow-sm);
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

	/* Follow-ups Due */

	.follow-ups-group {
		display: grid;
		gap: 0.5rem;
	}

	.follow-ups-group h2 {
		color: var(--accent);
	}

	.follow-up-count {
		background: var(--accent-light);
		color: var(--accent);
	}

	.follow-up-row {
		display: grid;
		grid-template-columns: 1fr auto;
		align-items: center;
		gap: 0.75rem;
		padding: 0.6rem 0.75rem;
		background: var(--accent-light);
		border: 1px solid var(--accent-medium);
		border-radius: var(--radius-md);
		text-decoration: none;
		color: inherit;
		transition: all var(--transition);
	}

	.follow-up-row:hover {
		border-color: var(--accent);
		box-shadow: var(--shadow-sm);
	}

	.follow-up-main {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		min-width: 0;
	}

	.follow-up-icon {
		font-size: 0.9rem;
		flex-shrink: 0;
	}

	.follow-up-name {
		font-size: 0.9rem;
		font-weight: 500;
		color: var(--text-primary);
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}

	.follow-up-meta {
		display: flex;
		flex-direction: column;
		align-items: flex-end;
		gap: 0.15rem;
		flex-shrink: 0;
	}

	.follow-up-overdue {
		font-size: 0.78rem;
		font-weight: 600;
		color: var(--error);
	}

	.follow-up-cadence {
		font-size: 0.72rem;
		color: var(--text-tertiary);
	}

	/* Task groups */

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

	/* Trends */

	.trends-grid {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 1rem;
	}

	.chart-card {
		background: var(--bg-surface);
		border: 1px solid var(--border);
		border-radius: var(--radius-lg);
		padding: 0.75rem;
		box-shadow: var(--shadow-sm);
	}

	.chart-container {
		width: 100%;
		min-height: 220px;
	}

	.compliance-card {
		grid-column: 1 / -1;
		padding: 1rem;
	}

	.compliance-card h2 {
		margin-bottom: 0.75rem;
	}

	.compliance-stat {
		display: flex;
		align-items: baseline;
		gap: 0.5rem;
		margin-bottom: 0.5rem;
	}

	.compliance-number {
		font-family: var(--font-display);
		font-size: 2rem;
		font-weight: 700;
		color: var(--success);
	}

	.compliance-label {
		font-size: 0.9rem;
		color: var(--text-secondary);
	}

	.compliance-bar {
		height: 8px;
		background: var(--bg-surface-hover);
		border-radius: 4px;
		overflow: hidden;
	}

	.compliance-fill {
		height: 100%;
		background: var(--success);
		border-radius: 4px;
		transition: width 0.3s ease;
	}

	.compliance-overdue {
		margin: 0.5rem 0 0;
		font-size: 0.8rem;
		color: var(--error);
		font-weight: 500;
	}

	.compliance-empty {
		color: var(--text-tertiary);
		font-size: 0.9rem;
	}

	/* Empty state */

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

	@media (max-width: 768px) {
		.trends-grid {
			grid-template-columns: 1fr;
		}
	}

	@media (max-width: 640px) {
		.task-location {
			overflow: hidden;
			text-overflow: ellipsis;
			white-space: nowrap;
			max-width: 160px;
		}

		.task-row,
		.follow-up-row {
			grid-template-columns: 1fr;
			gap: 0.25rem;
		}

		.task-meta,
		.follow-up-meta {
			flex-direction: row;
			align-items: center;
			flex-wrap: wrap;
			gap: 0.35rem;
		}
	}
</style>
