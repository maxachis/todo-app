<script lang="ts">
	import type { Task, UpdateTaskInput } from '$lib';

	interface Props {
		task: Task;
		onSave: (payload: UpdateTaskInput) => Promise<void>;
	}

	let { task, onSave }: Props = $props();

	let recurrenceType = $state('none');
	let weeklyDays = $state<number[]>([]);
	let monthDay = $state(1);
	let yearlyMonth = $state(1);
	let yearlyDay = $state(1);
	let customDates = $state<string[]>([]);
	let newCustomDate = $state('');

	const dayLabels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
	const monthLabels = [
		'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
		'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
	];

	$effect(() => {
		recurrenceType = task.recurrence_type || 'none';
		const rule = task.recurrence_rule || {};
		weeklyDays = (rule.days as number[]) || [];
		monthDay = (rule.day_of_month as number) || 1;
		yearlyMonth = (rule.month as number) || 1;
		yearlyDay = (rule.day as number) || 1;
		customDates = (rule.dates as string[]) || [];
	});

	function buildRule(): Record<string, unknown> {
		switch (recurrenceType) {
			case 'weekly':
				return { days: weeklyDays };
			case 'monthly':
				return { day_of_month: monthDay };
			case 'yearly':
				return { month: yearlyMonth, day: yearlyDay };
			case 'custom_dates':
				return { dates: customDates };
			default:
				return {};
		}
	}

	async function save(): Promise<void> {
		await onSave({
			recurrence_type: recurrenceType,
			recurrence_rule: buildRule()
		});
	}

	async function handleTypeChange(): Promise<void> {
		if (recurrenceType === 'none') {
			await onSave({ recurrence_type: 'none', recurrence_rule: {} });
		}
	}

	function toggleDay(day: number): void {
		if (weeklyDays.includes(day)) {
			weeklyDays = weeklyDays.filter((d) => d !== day);
		} else {
			weeklyDays = [...weeklyDays, day].sort();
		}
	}

	function addCustomDate(): void {
		const trimmed = newCustomDate.trim();
		if (trimmed && /^\d{2}-\d{2}$/.test(trimmed) && !customDates.includes(trimmed)) {
			customDates = [...customDates, trimmed].sort();
			newCustomDate = '';
		}
	}

	function removeCustomDate(d: string): void {
		customDates = customDates.filter((x) => x !== d);
	}
</script>

<div class="recurrence-editor">
	<label for="recurrence-type">Repeat</label>
	<select
		id="recurrence-type"
		bind:value={recurrenceType}
		onchange={handleTypeChange}
		onblur={save}
	>
		<option value="none">None</option>
		<option value="daily">Daily</option>
		<option value="weekly">Weekly</option>
		<option value="monthly">Monthly</option>
		<option value="yearly">Yearly</option>
		<option value="custom_dates">Custom Dates</option>
	</select>

	{#if recurrenceType === 'weekly'}
		<div class="day-picker">
			{#each dayLabels as label, i}
				<button
					class="day-toggle"
					class:active={weeklyDays.includes(i)}
					onclick={() => toggleDay(i)}
					onblur={save}
					type="button"
				>
					{label}
				</button>
			{/each}
		</div>
	{/if}

	{#if recurrenceType === 'monthly'}
		<div class="month-day-input">
			<label for="month-day">Day of month</label>
			<input
				id="month-day"
				type="number"
				min="1"
				max="31"
				bind:value={monthDay}
				onblur={save}
			/>
		</div>
	{/if}

	{#if recurrenceType === 'yearly'}
		<div class="yearly-inputs">
			<div class="yearly-field">
				<label for="yearly-month">Month</label>
				<select id="yearly-month" bind:value={yearlyMonth} onblur={save}>
					{#each monthLabels as label, i}
						<option value={i + 1}>{label}</option>
					{/each}
				</select>
			</div>
			<div class="yearly-field">
				<label for="yearly-day">Day</label>
				<input
					id="yearly-day"
					type="number"
					min="1"
					max="31"
					bind:value={yearlyDay}
					onblur={save}
				/>
			</div>
		</div>
	{/if}

	{#if recurrenceType === 'custom_dates'}
		<div class="custom-dates">
			<div class="date-list">
				{#each customDates as d}
					<span class="date-chip">
						{d}
						<button type="button" onclick={() => { removeCustomDate(d); save(); }}>✕</button>
					</span>
				{/each}
			</div>
			<div class="date-add">
				<input
					placeholder="MM-DD"
					bind:value={newCustomDate}
					onkeydown={(e) => { if (e.key === 'Enter') { e.preventDefault(); addCustomDate(); save(); } }}
					maxlength="5"
				/>
				<button type="button" onclick={() => { addCustomDate(); save(); }}>+</button>
			</div>
		</div>
	{/if}
</div>

<style>
	.recurrence-editor {
		display: grid;
		gap: 0.3rem;
	}

	label {
		font-size: 0.7rem;
		font-weight: 600;
		color: var(--text-tertiary);
		text-transform: uppercase;
		letter-spacing: 0.06em;
	}

	select,
	input {
		border: 1px solid var(--border);
		border-radius: var(--radius-sm);
		padding: 0.4rem 0.55rem;
		font-size: 0.88rem;
		font-family: var(--font-body);
		color: var(--text-primary);
		background: var(--bg-input);
		transition: border-color var(--transition);
	}

	select:focus,
	input:focus {
		outline: none;
		border-color: var(--border-focus);
	}

	.day-picker {
		display: flex;
		gap: 0.25rem;
		flex-wrap: wrap;
	}

	.day-toggle {
		border: 1px solid var(--border);
		background: var(--bg-surface);
		border-radius: var(--radius-sm);
		padding: 0.25rem 0.45rem;
		font-size: 0.78rem;
		font-family: var(--font-body);
		cursor: pointer;
		color: var(--text-secondary);
		transition: all var(--transition);
	}

	.day-toggle.active {
		background: var(--accent);
		border-color: var(--accent);
		color: white;
	}

	.month-day-input,
	.yearly-inputs {
		display: flex;
		gap: 0.5rem;
		align-items: end;
	}

	.yearly-field {
		display: grid;
		gap: 0.2rem;
	}

	.yearly-inputs input {
		width: 4rem;
	}

	.custom-dates {
		display: grid;
		gap: 0.35rem;
	}

	.date-list {
		display: flex;
		flex-wrap: wrap;
		gap: 0.25rem;
	}

	.date-chip {
		background: var(--tag-bg);
		color: var(--tag-text);
		padding: 0.18rem 0.45rem;
		border-radius: var(--radius-sm);
		font-size: 0.78rem;
		font-weight: 500;
		display: inline-flex;
		align-items: center;
		gap: 0.25rem;
	}

	.date-chip button {
		background: transparent;
		border: none;
		cursor: pointer;
		color: var(--text-tertiary);
		font-size: 0.7rem;
		padding: 0;
	}

	.date-chip button:hover {
		color: var(--error);
	}

	.date-add {
		display: grid;
		grid-template-columns: 1fr auto;
		gap: 0.25rem;
	}

	.date-add button {
		border: 1px solid var(--border);
		background: var(--bg-surface);
		border-radius: var(--radius-sm);
		padding: 0.3rem 0.55rem;
		cursor: pointer;
		font-family: var(--font-body);
		font-size: 0.85rem;
		color: var(--text-secondary);
		transition: all var(--transition);
	}

	.date-add button:hover {
		background: var(--accent);
		border-color: var(--accent);
		color: white;
	}
</style>
