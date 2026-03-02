import {
	Decoration,
	type DecorationSet,
	EditorView,
	ViewPlugin,
	type ViewUpdate,
	WidgetType
} from '@codemirror/view';
import { type EditorState, RangeSetBuilder } from '@codemirror/state';
import { syntaxTree } from '@codemirror/language';

class CheckboxWidget extends WidgetType {
	readonly checked: boolean;
	readonly pos: number;

	constructor(checked: boolean, pos: number) {
		super();
		this.checked = checked;
		this.pos = pos;
	}

	eq(other: CheckboxWidget): boolean {
		return this.checked === other.checked && this.pos === other.pos;
	}

	toDOM(view: EditorView): HTMLElement {
		const input = document.createElement('input');
		input.type = 'checkbox';
		input.checked = this.checked;
		input.className = 'cm-checkbox-widget';
		input.addEventListener('mousedown', (e) => {
			e.preventDefault();
			const newText = this.checked ? '[ ]' : '[x]';
			// Find the [ ] or [x] at this position
			const doc = view.state.doc.toString();
			const oldText = this.checked ? '[x]' : '[ ]';
			// Search backwards from pos to find the checkbox marker
			const searchStart = Math.max(0, this.pos - 10);
			const searchEnd = Math.min(doc.length, this.pos + 10);
			const region = doc.substring(searchStart, searchEnd);
			const idx = region.indexOf(oldText);
			if (idx >= 0) {
				const from = searchStart + idx;
				const to = from + 3;
				view.dispatch({ changes: { from, to, insert: newText } });
			}
		});
		return input;
	}

	ignoreEvent(): boolean {
		return false;
	}
}

function getActiveLines(state: EditorState): Set<number> {
	const lines = new Set<number>();
	for (const range of state.selection.ranges) {
		const startLine = state.doc.lineAt(range.from).number;
		const endLine = state.doc.lineAt(range.to).number;
		for (let l = startLine; l <= endLine; l++) {
			lines.add(l);
		}
	}
	return lines;
}

function buildDecorations(view: EditorView): DecorationSet {
	const builder = new RangeSetBuilder<Decoration>();
	const state = view.state;
	const activeLines = getActiveLines(state);
	const tree = syntaxTree(state);

	const decos: { from: number; to: number; deco: Decoration }[] = [];

	tree.iterate({
		enter(node) {
			if (node.name === 'TaskMarker') {
				const line = state.doc.lineAt(node.from);
				if (activeLines.has(line.number)) return;

				const markerText = state.doc.sliceString(node.from, node.to);
				const checked = markerText === '[x]' || markerText === '[X]';

				// Find the full range to replace: "- [ ] " or "- [x] "
				// The ListMark (- ) is a sibling before the TaskMarker
				const lineText = line.text;
				const match = lineText.match(/^(\s*)-\s+\[[ xX]\]\s/);
				if (match) {
					const replaceFrom = line.from;
					const replaceTo = line.from + match[0].length;

					// Keep leading whitespace for indentation
					const indent = match[1];
					if (indent.length > 0) {
						// Replace just the "- [ ] " part after indent
						decos.push({
							from: line.from + indent.length,
							to: replaceTo,
							deco: Decoration.replace({
								widget: new CheckboxWidget(checked, node.from)
							})
						});
					} else {
						decos.push({
							from: replaceFrom,
							to: replaceTo,
							deco: Decoration.replace({
								widget: new CheckboxWidget(checked, node.from)
							})
						});
					}
				}
			}
		}
	});

	decos.sort((a, b) => a.from - b.from);
	for (const { from, to, deco } of decos) {
		if (from < to) {
			builder.add(from, to, deco);
		}
	}

	return builder.finish();
}

export const checkboxWidgets = ViewPlugin.fromClass(
	class {
		decorations: DecorationSet;
		constructor(view: EditorView) {
			this.decorations = buildDecorations(view);
		}
		update(update: ViewUpdate) {
			if (update.docChanged || update.selectionSet || update.viewportChanged) {
				this.decorations = buildDecorations(update.view);
			}
		}
	},
	{
		decorations: (v) => v.decorations,
		eventHandlers: {
			mousedown(e: MouseEvent) {
				const target = e.target as HTMLElement;
				if (target.classList?.contains('cm-checkbox-widget')) {
					return true; // Let the widget handle it
				}
				return false;
			}
		}
	}
);
