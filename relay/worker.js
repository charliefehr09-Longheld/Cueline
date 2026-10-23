// Cueline relay for AssemblyAI (Cloudflare Worker).
//
// Only needed if the iPad can't talk to AssemblyAI directly. It forwards Cueline's
// requests to AssemblyAI and adds the browser permission headers. Your API key is
// not stored here: Cueline sends it with each request, from your own device.
//
// Deploy: dash.cloudflare.com > Workers & Pages > Create > Hello World, replace the code
// with this file, Deploy, then paste the worker's URL into Cueline > Wrap > Advanced > Relay URL.

const UPSTREAM = "https://api.assemblyai.com"; // or https://api.eu.assemblyai.com
const ALLOWED_ORIGIN = "https://charliefehr09-longheld.github.io";
const ALLOWED_PATHS = /^\/v2\/(upload|transcript(\/[A-Za-z0-9-]+)?)$/;

export default {
  async fetch(request) {
    const cors = {
      "Access-Control-Allow-Origin": ALLOWED_ORIGIN,
      "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
      "Access-Control-Allow-Headers": "authorization, content-type",
      "Access-Control-Max-Age": "86400",
    };
    if (request.method === "OPTIONS") return new Response(null, { status: 204, headers: cors });
    const url = new URL(request.url);
    if (request.headers.get("Origin") !== ALLOWED_ORIGIN || !ALLOWED_PATHS.test(url.pathname)) {
      return new Response("Not allowed", { status: 403, headers: cors });
    }
    const upstream = await fetch(UPSTREAM + url.pathname + url.search, {
      method: request.method,
      headers: {
        authorization: request.headers.get("authorization") || "",
        "content-type": request.headers.get("content-type") || "application/json",
      },
      body: request.method === "GET" ? undefined : request.body,
    });
    const headers = new Headers(upstream.headers);
    Object.entries(cors).forEach(([k, v]) => headers.set(k, v));
    return new Response(upstream.body, { status: upstream.status, headers });
  },
};
