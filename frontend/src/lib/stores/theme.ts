import { writable } from 'svelte/store';

export type ThemePreference = 'light' | 'dark' | 'system';

function getInitialPreference(): ThemePreference {
	if (typeof localStorage === 'undefined') return 'system';
	const saved = localStorage.getItem('theme');
	if (saved === 'light' || saved === 'dark' || saved === 'system') return saved;
	return 'system';
}

function resolveTheme(preference: ThemePreference): 'light' | 'dark' {
	if (preference === 'system') {
		return matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
	}
	return preference;
}

function applyTheme(preference: ThemePreference) {
	const resolved = resolveTheme(preference);
	document.documentElement.dataset.theme = resolved;
	localStorage.setItem('theme', preference);
}

export const themePreference = writable<ThemePreference>(getInitialPreference());

let mediaQuery: MediaQueryList | null = null;
let mediaHandler: ((e: MediaQueryListEvent) => void) | null = null;

themePreference.subscribe((preference) => {
	if (typeof document === 'undefined') return;

	applyTheme(preference);

	// Clean up previous listener
	if (mediaQuery && mediaHandler) {
		mediaQuery.removeEventListener('change', mediaHandler);
		mediaHandler = null;
	}

	// Listen for OS changes when set to 'system'
	if (preference === 'system') {
		mediaQuery = matchMedia('(prefers-color-scheme: dark)');
		mediaHandler = () => applyTheme('system');
		mediaQuery.addEventListener('change', mediaHandler);
	}
});

export function cycleTheme() {
	themePreference.update((current) => {
		const cycle: ThemePreference[] = ['light', 'system', 'dark'];
		const idx = cycle.indexOf(current);
		return cycle[(idx + 1) % cycle.length];
	});
}
