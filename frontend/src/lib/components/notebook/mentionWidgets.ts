import {
	Decoration,
	type DecorationSet,
	EditorView,
	ViewPlugin,
	type ViewUpdate,
	WidgetType
} from '@codemirror/view';
import { RangeSetBuilder } from '@codemirror/state';

const PERSON_RE = /@\[person:(\d+)\|([^\]]+)\]/g;
const ENTITY_RE = /\[\[(page|task|org|project):(\d+)\|([^\]]+)\]\]/g;

const TYPE_BADGES: Record<string, string> = {
	person: '\u{1F464}',
	task: '\u2713',
	page: '\u{1F4C4}',
	org: '\u{1F3E2}',
	project: '\u{1F4CB}'
};

class MentionWidget extends WidgetType {
	readonly type: string;
	readonly label: string;

	constructor(type: string, label: string) {
		super();
		this.type = type;
		this.label = label;
	}

	eq(other: MentionWidget): boolean {
		return this.type === other.type && this.label === other.label;
	}

	toDOM(): HTMLElement {
		const span = document.createElement('span');
		span.className = 'cm-mention-chip';

		const badge = document.createElement('span');
		badge.className = 'cm-mention-badge';
		badge.textContent = TYPE_BADGES[this.type] || '';

		const label = document.createElement('span');
		label.className = 'cm-mention-label';
		label.textContent = this.label;

		span.appendChild(badge);
		span.appendChild(label);
		return span;
	}

	ignoreEvent(): boolean {
		return false;
	}
}

function buildDecorations(view: EditorView): DecorationSet {
	const builder = new RangeSetBuilder<Decoration>();
	const doc = view.state.doc;
	const text = doc.toString();

	const decos: { from: number; to: number; deco: Decoration }[] = [];

	// Person mentions: @[person:ID|Label]
	let match: RegExpExecArray | null;
	PERSON_RE.lastIndex = 0;
	while ((match = PERSON_RE.exec(text)) !== null) {
		const from = match.index;
		const to = from + match[0].length;
		decos.push({
			from,
			to,
			deco: Decoration.replace({
				widget: new MentionWidget('person', match[2])
			})
		});
	}

	// Entity mentions: [[type:ID|Label]]
	ENTITY_RE.lastIndex = 0;
	while ((match = ENTITY_RE.exec(text)) !== null) {
		const from = match.index;
		const to = from + match[0].length;
		decos.push({
			from,
			to,
			deco: Decoration.replace({
				widget: new MentionWidget(match[1], match[3])
			})
		});
	}

	// Sort by position
	decos.sort((a, b) => a.from - b.from);
	for (const { from, to, deco } of decos) {
		if (from < to) {
			builder.add(from, to, deco);
		}
	}

	return builder.finish();
}

export const mentionWidgets = ViewPlugin.fromClass(
	class {
		decorations: DecorationSet;
		constructor(view: EditorView) {
			this.decorations = buildDecorations(view);
		}
		update(update: ViewUpdate) {
			if (update.docChanged || update.viewportChanged) {
				this.decorations = buildDecorations(update.view);
			}
		}
	},
	{
		decorations: (v) => v.decorations
	}
);
