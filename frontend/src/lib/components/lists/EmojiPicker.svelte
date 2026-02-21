<script lang="ts">
	type EmojiEntry = {
		emoji: string;
		name: string;
		keywords: string[];
	};

	type EmojiCategory = {
		category: string;
		values: EmojiEntry[];
	};

	const EMOJIS: EmojiCategory[] = [
		{
			category: 'Productivity',
			values: [
				{ emoji: '\u{1F4DD}', name: 'memo', keywords: ['write', 'notes', 'draft'] },
				{ emoji: '\u{2705}', name: 'check mark', keywords: ['done', 'complete', 'success'] },
				{ emoji: '\u{1F4C5}', name: 'calendar', keywords: ['schedule', 'date', 'plan'] },
				{ emoji: '\u{23F0}', name: 'alarm clock', keywords: ['reminder', 'time', 'deadline'] },
				{ emoji: '\u{1F4CC}', name: 'pushpin', keywords: ['pin', 'important', 'mark'] },
				{ emoji: '\u{1F4CE}', name: 'paperclip', keywords: ['attach', 'file', 'document'] },
				{ emoji: '\u{1F4C8}', name: 'chart increasing', keywords: ['growth', 'metrics', 'analytics'] },
				{ emoji: '\u{1F4CA}', name: 'bar chart', keywords: ['report', 'stats', 'dashboard'] },
				{ emoji: '\u{1F4E2}', name: 'loudspeaker', keywords: ['announce', 'broadcast', 'notice'] },
				{ emoji: '\u{1F4A1}', name: 'light bulb', keywords: ['idea', 'brainstorm', 'inspiration'] },
				{ emoji: '\u{1F4E6}', name: 'package', keywords: ['ship', 'deliver', 'release'] },
				{ emoji: '\u{1F680}', name: 'rocket', keywords: ['launch', 'ship', 'boost'] }
			]
		},
		{
			category: 'Work',
			values: [
				{ emoji: '\u{1F4BC}', name: 'briefcase', keywords: ['office', 'job', 'career'] },
				{ emoji: '\u{1F5C2}', name: 'card index dividers', keywords: ['organize', 'archive', 'sort'] },
				{ emoji: '\u{1F4C1}', name: 'file folder', keywords: ['files', 'documents', 'storage'] },
				{ emoji: '\u{1F4CB}', name: 'clipboard', keywords: ['checklist', 'tasks', 'notes'] },
				{ emoji: '\u{1F4BB}', name: 'laptop', keywords: ['coding', 'computer', 'development'] },
				{ emoji: '\u{1F5A5}', name: 'desktop computer', keywords: ['workstation', 'pc', 'screen'] },
				{ emoji: '\u{1F4DE}', name: 'telephone receiver', keywords: ['call', 'meeting', 'client'] },
				{ emoji: '\u{1F465}', name: 'busts in silhouette', keywords: ['team', 'collaboration', 'people'] },
				{ emoji: '\u{1F91D}', name: 'handshake', keywords: ['deal', 'agreement', 'partnership'] },
				{ emoji: '\u{1F3E2}', name: 'office building', keywords: ['company', 'business', 'hq'] },
				{ emoji: '\u{1F4B0}', name: 'money bag', keywords: ['budget', 'finance', 'revenue'] },
				{ emoji: '\u{1F3AF}', name: 'bullseye', keywords: ['goal', 'target', 'objective'] }
			]
		},
		{
			category: 'Home',
			values: [
				{ emoji: '\u{1F3E0}', name: 'house', keywords: ['home', 'family', 'chores'] },
				{ emoji: '\u{1F9F9}', name: 'broom', keywords: ['clean', 'sweep', 'organize'] },
				{ emoji: '\u{1F9FA}', name: 'basket', keywords: ['laundry', 'storage', 'household'] },
				{ emoji: '\u{1F9FC}', name: 'soap', keywords: ['wash', 'cleaning', 'sanitize'] },
				{ emoji: '\u{1F6BF}', name: 'shower', keywords: ['bath', 'hygiene', 'morning'] },
				{ emoji: '\u{1F373}', name: 'cooking', keywords: ['meal', 'kitchen', 'prep'] },
				{ emoji: '\u{1F6D2}', name: 'shopping cart', keywords: ['groceries', 'buy', 'store'] },
				{ emoji: '\u{1F6CB}', name: 'couch and lamp', keywords: ['living room', 'furniture', 'rest'] },
				{ emoji: '\u{1F6AA}', name: 'door', keywords: ['entry', 'repair', 'house'] },
				{ emoji: '\u{1F527}', name: 'wrench', keywords: ['fix', 'maintenance', 'repair'] },
				{ emoji: '\u{1F529}', name: 'nut and bolt', keywords: ['hardware', 'build', 'maintenance'] },
				{ emoji: '\u{1F6E0}', name: 'hammer and wrench', keywords: ['project', 'diy', 'tools'] }
			]
		},
		{
			category: 'Health',
			values: [
				{ emoji: '\u{1F3C3}', name: 'person running', keywords: ['exercise', 'cardio', 'fitness'] },
				{ emoji: '\u{1F6B4}', name: 'person biking', keywords: ['ride', 'cycle', 'workout'] },
				{ emoji: '\u{1F3CB}', name: 'person lifting weights', keywords: ['gym', 'strength', 'train'] },
				{ emoji: '\u{1F9D8}', name: 'person in lotus position', keywords: ['meditation', 'mindfulness', 'calm'] },
				{ emoji: '\u{1F9D1}\u{200D}\u{2695}\u{FE0F}', name: 'health worker', keywords: ['doctor', 'clinic', 'medical'] },
				{ emoji: '\u{1F48A}', name: 'pill', keywords: ['medicine', 'prescription', 'meds'] },
				{ emoji: '\u{1FA7A}', name: 'stethoscope', keywords: ['checkup', 'diagnosis', 'appointment'] },
				{ emoji: '\u{1FA79}', name: 'drop of blood', keywords: ['lab', 'test', 'health'] },
				{ emoji: '\u{1F34E}', name: 'red apple', keywords: ['nutrition', 'diet', 'fruit'] },
				{ emoji: '\u{1F957}', name: 'green salad', keywords: ['meal', 'healthy', 'food'] },
				{ emoji: '\u{1F4A7}', name: 'droplet', keywords: ['water', 'hydrate', 'drink'] },
				{ emoji: '\u{1F6CC}', name: 'person in bed', keywords: ['sleep', 'rest', 'recovery'] }
			]
		},
		{
			category: 'Learning',
			values: [
				{ emoji: '\u{1F4DA}', name: 'books', keywords: ['study', 'read', 'learn'] },
				{ emoji: '\u{1F4D8}', name: 'blue book', keywords: ['textbook', 'class', 'school'] },
				{ emoji: '\u{1F4D6}', name: 'open book', keywords: ['research', 'reading', 'knowledge'] },
				{ emoji: '\u{1F393}', name: 'graduation cap', keywords: ['education', 'course', 'degree'] },
				{ emoji: '\u{1F9EA}', name: 'test tube', keywords: ['science', 'experiment', 'lab'] },
				{ emoji: '\u{1F52C}', name: 'microscope', keywords: ['biology', 'analysis', 'research'] },
				{ emoji: '\u{1F52D}', name: 'telescope', keywords: ['observe', 'astronomy', 'explore'] },
				{ emoji: '\u{1F4D0}', name: 'triangular ruler', keywords: ['math', 'geometry', 'measure'] },
				{ emoji: '\u{270F}\u{FE0F}', name: 'pencil', keywords: ['write', 'draft', 'homework'] },
				{ emoji: '\u{1F4DD}', name: 'memo', keywords: ['notes', 'lecture', 'summary'] },
				{ emoji: '\u{1F9E0}', name: 'brain', keywords: ['thinking', 'memory', 'focus'] },
				{ emoji: '\u{1F4AC}', name: 'speech balloon', keywords: ['discussion', 'debate', 'language'] }
			]
		},
		{
			category: 'Personal',
			values: [
				{ emoji: '\u{2764}\u{FE0F}', name: 'red heart', keywords: ['love', 'care', 'relationship'] },
				{ emoji: '\u{1F46A}', name: 'family', keywords: ['home', 'kids', 'relatives'] },
				{ emoji: '\u{1F973}', name: 'partying face', keywords: ['celebration', 'event', 'birthday'] },
				{ emoji: '\u{1F381}', name: 'wrapped gift', keywords: ['present', 'gift', 'holiday'] },
				{ emoji: '\u{1F4F8}', name: 'camera with flash', keywords: ['photos', 'memories', 'travel'] },
				{ emoji: '\u{1F4DE}', name: 'telephone receiver', keywords: ['call', 'catch up', 'friend'] },
				{ emoji: '\u{1F4E7}', name: 'email', keywords: ['message', 'send', 'invite'] },
				{ emoji: '\u{1F5D3}', name: 'spiral calendar', keywords: ['events', 'plans', 'appointments'] },
				{ emoji: '\u{1F3B5}', name: 'musical note', keywords: ['music', 'practice', 'playlist'] },
				{ emoji: '\u{1F3AC}', name: 'clapper board', keywords: ['movie', 'watch', 'film'] },
				{ emoji: '\u{1F3AE}', name: 'video game', keywords: ['play', 'gaming', 'relax'] },
				{ emoji: '\u{1F3A8}', name: 'artist palette', keywords: ['creative', 'art', 'hobby'] }
			]
		},
		{
			category: 'Travel',
			values: [
				{ emoji: '\u{2708}\u{FE0F}', name: 'airplane', keywords: ['flight', 'trip', 'travel'] },
				{ emoji: '\u{1F5FA}\u{FE0F}', name: 'world map', keywords: ['destination', 'route', 'explore'] },
				{ emoji: '\u{1F9F3}', name: 'luggage', keywords: ['pack', 'bags', 'vacation'] },
				{ emoji: '\u{1F697}', name: 'automobile', keywords: ['drive', 'road trip', 'car'] },
				{ emoji: '\u{1F686}', name: 'train', keywords: ['commute', 'rail', 'transit'] },
				{ emoji: '\u{1F68C}', name: 'bus', keywords: ['transport', 'route', 'city'] },
				{ emoji: '\u{1F6F3}\u{FE0F}', name: 'passenger ship', keywords: ['cruise', 'boat', 'sea'] },
				{ emoji: '\u{1F3D6}\u{FE0F}', name: 'beach with umbrella', keywords: ['vacation', 'summer', 'coast'] },
				{ emoji: '\u{1F3D4}\u{FE0F}', name: 'snow-capped mountain', keywords: ['hike', 'outdoor', 'trail'] },
				{ emoji: '\u{1F3E8}', name: 'hotel', keywords: ['stay', 'booking', 'trip'] },
				{ emoji: '\u{1F4CD}', name: 'round pushpin', keywords: ['location', 'place', 'map'] },
				{ emoji: '\u{1F6C2}', name: 'passport control', keywords: ['airport', 'border', 'international'] }
			]
		},
		{
			category: 'Focus',
			values: [
				{ emoji: '\u{1F525}', name: 'fire', keywords: ['streak', 'momentum', 'intense'] },
				{ emoji: '\u{26A1}', name: 'high voltage', keywords: ['energy', 'fast', 'power'] },
				{ emoji: '\u{1F9E9}', name: 'puzzle piece', keywords: ['problem solving', 'logic', 'build'] },
				{ emoji: '\u{1F3AF}', name: 'bullseye', keywords: ['target', 'precision', 'goal'] },
				{ emoji: '\u{1F50D}', name: 'magnifying glass', keywords: ['review', 'inspect', 'analyze'] },
				{ emoji: '\u{1F4A5}', name: 'collision', keywords: ['breakthrough', 'impact', 'push'] },
				{ emoji: '\u{1F4AA}', name: 'flexed biceps', keywords: ['discipline', 'effort', 'grit'] },
				{ emoji: '\u{1F3C1}', name: 'chequered flag', keywords: ['finish', 'complete', 'end'] },
				{ emoji: '\u{1F6A7}', name: 'construction', keywords: ['in progress', 'wip', 'work'] },
				{ emoji: '\u{1F3D7}\u{FE0F}', name: 'building construction', keywords: ['build', 'project', 'develop'] },
				{ emoji: '\u{1F4A8}', name: 'dash', keywords: ['sprint', 'speed', 'rush'] },
				{ emoji: '\u{23F3}', name: 'hourglass', keywords: ['timebox', 'timer', 'focus'] }
			]
		},
		{
			category: 'Errands',
			values: [
				{ emoji: '\u{1F6D2}', name: 'shopping cart', keywords: ['buy', 'store', 'groceries'] },
				{ emoji: '\u{1F3E6}', name: 'bank', keywords: ['money', 'finance', 'account'] },
				{ emoji: '\u{1F4EC}', name: 'open mailbox', keywords: ['mail', 'post office', 'send'] },
				{ emoji: '\u{1F4E6}', name: 'package', keywords: ['pickup', 'delivery', 'parcel'] },
				{ emoji: '\u{1F69A}', name: 'delivery truck', keywords: ['shipment', 'dropoff', 'courier'] },
				{ emoji: '\u{1F3E5}', name: 'hospital', keywords: ['appointment', 'medical', 'visit'] },
				{ emoji: '\u{1F489}', name: 'syringe', keywords: ['vaccine', 'shot', 'clinic'] },
				{ emoji: '\u{1F9FE}', name: 'receipt', keywords: ['bill', 'payment', 'expenses'] },
				{ emoji: '\u{1F4B3}', name: 'credit card', keywords: ['pay', 'purchase', 'wallet'] },
				{ emoji: '\u{1F691}', name: 'ambulance', keywords: ['urgent', 'emergency', 'medical'] },
				{ emoji: '\u{1F6D1}', name: 'stop sign', keywords: ['blocker', 'pause', 'waiting'] },
				{ emoji: '\u{1F512}', name: 'locked', keywords: ['security', 'account', 'private'] }
			]
		}
	];

	let {
		open = false,
		onClose = () => {},
		onSelect = (_emoji: string) => {}
	}: {
		open?: boolean;
		onClose?: () => void;
		onSelect?: (emoji: string) => void;
	} = $props();

	let query = $state('');
	const normalizedQuery = $derived(query.trim().toLowerCase());

	const filtered = $derived(
		EMOJIS.map((group) => ({
			...group,
			values: group.values.filter((item) => {
				if (!normalizedQuery) return true;
				const haystack = `${group.category} ${item.name} ${item.keywords.join(' ')}`.toLowerCase();
				return haystack.includes(normalizedQuery) || item.emoji.includes(normalizedQuery);
			})
		})).filter((group) => group.values.length > 0)
	);

	function handleSelect(emoji: string): void {
		onSelect(emoji);
		onClose();
	}

	function handleBackdrop(event: MouseEvent): void {
		if (event.target === event.currentTarget) {
			onClose();
		}
	}

	function handleKey(event: KeyboardEvent): void {
		if (event.key === 'Escape') {
			onClose();
		}
	}
</script>

{#if open}
	<div class="backdrop" onclick={handleBackdrop} onkeydown={handleKey} tabindex="0" role="dialog" aria-modal="true">
		<div class="picker">
			<input bind:value={query} placeholder="Search emoji..." />
			{#each filtered as group}
				<div class="group">
					<strong>{group.category}</strong>
					<div class="grid">
						{#each group.values as item (`${group.category}-${item.emoji}-${item.name}`)}
							<button
								type="button"
								title={item.name}
								aria-label={item.name}
								data-emoji={item.emoji}
								onclick={() => handleSelect(item.emoji)}
							>
								{item.emoji}
							</button>
						{/each}
					</div>
				</div>
			{/each}
			{#if filtered.length === 0}
				<p class="empty">No emoji found for "{query}".</p>
			{/if}
		</div>
	</div>
{/if}

<style>
	.backdrop {
		position: fixed;
		inset: 0;
		background: var(--backdrop);
		backdrop-filter: blur(2px);
		display: grid;
		place-items: center;
		z-index: 50;
	}

	.picker {
		background: var(--bg-surface);
		border-radius: var(--radius-xl);
		padding: 1rem;
		width: min(92vw, 420px);
		max-height: 72vh;
		overflow: auto;
		border: 1px solid var(--border);
		box-shadow: var(--shadow-lg);
	}

	.picker strong {
		font-family: var(--font-display);
		font-size: 0.9rem;
		color: var(--text-secondary);
	}

	input {
		width: 100%;
		padding: 0.5rem 0.7rem;
		border: 1px solid var(--border);
		border-radius: var(--radius-md);
		margin-bottom: 0.75rem;
		font-family: var(--font-body);
		font-size: 0.85rem;
		color: var(--text-primary);
		background: var(--bg-input);
	}

	input::placeholder {
		color: var(--text-tertiary);
	}

	input:focus {
		outline: none;
		border-color: var(--border-focus);
	}

	.group {
		margin-bottom: 0.75rem;
	}

	.grid {
		display: grid;
		grid-template-columns: repeat(5, minmax(0, 1fr));
		gap: 0.35rem;
		margin-top: 0.35rem;
	}

	button {
		border: 1px solid var(--border-light);
		background: var(--bg-surface);
		border-radius: var(--radius-sm);
		padding: 0.45rem 0;
		font-size: 1.1rem;
		cursor: pointer;
		transition: all var(--transition);
	}

	button:hover {
		background: var(--accent-light);
		border-color: var(--accent);
		transform: scale(1.1);
	}

	.empty {
		margin: 0.6rem 0 0;
		color: var(--text-secondary);
		font-size: 0.85rem;
	}
</style>
