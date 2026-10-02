const CACHE_NAME = 'jurnal-cache-v1';

self.addEventListener('install', (event) => {
    self.skipWaiting();
});

self.addEventListener('activate', (event) => {
    event.waitUntil(clients.claim());
});

self.addEventListener('fetch', (event) => {
    // Teruskan langsung ke server Django
    event.respondWith(
        fetch(event.request).catch(() => caches.match(event.request))
    );
});