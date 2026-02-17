import { writable } from 'svelte/store';

import { api, type CreateTimeEntryInput, type TimeEntry, type TimesheetResponse } from '$lib';

export const timesheetStore = writable<TimesheetResponse | null>(null);

export async function loadTimesheet(week?: string): Promise<TimesheetResponse> {
  const payload = await api.timesheet.get(week);
  timesheetStore.set(payload);
  return payload;
}

export async function createTimeEntry(payload: CreateTimeEntryInput): Promise<TimeEntry> {
  const entry = await api.timesheet.create(payload);
  await loadTimesheet(payload.date);
  return entry;
}

export async function deleteTimeEntry(entryId: number, week?: string): Promise<void> {
  await api.timesheet.remove(entryId);
  await loadTimesheet(week);
}
