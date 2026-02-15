/* ============================================
   Mobile Panels, Nav Highlight, Sidebar/Section Editing
   ============================================ */

// ─── Mobile Panel Toggles ───────────────────

function isMobileOrTablet() {
  return window.innerWidth < 1024;
}

function openSidebar() {
  document.body.classList.add("sidebar-open");
}

function closeSidebar() {
  document.body.classList.remove("sidebar-open");
}

function openDetailPanel() {
  if (isMobileOrTablet()) {
    document.body.classList.add("detail-open");
  }
}

function closeDetailPanel() {
  document.body.classList.remove("detail-open");
}

function initMobilePanels() {
  var hamburger = document.getElementById("sidebar-toggle");
  if (hamburger) {
    hamburger.addEventListener("click", function() {
      if (document.body.classList.contains("sidebar-open")) {
        closeSidebar();
      } else {
        openSidebar();
      }
    });
  }

  var sidebarBackdrop = document.getElementById("sidebar-backdrop");
  if (sidebarBackdrop) {
    sidebarBackdrop.addEventListener("click", closeSidebar);
  }

  var detailBackdrop = document.getElementById("detail-backdrop");
  if (detailBackdrop) {
    detailBackdrop.addEventListener("click", closeDetailPanel);
  }

  document.querySelectorAll(".detail-close-btn").forEach(function(btn) {
    if (btn._closeBound) return;
    btn._closeBound = true;
    btn.addEventListener("click", closeDetailPanel);
  });

  window.addEventListener("resize", function() {
    if (!isMobileOrTablet()) {
      closeSidebar();
      closeDetailPanel();
    }
  });
}

// ─── Active Nav Highlight ───────────────────

function updateActiveNav() {
  var path = window.location.pathname;
  var navMap = {
    "/": "todo",
    "/projects/": "projects",
    "/timesheet/": "timesheet",
    "/import/": "import"
  };

  var active = "";
  for (var prefix in navMap) {
    if (path === prefix || (prefix !== "/" && path.startsWith(prefix))) {
      active = navMap[prefix];
    }
  }
  if (!active && path === "/") active = "todo";

  document.querySelectorAll(".navbar-link").forEach(function(link) {
    link.classList.remove("active");
    var href = link.getAttribute("href");
    if (navMap[href] === active) link.classList.add("active");
  });

  document.querySelectorAll(".bottom-tab").forEach(function(tab) {
    tab.classList.remove("active");
    var href = tab.getAttribute("href");
    if (navMap[href] === active) tab.classList.add("active");
  });
}

// ─── Sidebar List Name Edit ──────────────────

function initListNameEdit() {
  document.querySelectorAll(".list-nav-item").forEach(function(li) {
    if (li._editBound) return;
    li._editBound = true;

    var display = li.querySelector(".list-nav-display");
    var form = li.querySelector(".list-nav-edit-form");
    if (!display || !form) return;

    var nameInput = form.querySelector('input[name="name"]');

    display.addEventListener("dblclick", function(e) {
      e.preventDefault();
      e.stopPropagation();
      li.classList.add("editing");
      if (nameInput) {
        nameInput.focus();
        nameInput.select();
      }
    });

    li.addEventListener("click", function(e) {
      if (li.classList.contains("editing") && !form.contains(e.target)) {
        e.preventDefault();
        e.stopPropagation();
      }
    }, true);

    li.addEventListener("htmx:confirm", function(e) {
      if (li.classList.contains("editing") && e.detail.elt === li) {
        e.preventDefault();
      }
    });

    if (nameInput) {
      nameInput.addEventListener("keydown", function(e) {
        if (e.key === "Enter") {
          e.preventDefault();
          htmx.trigger(form, "submit");
        } else if (e.key === "Escape") {
          e.preventDefault();
          cancelEdit(li);
        }
      });
    }
  });
}

// Click anywhere outside an editing list item saves the edit
document.addEventListener("mousedown", function(e) {
  var editingItem = document.querySelector(".list-nav-item.editing");
  if (!editingItem) return;
  var pickerOpen = emojiPickerEl && emojiPickerEl.style.display !== "none";
  if (editingItem.contains(e.target) || (pickerOpen && emojiPickerEl.contains(e.target))) return;
  var form = editingItem.querySelector(".list-nav-edit-form");
  if (form) {
    htmx.trigger(form, "submit");
  }
});

function cancelEdit(li) {
  li.classList.remove("editing");
  var nameInput = li.querySelector('.list-nav-edit-form input[name="name"]');
  var nameSpan = li.querySelector(".list-name");
  if (nameInput && nameSpan) {
    nameInput.value = nameSpan.textContent;
  }
  var emojiInput = li.querySelector('.list-nav-edit-form input[name="emoji"]');
  var emojiSpan = li.querySelector(".list-emoji");
  var emojiBtn = li.querySelector(".list-nav-edit-form .emoji-trigger");
  if (emojiInput && emojiSpan) {
    emojiInput.value = emojiSpan.textContent;
    if (emojiBtn) emojiBtn.textContent = emojiSpan.textContent || "+";
  }
}

// ─── Toggle All Sections ────────────────────

function toggleAllSections() {
  var sections = document.querySelectorAll("#center-panel .section");
  var btn = document.getElementById("toggle-all-sections");
  var anyOpen = false;
  sections.forEach(function(s) { if (s.open) anyOpen = true; });

  sections.forEach(function(s) {
    if (anyOpen) {
      s.removeAttribute("open");
    } else {
      s.setAttribute("open", "");
    }
  });

  if (btn) {
    btn.textContent = anyOpen ? "Expand All" : "Collapse All";
  }
}

// ─── Section Name Edit ──────────────────────

function initSectionNameEdit() {
  document.querySelectorAll(".section-edit-btn").forEach(function(btn) {
    if (btn._editBound) return;
    btn._editBound = true;

    btn.addEventListener("click", function(e) {
      e.preventDefault();
      var header = btn.closest(".section-header");
      if (!header) return;
      header.classList.add("editing");
      var input = header.querySelector(".section-edit-input");
      if (input) {
        input.focus();
        input.select();
      }
    });
  });

  document.querySelectorAll(".section-edit-cancel").forEach(function(btn) {
    if (btn._cancelBound) return;
    btn._cancelBound = true;

    btn.addEventListener("click", function(e) {
      e.preventDefault();
      var header = btn.closest(".section-header");
      if (header) header.classList.remove("editing");
    });
  });

  document.querySelectorAll(".section-edit-input").forEach(function(input) {
    if (input._keyBound) return;
    input._keyBound = true;

    input.addEventListener("keydown", function(e) {
      if (e.key === "Enter") {
        e.preventDefault();
        var form = input.closest(".section-edit-form");
        if (form) htmx.trigger(form, "submit");
      } else if (e.key === "Escape") {
        e.preventDefault();
        var header = input.closest(".section-header");
        if (header) header.classList.remove("editing");
      }
    });
  });
}
