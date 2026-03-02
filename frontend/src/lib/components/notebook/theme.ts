import { EditorView } from '@codemirror/view';

export const notebookTheme = EditorView.theme({
	'&': {
		fontSize: '0.9rem',
		height: '100%'
	},
	'.cm-content': {
		fontFamily: 'var(--font-body)',
		lineHeight: '1.7',
		padding: '0.75rem',
		caretColor: 'var(--text-primary)'
	},
	'&.cm-focused': {
		outline: 'none'
	},
	'.cm-cursor, .cm-dropCursor': {
		borderLeftColor: 'var(--text-primary)'
	},
	'.cm-selectionBackground, &.cm-focused .cm-selectionBackground, ::selection': {
		background: 'var(--accent-light) !important'
	},
	'.cm-scroller': {
		overflow: 'auto'
	},
	'.cm-line': {
		padding: '0 2px'
	},

	// Heading styles
	'.cm-heading-1': { fontSize: '1.5em', fontWeight: '700', lineHeight: '1.3' },
	'.cm-heading-2': { fontSize: '1.25em', fontWeight: '700', lineHeight: '1.3' },
	'.cm-heading-3': { fontSize: '1.1em', fontWeight: '600', lineHeight: '1.4' },
	'.cm-heading-4': { fontSize: '1.05em', fontWeight: '600', lineHeight: '1.4' },
	'.cm-heading-5': { fontSize: '1em', fontWeight: '600', lineHeight: '1.5' },
	'.cm-heading-6': { fontSize: '0.95em', fontWeight: '600', lineHeight: '1.5', color: 'var(--text-secondary)' },

	// Inline styles
	'.cm-bold': { fontWeight: '700' },
	'.cm-italic': { fontStyle: 'italic' },
	'.cm-inline-code': {
		fontFamily: 'monospace',
		fontSize: '0.88em',
		background: 'var(--tag-bg)',
		borderRadius: '3px',
		padding: '1px 4px'
	},
	'.cm-link-text': {
		color: 'var(--accent)',
		textDecoration: 'underline',
		textDecorationColor: 'var(--accent-light)',
		textUnderlineOffset: '2px'
	},

	// Code blocks
	'.cm-code-block': {
		fontFamily: 'monospace',
		fontSize: '0.88em',
		background: 'var(--tag-bg)',
		borderRadius: '4px'
	},

	// Blockquotes
	'.cm-blockquote': {
		borderLeft: '3px solid var(--border)',
		paddingLeft: '0.75rem',
		color: 'var(--text-secondary)'
	},

	// Horizontal rule widget
	'.cm-hr-widget': {
		display: 'block',
		border: 'none',
		borderTop: '1px solid var(--border)',
		margin: '0.5em 0'
	},

	// Bullet widget
	'.cm-bullet-widget': {
		display: 'inline',
		color: 'var(--text-tertiary)',
		marginRight: '0.3em'
	},

	// Checkbox widget
	'.cm-checkbox-widget': {
		cursor: 'pointer',
		verticalAlign: 'middle',
		marginRight: '0.3em',
		accentColor: 'var(--accent)'
	},

	// Mention chips
	'.cm-mention-chip': {
		background: 'var(--accent-light)',
		borderRadius: '4px',
		padding: '1px 6px',
		fontSize: '0.88em',
		display: 'inline',
		whiteSpace: 'nowrap'
	},
	'.cm-mention-badge': {
		marginRight: '3px',
		fontSize: '0.85em'
	},
	'.cm-mention-label': {
		color: 'var(--accent)',
		fontWeight: '500'
	},
	'.cm-mention-new': {
		background: 'var(--warning-bg, #fef3c7)',
		borderColor: 'var(--warning, #d97706)'
	},
	'.cm-mention-new .cm-mention-label': {
		color: 'var(--warning, #d97706)'
	},
	'.cm-mention-notes': {
		color: 'var(--text-tertiary)',
		fontSize: '0.85em',
		fontStyle: 'italic'
	},

	// Autocomplete dropdown
	'.cm-tooltip-autocomplete': {
		background: 'var(--bg-surface) !important',
		border: '1px solid var(--border) !important',
		borderRadius: 'var(--radius-md) !important',
		boxShadow: 'var(--shadow-lg) !important',
		maxHeight: '260px',
		overflow: 'auto',
		fontFamily: 'var(--font-body)'
	},
	'.cm-tooltip-autocomplete ul': {
		fontFamily: 'var(--font-body)'
	},
	'.cm-tooltip-autocomplete li': {
		padding: '0.45rem 0.65rem !important',
		fontSize: '0.85rem',
		color: 'var(--text-primary)',
		lineHeight: '1.4'
	},
	'.cm-tooltip-autocomplete li[aria-selected]': {
		background: 'var(--accent-light) !important',
		color: 'var(--text-primary) !important'
	},
	'.cm-completionLabel': {
		fontFamily: 'var(--font-body)'
	},
	'.cm-completionDetail': {
		fontFamily: 'var(--font-body)',
		fontSize: '0.7rem',
		color: 'var(--text-tertiary)',
		textTransform: 'uppercase',
		marginLeft: '0.5rem',
		fontStyle: 'normal !important'
	}
});
