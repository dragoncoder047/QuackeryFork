// modified from https://stackoverflow.com/questions/70455869/how-to-enable-sharedarraybuffer-in-microsoft-edge-javascript

self.addEventListener("install", e => {
    self.skipWaiting();
    console.log('[service worker] installed!')
});

self.addEventListener("activate", e => {
    e.waitUntil(self.clients.claim());
    console.log('[service worker] activated!')
});

self.addEventListener("fetch", e => {
    if (e.request.cache === "only-if-cached" && e.request.mode !== "same-origin") {
        return;
    }
    console.log(`[service worker] fudging request to ${e.request.url} !`)

    e.respondWith(
        fetch(e.request).then(response => {
            // It seems like we only need to set the headers for index.html
            // If you want to be on the safe side, comment this out
            // if (!response.url.includes("index.html")) return response;

            const newHeaders = new Headers(response.headers);
            newHeaders.set("Cross-Origin-Embedder-Policy", "require-corp");
            newHeaders.set("Cross-Origin-Opener-Policy", "same-origin");

            const fudgedResponse = new Response(response.body, {
                status: response.status,
                statusText: response.statusText,
                headers: newHeaders,
            });
            console.log(`[service worker] fudging done!`)
            return fudgedResponse;
        }).catch(function (e) {
            console.error(e);
        })
    );
});