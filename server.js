// Ntandomods INC web server. No dependencies. Node 18+.
const http = require("http");
const fs = require("fs");
const path = require("path");

const PORT = process.env.PORT || 3000;
const API_BASE = (process.env.API_BASE || "https://ladybug-api-e8q8.onrender.com").replace(/\/+$/, "");
const CLOUD_URL = process.env.CLOUD_URL || "https://ladybugcloud.xubi.org/";
const RESEND_API_KEY = process.env.RESEND_API_KEY || "";
const CONTACT_TO = process.env.CONTACT_TO || "";
const CONTACT_FROM = process.env.CONTACT_FROM || "Ntandomods <onboarding@resend.dev>";
const PUBLIC = path.join(__dirname, "public");
const contactEnabled = !!(RESEND_API_KEY && CONTACT_TO);

const TYPES = {
  ".html": "text/html; charset=utf-8", ".css": "text/css; charset=utf-8", ".js": "text/javascript; charset=utf-8",
  ".svg": "image/svg+xml", ".png": "image/png", ".jpg": "image/jpeg", ".ico": "image/x-icon", ".txt": "text/plain; charset=utf-8",
  ".xml": "application/xml", ".json": "application/json",
};
const SECURITY = {
  "X-Content-Type-Options": "nosniff",
  "X-Frame-Options": "DENY",
  "Referrer-Policy": "strict-origin-when-cross-origin",
  "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
};

// ---- tiny per-IP rate limiter ----
const hits = new Map();
function limited(ip, bucket, max, windowMs) {
  const k = bucket + ":" + ip, now = Date.now();
  const arr = (hits.get(k) || []).filter((t) => now - t < windowMs);
  arr.push(now); hits.set(k, arr);
  return arr.length > max;
}
setInterval(() => { const now = Date.now(); for (const [k, v] of hits) if (!v.some((t) => now - t < 3600e3)) hits.delete(k); }, 600e3).unref();

const ipOf = (req) => (req.headers["x-forwarded-for"] || req.socket.remoteAddress || "").split(",")[0].trim();
const send = (res, code, body, headers = {}) => {
  res.writeHead(code, { ...SECURITY, ...headers });
  res.end(body);
};
const json = (res, code, obj) => send(res, code, JSON.stringify(obj), { "Content-Type": "application/json" });

function readBody(req, max = 20000) {
  return new Promise((resolve, reject) => {
    let n = 0; const chunks = [];
    req.on("data", (c) => { n += c.length; if (n > max) { reject(new Error("too large")); req.destroy(); } else chunks.push(c); });
    req.on("end", () => resolve(Buffer.concat(chunks).toString()));
    req.on("error", reject);
  });
}

// ---- Ladybug API proxy (allow-listed paths only) ----
const ALLOWED = [/^\/health$/, /^\/v1\/pricing\/free-key$/, /^\/v1\/utils\/(currency|dns|uuid|email-validate|hash|slug)$/, /^\/v1\/qr$/];
async function proxy(req, res, url) {
  const sub = url.pathname.replace(/^\/api\/ladybug/, "") || "/";
  if (!ALLOWED.some((r) => r.test(sub))) return json(res, 404, { error: "Endpoint not available in the demo" });
  if (limited(ipOf(req), "proxy", 60, 60e3)) return json(res, 429, { error: "Too many requests, slow down" });
  try {
    const headers = {};
    if (req.headers["x-api-key"]) headers["X-API-Key"] = req.headers["x-api-key"];
    const r = await fetch(API_BASE + sub + url.search, { method: req.method === "POST" ? "POST" : "GET", headers, signal: AbortSignal.timeout(30000) });
    const out = { "Content-Type": r.headers.get("content-type") || "application/octet-stream", "Cache-Control": "no-store" };
    for (const h of ["x-ratelimit-limit", "x-ratelimit-remaining", "x-ratelimit-reset", "retry-after"]) if (r.headers.get(h)) out[h] = r.headers.get(h);
    send(res, r.status, Buffer.from(await r.arrayBuffer()), out);
  } catch (e) {
    json(res, 502, { error: "The API did not respond. Try again in a moment." });
  }
}

// ---- contact form ----
const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
async function contact(req, res) {
  if (!contactEnabled) return json(res, 503, { error: "Contact form is not set up yet" });
  if (limited(ipOf(req), "contact", 5, 3600e3)) return json(res, 429, { error: "Too many messages from your connection" });
  let d;
  try { d = JSON.parse(await readBody(req)); } catch { return json(res, 400, { error: "Invalid request" }); }
  if (d.website) return json(res, 200, { ok: true }); // honeypot
  const name = String(d.name || "").trim().slice(0, 120), email = String(d.email || "").trim().slice(0, 200);
  const topic = String(d.topic || "Something else").slice(0, 60), msg = String(d.msg || "").trim().slice(0, 3000);
  if (!name || !msg || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) return json(res, 400, { error: "Please fill in your name, a valid email and a message" });
  const r = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: { Authorization: "Bearer " + RESEND_API_KEY, "Content-Type": "application/json" },
    body: JSON.stringify({
      from: CONTACT_FROM, to: [CONTACT_TO], reply_to: email, subject: `Ntandomods website: ${topic} (${name})`,
      html: `<p><b>${esc(name)}</b> &lt;${esc(email)}&gt;<br>Topic: ${esc(topic)}</p><p>${esc(msg).replace(/\n/g, "<br>")}</p>`,
    }),
  }).catch(() => null);
  if (!r || !r.ok) { console.error("resend failed", r && r.status, r && (await r.text())); return json(res, 502, { error: "Could not deliver your message" }); }
  json(res, 200, { ok: true });
}

// ---- static files ----
const pageCache = new Map();
function render(file) {
  const html = fs.readFileSync(file, "utf8");
  return html.replaceAll("{{API_BASE}}", API_BASE).replaceAll("{{API_HOST}}", new URL(API_BASE).host).replaceAll("{{CLOUD_URL}}", CLOUD_URL);
}
function serveStatic(req, res, url) {
  let p = decodeURIComponent(url.pathname);
  if (p === "/") p = "/index.html";
  const file = path.normalize(path.join(PUBLIC, p));
  if (!file.startsWith(PUBLIC) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) {
    const nf = path.join(PUBLIC, "404.html");
    return send(res, 404, fs.existsSync(nf) ? render(nf) : "Not found", { "Content-Type": "text/html; charset=utf-8" });
  }
  const ext = path.extname(file);
  const type = TYPES[ext] || "application/octet-stream";
  const cache = ext === ".html" ? "no-cache" : ext === ".svg" || ext === ".png" ? "public, max-age=86400" : "public, max-age=3600";
  if (ext === ".html") {
    if (!pageCache.has(file)) pageCache.set(file, render(file));
    return send(res, 200, pageCache.get(file), { "Content-Type": type, "Cache-Control": cache });
  }
  send(res, 200, fs.readFileSync(file), { "Content-Type": type, "Cache-Control": cache });
}

const server = http.createServer(async (req, res) => {
  try {
    const url = new URL(req.url, "http://x");
    if (url.pathname === "/healthz") return json(res, 200, { ok: true });
    if (url.pathname === "/api/config") return json(res, 200, { contact: contactEnabled, apiBase: API_BASE });
    if (url.pathname === "/api/contact" && req.method === "POST") return await contact(req, res);
    if (url.pathname.startsWith("/api/ladybug")) return await proxy(req, res, url);
    if (req.method !== "GET" && req.method !== "HEAD") return json(res, 405, { error: "Method not allowed" });
    serveStatic(req, res, url);
  } catch (e) {
    console.error(e);
    json(res, 500, { error: "Server error" });
  }
});
server.listen(PORT, () => console.log(`Ntandomods server on :${PORT}, API_BASE=${API_BASE}, contact=${contactEnabled}`));
