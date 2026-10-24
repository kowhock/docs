// Tiny local stand-in for the Supabase API gateway:
//   /rest/v1/*  → PostgREST on :3001
//   /auth/v1/*  → fake GoTrue (password = "demo" for every user in auth.users)
//   /storage/v1 → accepts uploads, serves a placeholder
//   /realtime   → not available (pages still work, just no live refresh)
const http = require("http");
const httpProxy = require("http-proxy");
const jwt = require("jsonwebtoken");
const { execFileSync } = require("child_process");

const SECRET = "super-secret-jwt-token-with-at-least-32-characters-long";
const proxy = httpProxy.createProxyServer({ target: "http://127.0.0.1:3001" });
proxy.on("error", (e, req, res) => { res.writeHead(502); res.end(String(e)); });

function sql(q) {
  return execFileSync("psql", ["-h", "127.0.0.1", "-U", "postgres", "-d", "kh", "-At", "-c", q]).toString().trim();
}
function userByEmail(email) {
  const row = sql(`select row_to_json(u) from auth.users u where lower(email)=lower('${email.replace(/'/g, "''")}')`);
  return row ? JSON.parse(row) : null;
}
function userById(id) {
  const row = sql(`select row_to_json(u) from auth.users u where id='${id.replace(/'/g, "")}'`);
  return row ? JSON.parse(row) : null;
}
const asUser = (u) => ({
  id: u.id, aud: "authenticated", role: "authenticated", email: u.email,
  app_metadata: { provider: "email" }, user_metadata: u.raw_user_meta_data || {},
  created_at: u.created_at, updated_at: u.created_at, email_confirmed_at: u.created_at,
});
function session(u) {
  const now = Math.floor(Date.now() / 1000);
  const access_token = jwt.sign({ sub: u.id, role: "authenticated", aud: "authenticated", email: u.email, iat: now, exp: now + 86400 * 30 }, SECRET);
  return { access_token, token_type: "bearer", expires_in: 86400 * 30, expires_at: now + 86400 * 30, refresh_token: "r-" + u.id, user: asUser(u) };
}
const json = (res, code, body) => { res.writeHead(code, { "content-type": "application/json", "access-control-allow-origin": "*" }); res.end(JSON.stringify(body)); };
const readBody = (req) => new Promise((r) => { let b = ""; req.on("data", (c) => (b += c)); req.on("end", () => r(b)); });

const PNG = Buffer.from("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+ip1sAAAAASUVORK5CYII=", "base64");

http.createServer(async (req, res) => {
  const url = new URL(req.url, "http://x");
  if (req.method === "OPTIONS") { res.writeHead(204, { "access-control-allow-origin": "*", "access-control-allow-headers": "*", "access-control-allow-methods": "*" }); return res.end(); }
  if (url.pathname.startsWith("/rest/v1")) {
    req.url = req.url.replace(/^\/rest\/v1/, "") || "/";
    return proxy.web(req, res);
  }
  if (url.pathname.startsWith("/auth/v1")) {
    const p = url.pathname.slice(8);
    if (p === "/token") {
      const body = JSON.parse((await readBody(req)) || "{}");
      if (url.searchParams.get("grant_type") === "refresh_token") {
        const u = userById(String(body.refresh_token || "").slice(2));
        return u ? json(res, 200, session(u)) : json(res, 400, { error: "invalid_grant", error_description: "Invalid Refresh Token" });
      }
      const u = body.email && userByEmail(body.email);
      if (!u || body.password !== "demo") return json(res, 400, { error: "invalid_grant", error_description: "Invalid login credentials", code: "invalid_credentials" });
      return json(res, 200, session(u));
    }
    if (p === "/user") {
      try {
        const claims = jwt.verify((req.headers.authorization || "").replace(/^Bearer /i, ""), SECRET);
        const u = claims.sub && userById(claims.sub);
        return u ? json(res, 200, asUser(u)) : json(res, 401, { msg: "no user" });
      } catch { return json(res, 401, { code: 401, msg: "invalid JWT" }); }
    }
    if (p === "/logout") { res.writeHead(204); return res.end(); }
    return json(res, 404, { msg: "not supported locally" });
  }
  if (url.pathname.startsWith("/storage/v1")) {
    await readBody(req);
    if (req.method === "POST" || req.method === "PUT") return json(res, 200, { Key: url.pathname });
    if (url.pathname.includes("/object/sign/")) return json(res, 200, { signedURL: "/storage/v1/object/public/placeholder.png" });
    res.writeHead(200, { "content-type": "image/png" }); return res.end(PNG);
  }
  json(res, 404, { msg: "not available locally" });
}).listen(54321, () => console.log("gateway on :54321"));
