import { writable } from 'svelte/store';

export type CompletionSound = 'none' | 'ding' | 'pop' | 'chime' | 'celeste';

function getInitialSound(): CompletionSound {
	if (typeof localStorage === 'undefined') return 'ding';
	const saved = localStorage.getItem('completion-sound');
	if (saved === 'none' || saved === 'ding' || saved === 'pop' || saved === 'chime' || saved === 'celeste')
		return saved;
	return 'ding';
}

export const completionSoundPreference = writable<CompletionSound>(getInitialSound());

completionSoundPreference.subscribe((sound) => {
	if (typeof localStorage === 'undefined') return;
	localStorage.setItem('completion-sound', sound);
});
