/* ============================================
   ToDo App — Orchestrator
   Calls init functions from individual modules.
   ============================================ */

function initAll() {
  try { initSortable(); } catch (ex) { console.error("initSortable error:", ex); }
  setupToastDismiss();
  try { initEmojiPickers(); } catch (ex) { console.error("initEmojiPickers error:", ex); }
  try { initTitleInput(); } catch (ex) { console.error("initTitleInput error:", ex); }
  try { initMarkdownEditor(); } catch (ex) { console.error("initMarkdownEditor error:", ex); }
  try { initListNameEdit(); } catch (ex) { console.error("initListNameEdit error:", ex); }
  try { initSectionNameEdit(); } catch (ex) { console.error("initSectionNameEdit error:", ex); }
  try { initMobilePanels(); } catch (ex) { console.error("initMobilePanels error:", ex); }
  updateSubtaskCounts();
  restoreTaskFocus();
  restoreFocus();
}

/* Debounced version of initAll for HTMX event handlers.
   Collapses rapid-fire calls (e.g. afterSwap + afterSettle
   firing back-to-back) into a single execution. */
var _initAllTimer = null;
function debouncedInitAll() {
  if (_initAllTimer) clearTimeout(_initAllTimer);
  _initAllTimer = setTimeout(function() {
    _initAllTimer = null;
    initAll();
  }, 16);
}

// Re-init after HTMX swaps.
document.addEventListener("htmx:afterSwap", function(e) {
  debouncedInitAll();
  if (e.detail.target && e.detail.target.id === "center-panel") {
    closeSidebar();
  }
  if (e.detail.target && e.detail.target.id === "page-body") {
    closeSidebar();
    closeDetailPanel();
    updateActiveNav();
  }
});
document.addEventListener("htmx:afterSettle", function(e) {
  debouncedInitAll();
});

// Init on page load
document.addEventListener("DOMContentLoaded", function() {
  trackFormFocus();
  initKeyboardNav();
  initCompletionTransitions();
  addSectionIntroAnimation();
  initAll();

  if ("serviceWorker" in navigator) {
    navigator.serviceWorker.register("/service-worker.js");
  }
});
