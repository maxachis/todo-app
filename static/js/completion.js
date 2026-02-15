/* ============================================
   Task Completion Transitions
   ============================================ */

/**
 * Apply optimistic CSS classes when a checkbox is clicked, providing
 * immediate visual feedback (fade-out) before the server responds.
 */
function initCompletionTransitions() {
  document.body.addEventListener("htmx:beforeRequest", function(e) {
    var elt = e.detail.elt;
    if (!elt || !elt.classList.contains("checkbox")) return;

    var taskItem = elt.closest(".task-item");
    if (!taskItem) return;

    var isCompleting = !elt.classList.contains("checked");
    if (isCompleting) {
      taskItem.classList.add("completing");
    } else {
      taskItem.classList.add("uncompleting");
    }
  });
}

/**
 * Add the intro animation class to sections on initial page load only.
 * Sections inserted later via HTMX swaps won't have this class,
 * so they appear instantly without a fadeInUp flash.
 */
function addSectionIntroAnimation() {
  document.querySelectorAll(".section").forEach(function(el) {
    el.classList.add("section-intro");
  });
}
