/* ============================================
   Focus Tracking & Restoration after HTMX Swaps
   ============================================ */

var lastFocusedInputSelector = null;
var _suppressRestoreFocus = false;

function suppressRestoreFocus() {
  _suppressRestoreFocus = true;
}

function trackFormFocus() {
  document.addEventListener("focusin", function(e) {
    var el = e.target;
    if (el.matches(".inline-form input[type='text'], .task-form input[type='text'], .section-form input[type='text'], .tag-form input[type='text']")) {
      var form = el.closest("form");
      if (form) {
        if (form.classList.contains("task-form")) {
          var section = form.closest(".section");
          if (section) {
            lastFocusedInputSelector = '.section[data-section-id="' + section.dataset.sectionId + '"] .task-form input[name="title"]';
          }
        } else if (form.classList.contains("section-form")) {
          lastFocusedInputSelector = '.section-form input[name="name"]';
        } else if (form.classList.contains("tag-form")) {
          lastFocusedInputSelector = '.tag-form input[name="name"]';
        } else if (form.closest(".sidebar")) {
          lastFocusedInputSelector = '.sidebar .inline-form input[name="name"]';
        }
      }
    }
  });
}

function restoreFocus() {
  if (lastFocusedInputSelector) {
    // When keyboard navigation has just moved from an input to a task row
    // (e.g. ArrowUp from "Add a task"), skip restoring focus to that input.
    // Without this guard the HTMX detail-panel swap triggers initAll() →
    // restoreFocus() which re-focuses the input, forcing the user to press
    // ArrowUp an extra time.
    if (_suppressRestoreFocus) {
      _suppressRestoreFocus = false;
      lastFocusedInputSelector = null;
      return;
    }
    var el = document.querySelector(lastFocusedInputSelector);
    if (el) {
      el.focus();
    }
    lastFocusedInputSelector = null;
  } else {
    _suppressRestoreFocus = false;
  }
}
