import type { CompletionSound } from '$lib/stores/completionSound';

let audioCtx: AudioContext | null = null;

function getContext(): AudioContext {
	if (!audioCtx) {
		audioCtx = new AudioContext();
	}
	if (audioCtx.state === 'suspended') {
		audioCtx.resume();
	}
	return audioCtx;
}

function ding(ctx: AudioContext): void {
	const osc = ctx.createOscillator();
	const gain = ctx.createGain();
	osc.type = 'sine';
	osc.frequency.setValueAtTime(800, ctx.currentTime);
	osc.frequency.exponentialRampToValueAtTime(600, ctx.currentTime + 0.15);
	gain.gain.setValueAtTime(0.3, ctx.currentTime);
	gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.4);
	osc.connect(gain);
	gain.connect(ctx.destination);
	osc.start(ctx.currentTime);
	osc.stop(ctx.currentTime + 0.4);
}

function pop(ctx: AudioContext): void {
	const osc = ctx.createOscillator();
	const gain = ctx.createGain();
	osc.type = 'sine';
	osc.frequency.setValueAtTime(400, ctx.currentTime);
	osc.frequency.exponentialRampToValueAtTime(200, ctx.currentTime + 0.08);
	gain.gain.setValueAtTime(0.35, ctx.currentTime);
	gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.15);
	osc.connect(gain);
	gain.connect(ctx.destination);
	osc.start(ctx.currentTime);
	osc.stop(ctx.currentTime + 0.15);
}

function chime(ctx: AudioContext): void {
	const now = ctx.currentTime;

	// First tone: C5 (523 Hz)
	const osc1 = ctx.createOscillator();
	const gain1 = ctx.createGain();
	osc1.type = 'sine';
	osc1.frequency.setValueAtTime(523, now);
	gain1.gain.setValueAtTime(0.25, now);
	gain1.gain.exponentialRampToValueAtTime(0.001, now + 0.3);
	osc1.connect(gain1);
	gain1.connect(ctx.destination);
	osc1.start(now);
	osc1.stop(now + 0.3);

	// Second tone: E5 (659 Hz), slightly delayed
	const osc2 = ctx.createOscillator();
	const gain2 = ctx.createGain();
	osc2.type = 'sine';
	osc2.frequency.setValueAtTime(659, now + 0.1);
	gain2.gain.setValueAtTime(0.001, now);
	gain2.gain.linearRampToValueAtTime(0.25, now + 0.1);
	gain2.gain.exponentialRampToValueAtTime(0.001, now + 0.45);
	osc2.connect(gain2);
	gain2.connect(ctx.destination);
	osc2.start(now);
	osc2.stop(now + 0.45);
}

function celeste(ctx: AudioContext): void {
	const now = ctx.currentTime;

	// Fundamental: A5 (880 Hz)
	const osc1 = ctx.createOscillator();
	const gain1 = ctx.createGain();
	osc1.type = 'sine';
	osc1.frequency.setValueAtTime(880, now);
	gain1.gain.setValueAtTime(0.2, now);
	gain1.gain.exponentialRampToValueAtTime(0.001, now + 0.5);
	osc1.connect(gain1);
	gain1.connect(ctx.destination);
	osc1.start(now);
	osc1.stop(now + 0.5);

	// Soft overtone: E6 (1319 Hz)
	const osc2 = ctx.createOscillator();
	const gain2 = ctx.createGain();
	osc2.type = 'sine';
	osc2.frequency.setValueAtTime(1319, now);
	gain2.gain.setValueAtTime(0.08, now);
	gain2.gain.exponentialRampToValueAtTime(0.001, now + 0.45);
	osc2.connect(gain2);
	gain2.connect(ctx.destination);
	osc2.start(now);
	osc2.stop(now + 0.45);
}

const soundFns: Record<Exclude<CompletionSound, 'none'>, (ctx: AudioContext) => void> = {
	ding,
	pop,
	chime,
	celeste
};

export function playCompletionSound(sound: CompletionSound): void {
	if (sound === 'none') return;
	const fn = soundFns[sound];
	if (fn) {
		fn(getContext());
	}
}
