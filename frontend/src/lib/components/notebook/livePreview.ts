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

class BulletWidget extends WidgetType {
	toDOM(): HTMLElement {
		const span = document.createElement('span');
		span.className = 'cm-bullet-widget';
		span.textContent = '• ';
		return span;
	}
}

class HorizontalRuleWidget extends WidgetType {
	toDOM(): HTMLElement {
		const hr = document.createElement('hr');
		hr.className = 'cm-hr-widget';
		return hr;
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

function isOnActiveLine(state: EditorState, from: number, to: number, activeLines: Set<number>): boolean {
	const startLine = state.doc.lineAt(from).number;
	const endLine = state.doc.lineAt(to).number;
	for (let l = startLine; l <= endLine; l++) {
		if (activeLines.has(l)) return true;
	}
	return false;
}

function buildDecorations(view: EditorView): DecorationSet {
	const builder = new RangeSetBuilder<Decoration>();
	const state = view.state;
	const activeLines = getActiveLines(state);
	const tree = syntaxTree(state);

	const decos: { from: number; to: number; deco: Decoration }[] = [];

	tree.iterate({
		enter(node) {
			const { from, to, name } = node;

			// ATX Headings (ATXHeading1 through ATXHeading6)
			if (name.startsWith('ATXHeading') && !name.includes('Mark')) {
				const level = parseInt(name.replace('ATXHeading', ''), 10);
				if (!level || level < 1 || level > 6) return;

				if (!isOnActiveLine(state, from, to, activeLines)) {
					// Find the HeaderMark (# symbols + space)
					let markEnd = from;
					node.node.cursor().iterate((child) => {
						if (child.name === 'HeaderMark') {
							markEnd = child.to;
						}
					});
					// Include the space after the mark
					const lineText = state.doc.sliceString(from, to);
					const markerLen = level + 1; // "# " = 2, "## " = 3, etc.
					const actualMarkEnd = from + markerLen;
					if (actualMarkEnd <= to) {
						decos.push({
							from,
							to: actualMarkEnd,
							deco: Decoration.replace({})
						});
					}
					decos.push({
						from: actualMarkEnd,
						to,
						deco: Decoration.mark({ class: `cm-heading-${level}` })
					});
				}
				return false; // Don't recurse into heading children for other decorations
			}

			// Strong emphasis (**bold**)
			if (name === 'StrongEmphasis') {
				if (!isOnActiveLine(state, from, to, activeLines)) {
					// Hide the ** delimiters (2 chars each side)
					decos.push({ from, to: from + 2, deco: Decoration.replace({}) });
					decos.push({ from: from + 2, to: to - 2, deco: Decoration.mark({ class: 'cm-bold' }) });
					decos.push({ from: to - 2, to, deco: Decoration.replace({}) });
				}
				return false;
			}

			// Emphasis (*italic*)
			if (name === 'Emphasis') {
				if (!isOnActiveLine(state, from, to, activeLines)) {
					decos.push({ from, to: from + 1, deco: Decoration.replace({}) });
					decos.push({ from: from + 1, to: to - 1, deco: Decoration.mark({ class: 'cm-italic' }) });
					decos.push({ from: to - 1, to, deco: Decoration.replace({}) });
				}
				return false;
			}

			// Inline code (`code`)
			if (name === 'InlineCode') {
				if (!isOnActiveLine(state, from, to, activeLines)) {
					const text = state.doc.sliceString(from, to);
					// Find backtick boundaries
					const openTicks = text.match(/^`+/)?.[0].length || 1;
					const closeTicks = text.match(/`+$/)?.[0].length || 1;
					decos.push({ from, to: from + openTicks, deco: Decoration.replace({}) });
					decos.push({
						from: from + openTicks,
						to: to - closeTicks,
						deco: Decoration.mark({ class: 'cm-inline-code' })
					});
					decos.push({ from: to - closeTicks, to, deco: Decoration.replace({}) });
				}
				return false;
			}

			// Links [text](url)
			if (name === 'Link') {
				if (!isOnActiveLine(state, from, to, activeLines)) {
					// Find child nodes: [ LinkMark, content, LinkMark, URL ]
					let linkTextFrom = -1;
					let linkTextTo = -1;
					let urlStart = -1;

					node.node.cursor().iterate((child) => {
						if (child.name === 'LinkMark') {
							if (linkTextFrom === -1) {
								// Opening [
								linkTextFrom = child.to;
							} else if (linkTextTo === -1) {
								// Closing ]
								linkTextTo = child.from;
							}
						}
						if (child.name === 'URL') {
							urlStart = child.from;
						}
					});

					if (linkTextFrom >= 0 && linkTextTo >= 0) {
						// Hide [ before text
						decos.push({ from, to: linkTextFrom, deco: Decoration.replace({}) });
						// Style link text
						decos.push({
							from: linkTextFrom,
							to: linkTextTo,
							deco: Decoration.mark({ class: 'cm-link-text' })
						});
						// Hide ](url)
						decos.push({ from: linkTextTo, to, deco: Decoration.replace({}) });
					}
				}
				return false;
			}

			// Horizontal rule
			if (name === 'HorizontalRule') {
				if (!isOnActiveLine(state, from, to, activeLines)) {
					decos.push({
						from,
						to,
						deco: Decoration.replace({ widget: new HorizontalRuleWidget() })
					});
				}
				return false;
			}

			// Fenced code blocks
			if (name === 'FencedCode') {
				if (!isOnActiveLine(state, from, to, activeLines)) {
					// Mark the whole block with code-block class
					decos.push({
						from,
						to,
						deco: Decoration.mark({ class: 'cm-code-block' })
					});
					// Hide opening and closing fence lines
					node.node.cursor().iterate((child) => {
						if (child.name === 'CodeMark') {
							const line = state.doc.lineAt(child.from);
							decos.push({
								from: line.from,
								to: Math.min(line.to + 1, state.doc.length),
								deco: Decoration.replace({})
							});
						}
					});
				}
				return false;
			}

			// Blockquotes
			if (name === 'Blockquote') {
				if (!isOnActiveLine(state, from, to, activeLines)) {
					decos.push({
						from,
						to,
						deco: Decoration.mark({ class: 'cm-blockquote' })
					});
					// Hide > markers
					node.node.cursor().iterate((child) => {
						if (child.name === 'QuoteMark') {
							// Replace "> " with nothing (the styling gives the visual indent)
							const afterMark = child.to;
							const nextChar = state.doc.sliceString(afterMark, afterMark + 1);
							const replEnd = nextChar === ' ' ? afterMark + 1 : afterMark;
							decos.push({
								from: child.from,
								to: replEnd,
								deco: Decoration.replace({})
							});
						}
					});
				}
				return false;
			}

			// List items — bullet replacement
			if (name === 'ListMark') {
				const mark = state.doc.sliceString(from, to);
				if (mark === '-' || mark === '*' || mark === '+') {
					if (!isOnActiveLine(state, from, to, activeLines)) {
						// Check if this is a task list item (has TaskMarker sibling)
						// If so, skip bullet replacement — checkbox widget handles it
						const parent = node.node.parent;
						let isTask = false;
						if (parent) {
							const cursor = parent.cursor();
							cursor.iterate((child) => {
								if (child.name === 'TaskMarker') isTask = true;
							});
						}
						if (!isTask) {
							// Replace "- " with bullet widget
							const afterMark = to;
							const nextChar = state.doc.sliceString(afterMark, afterMark + 1);
							const replEnd = nextChar === ' ' ? afterMark + 1 : afterMark;
							decos.push({
								from,
								to: replEnd,
								deco: Decoration.replace({ widget: new BulletWidget() })
							});
						}
					}
				}
			}
		}
	});

	// Sort by position (required by RangeSetBuilder)
	decos.sort((a, b) => a.from - b.from || a.to - b.to);

	for (const { from, to, deco } of decos) {
		if (from < to) {
			builder.add(from, to, deco);
		}
	}

	return builder.finish();
}

export const livePreview = ViewPlugin.fromClass(
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
		decorations: (v) => v.decorations
	}
);
