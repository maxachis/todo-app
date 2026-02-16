/* ============================================
   Emoji Picker
   ============================================ */

var emojiPickerEl = null;
var emojiPickerTarget = null;
var emojiPickerTrigger = null;

function createEmojiPicker() {
  if (emojiPickerEl) return emojiPickerEl;

  var picker = document.createElement("div");
  picker.className = "emoji-picker";
  picker.style.display = "none";

  var searchDiv = document.createElement("div");
  searchDiv.className = "emoji-picker-search";
  var searchInput = document.createElement("input");
  searchInput.type = "text";
  searchInput.placeholder = "Search emoji...";
  searchDiv.appendChild(searchInput);
  picker.appendChild(searchDiv);

  var gridContainer = document.createElement("div");
  gridContainer.className = "emoji-picker-grid";
  picker.appendChild(gridContainer);

  function renderEmojis(filter) {
    gridContainer.innerHTML = "";
    var lowerFilter = (filter || "").toLowerCase();

    if (typeof EMOJI_DATA === "undefined") return;

    EMOJI_DATA.forEach(function(cat) {
      var filtered = cat.emojis;
      if (lowerFilter) {
        filtered = cat.emojis.filter(function(em) {
          return em.n.indexOf(lowerFilter) !== -1;
        });
      }
      if (filtered.length === 0) return;

      var label = document.createElement("div");
      label.className = "emoji-category-label";
      label.textContent = cat.name;
      gridContainer.appendChild(label);

      var grid = document.createElement("div");
      grid.className = "emoji-grid";

      filtered.forEach(function(em) {
        var btn = document.createElement("button");
        btn.type = "button";
        btn.className = "emoji-btn";
        btn.textContent = em.e;
        btn.title = em.n;
        btn.addEventListener("click", function() {
          selectEmoji(em.e);
        });
        grid.appendChild(btn);
      });

      gridContainer.appendChild(grid);
    });
  }

  var searchTimer = null;
  searchInput.addEventListener("input", function() {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(function() {
      renderEmojis(searchInput.value);
    }, 150);
  });

  renderEmojis("");
  document.body.appendChild(picker);
  emojiPickerEl = picker;
  return picker;
}

function selectEmoji(emoji) {
  if (emojiPickerTarget) {
    emojiPickerTarget.value = emoji;
  }
  var trigger = emojiPickerTrigger;
  if (trigger) {
    trigger.textContent = emoji;
  }
  closeEmojiPicker();

  if (trigger) {
    var editForm = trigger.closest(".list-nav-edit-form, .list-header-edit-form");
    if (editForm) {
      htmx.trigger(editForm, "submit");
    }
  }
}

function openEmojiPicker(triggerBtn) {
  var picker = createEmojiPicker();
  var form = triggerBtn.closest("form");
  var targetName = triggerBtn.dataset.emojiTarget;
  emojiPickerTarget = form ? form.querySelector('input[name="' + targetName + '"]') : null;
  emojiPickerTrigger = triggerBtn;

  var rect = triggerBtn.getBoundingClientRect();
  var pickerWidth = 320;
  var pickerHeight = 360;

  var left = rect.left;
  var top = rect.bottom + 4;

  if (left + pickerWidth > window.innerWidth) {
    left = window.innerWidth - pickerWidth - 8;
  }
  if (top + pickerHeight > window.innerHeight) {
    top = rect.top - pickerHeight - 4;
  }

  picker.style.left = left + "px";
  picker.style.top = top + "px";
  picker.style.display = "flex";

  var searchInput = picker.querySelector("input");
  if (searchInput) {
    searchInput.value = "";
    var gridContainer = picker.querySelector(".emoji-picker-grid");
    if (gridContainer) {
      renderAllEmojis(gridContainer, "");
    }
    setTimeout(function() { searchInput.focus(); }, 50);
  }
}

function renderAllEmojis(gridContainer, filter) {
  gridContainer.innerHTML = "";
  var lowerFilter = (filter || "").toLowerCase();

  if (typeof EMOJI_DATA === "undefined") return;

  EMOJI_DATA.forEach(function(cat) {
    var filtered = cat.emojis;
    if (lowerFilter) {
      filtered = cat.emojis.filter(function(em) {
        return em.n.indexOf(lowerFilter) !== -1;
      });
    }
    if (filtered.length === 0) return;

    var label = document.createElement("div");
    label.className = "emoji-category-label";
    label.textContent = cat.name;
    gridContainer.appendChild(label);

    var grid = document.createElement("div");
    grid.className = "emoji-grid";

    filtered.forEach(function(em) {
      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "emoji-btn";
      btn.textContent = em.e;
      btn.title = em.n;
      btn.addEventListener("click", function() {
        selectEmoji(em.e);
      });
      grid.appendChild(btn);
    });

    gridContainer.appendChild(grid);
  });
}

function closeEmojiPicker() {
  if (emojiPickerEl) {
    emojiPickerEl.style.display = "none";
  }
  emojiPickerTarget = null;
  emojiPickerTrigger = null;
}

function initEmojiPickers() {
  document.querySelectorAll(".emoji-trigger").forEach(function(btn) {
    if (btn._emojiBound) return;
    btn._emojiBound = true;

    btn.addEventListener("click", function(e) {
      e.preventDefault();
      e.stopPropagation();
      if (emojiPickerEl && emojiPickerEl.style.display !== "none" && emojiPickerTrigger === btn) {
        closeEmojiPicker();
      } else {
        openEmojiPicker(btn);
      }
    });

    var form = btn.closest("form");
    var targetName = btn.dataset.emojiTarget;
    if (form) {
      var hiddenInput = form.querySelector('input[name="' + targetName + '"]');
      if (hiddenInput && hiddenInput.value) {
        btn.textContent = hiddenInput.value;
      }
    }
  });
}

// Close picker on outside click or Escape
document.addEventListener("click", function(e) {
  if (emojiPickerEl && emojiPickerEl.style.display !== "none") {
    if (!emojiPickerEl.contains(e.target) && !e.target.classList.contains("emoji-trigger")) {
      closeEmojiPicker();
    }
  }
});
document.addEventListener("keydown", function(e) {
  if (e.key === "Escape" && emojiPickerEl && emojiPickerEl.style.display !== "none") {
    closeEmojiPicker();
  }
});
