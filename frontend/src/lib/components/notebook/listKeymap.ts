import type { KeyBinding } from '@codemirror/view';
import { EditorSelection } from '@codemirror/state';
import type { EditorView } from '@codemirror/view';

const LIST_RE = /^(\s*)(-|\*|\+)\s/;
const LIST_WITH_CONTENT_RE = /^(\s*)(-|\*|\+)\s(.+)$/;
const EMPTY_LIST_RE = /^(\s*)(-|\*|\+)\s$/;
const CHECKBOX_RE = /^(\s*)(-|\*|\+)\s\[[ xX]\]\s/;
const CHECKBOX_WITH_CONTENT_RE = /^(\s*)(-|\*|\+)\s\[[ xX]\]\s(.+)$/;
const EMPTY_CHECKBOX_RE = /^(\s*)(-|\*|\+)\s\[[ xX]\]\s$/;

function indentList(view: EditorView): boolean {
	const { state } = view;
	const line = state.doc.lineAt(state.selection.main.head);
	if (!LIST_RE.test(line.text)) return false;

	view.dispatch({
		changes: { from: line.from, to: line.from, insert: '  ' }
	});
	return true;
}

function dedentList(view: EditorView): boolean {
	const { state } = view;
	const line = state.doc.lineAt(state.selection.main.head);
	if (!LIST_RE.test(line.text)) return false;

	const leadingSpaces = line.text.match(/^(\s*)/)?.[1].length || 0;
	if (leadingSpaces === 0) return false;

	const removeCount = Math.min(2, leadingSpaces);
	view.dispatch({
		changes: { from: line.from, to: line.from + removeCount }
	});
	return true;
}

function continueList(view: EditorView): boolean {
	const { state } = view;
	const head = state.selection.main.head;
	const line = state.doc.lineAt(head);

	// Only handle if cursor is at end of line
	if (head !== line.to) return false;

	// Check for empty list item — remove it
	const emptyCheckboxMatch = line.text.match(EMPTY_CHECKBOX_RE);
	if (emptyCheckboxMatch) {
		view.dispatch({
			changes: { from: line.from, to: line.to, insert: '' },
			selection: EditorSelection.cursor(line.from)
		});
		return true;
	}

	const emptyMatch = line.text.match(EMPTY_LIST_RE);
	if (emptyMatch) {
		view.dispatch({
			changes: { from: line.from, to: line.to, insert: '' },
			selection: EditorSelection.cursor(line.from)
		});
		return true;
	}

	// Continue checkbox list
	const checkboxMatch = line.text.match(CHECKBOX_WITH_CONTENT_RE);
	if (checkboxMatch) {
		const indent = checkboxMatch[1];
		const marker = checkboxMatch[2];
		const prefix = `\n${indent}${marker} [ ] `;
		view.dispatch({
			changes: { from: head, insert: prefix },
			selection: EditorSelection.cursor(head + prefix.length)
		});
		return true;
	}

	// Continue regular list
	const listMatch = line.text.match(LIST_WITH_CONTENT_RE);
	if (listMatch) {
		const indent = listMatch[1];
		const marker = listMatch[2];
		const prefix = `\n${indent}${marker} `;
		view.dispatch({
			changes: { from: head, insert: prefix },
			selection: EditorSelection.cursor(head + prefix.length)
		});
		return true;
	}

	return false;
}

export const listKeymap: KeyBinding[] = [
	{ key: 'Tab', run: indentList },
	{ key: 'Shift-Tab', run: dedentList },
	{ key: 'Enter', run: continueList }
];
