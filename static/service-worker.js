// Service Worker — ToDo App (PWA)
// Network-first for HTML/HTMX, cache-first for static assets.

var CACHE_NAME = "todo-v1";
var SHELL_ASSETS = [
  "/static/css/style.css",
  "/static/js/app.js",
  "/static/js/emoji_data.js",
  "/static/vendor/htmx.min.js",
  "/static/vendor/Sortable.min.js",
  "/static/icons/icon-192.png",
  "/static/icons/icon-512.png"
];

self.addEventListener("install", function (e) {
  e.waitUntil(
    caches.open(CACHE_NAME).then(function (cache) {
      return cache.addAll(SHELL_ASSETS);
    })
  );
  self.skipWaiting();
});

self.addEventListener("activate", function (e) {
  e.waitUntil(
    caches.keys().then(function (names) {
      return Promise.all(
        names
          .filter(function (n) { return n !== CACHE_NAME; })
          .map(function (n) { return caches.delete(n); })
      );
    })
  );
  self.clients.claim();
});

self.addEventListener("fetch", function (e) {
  var url = new URL(e.request.url);

  // Static assets: cache-first
  if (url.pathname.startsWith("/static/")) {
    e.respondWith(
      caches.match(e.request).then(function (cached) {
        return cached || fetch(e.request).then(function (resp) {
          var clone = resp.clone();
          caches.open(CACHE_NAME).then(function (cache) {
            cache.put(e.request, clone);
          });
          return resp;
        });
      })
    );
    return;
  }

  // HTML / HTMX requests: network-first, fall back to cache
  if (e.request.mode === "navigate" || e.request.headers.get("HX-Request")) {
    e.respondWith(
      fetch(e.request)
        .then(function (resp) {
          var clone = resp.clone();
          caches.open(CACHE_NAME).then(function (cache) {
            cache.put(e.request, clone);
          });
          return resp;
        })
        .catch(function () {
          return caches.match(e.request);
        })
    );
    return;
  }

  // Everything else: network with cache fallback
  e.respondWith(
    fetch(e.request).catch(function () {
      return caches.match(e.request);
    })
  );
});
