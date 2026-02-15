/* ============================================
   Focus Tracking & Restoration after HTMX Swaps
   ============================================ */

var lastFocusedInputSelector = null;

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
    var el = document.querySelector(lastFocusedInputSelector);
    if (el) {
      el.focus();
    }
    lastFocusedInputSelector = null;
  }
}
