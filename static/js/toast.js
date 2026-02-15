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
  var toast = document.getElementById("undo-toast");
  if (toast) {
    var timeout = parseInt(toast.dataset.autoDismiss) || 5000;
    setTimeout(function() {
      if (toast && toast.parentNode) {
        toast.style.animation = "toastOut 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards";
        toast.addEventListener("animationend", function() {
          if (toast.parentNode) toast.remove();
        });
      }
    }, timeout);
  }
}
