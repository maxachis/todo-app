/* ============================================
   Toast Management
   ============================================ */

function dismissToast() {
  var toast = document.getElementById("undo-toast");
  if (toast) {
    toast.style.animation = "toastOut 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards";
    toast.addEventListener("animationend", function() {
      if (toast.parentNode) toast.remove();
    });
  }
}

function setupToastDismiss() {
  document.querySelectorAll("#toast-container .toast").forEach(function(toast) {
    if (toast.dataset.dismissBound === "1") return;
    toast.dataset.dismissBound = "1";

    var timeout = parseInt(toast.dataset.autoDismiss, 10) || 5000;
    setTimeout(function() {
      if (toast && toast.parentNode) {
        toast.style.animation = "toastOut 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards";
        toast.addEventListener("animationend", function() {
          if (toast.parentNode) toast.remove();
        });
      }
    }, timeout);
  });
}

// Ensure newly injected OOB toasts always get dismissal timers.
document.addEventListener("htmx:oobAfterSwap", function(e) {
  if (!e.detail || !e.detail.target) return;
  if (e.detail.target.id !== "toast-container") return;
  setupToastDismiss();
});

// Fallback for non-OOB swaps and initial page load.
document.addEventListener("htmx:afterSettle", setupToastDismiss);
document.addEventListener("DOMContentLoaded", setupToastDismiss);
