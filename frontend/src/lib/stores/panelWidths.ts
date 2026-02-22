import { writable, get } from 'svelte/store';

const STORAGE_KEY = 'panel-widths';
const DEFAULT_SIDEBAR = 300;
const DEFAULT_DETAIL = 320;
const MIN_SIDEBAR = 180;
const MIN_DETAIL = 220;
const MIN_CENTER = 200;
const HANDLE_WIDTH = 6;
const TOTAL_GAP = HANDLE_WIDTH * 2;

function loadWidths(): { sidebar: number; detail: number } {
	try {
		const raw = localStorage.getItem(STORAGE_KEY);
		if (raw) {
			const parsed = JSON.parse(raw);
			if (typeof parsed.sidebar === 'number' && typeof parsed.detail === 'number') {
				return { sidebar: parsed.sidebar, detail: parsed.detail };
			}
		}
	} catch {
		// ignore parse errors
	}
	return { sidebar: DEFAULT_SIDEBAR, detail: DEFAULT_DETAIL };
}

const initial = loadWidths();
export const sidebarWidth = writable(initial.sidebar);
export const detailWidth = writable(initial.detail);

export function savePanelWidths(): void {
	const data = { sidebar: get(sidebarWidth), detail: get(detailWidth) };
	try {
		localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
	} catch {
		// ignore storage errors
	}
}

export function clampWidths(viewportWidth: number): void {
	const available = viewportWidth - TOTAL_GAP - 2 * 14; // subtract padding (0.875rem ~14px each side)
	let sw = get(sidebarWidth);
	let dw = get(detailWidth);

	sw = Math.max(MIN_SIDEBAR, Math.min(sw, available - MIN_CENTER - MIN_DETAIL));
	dw = Math.max(MIN_DETAIL, Math.min(dw, available - MIN_CENTER - sw));

	sidebarWidth.set(sw);
	detailWidth.set(dw);
}
