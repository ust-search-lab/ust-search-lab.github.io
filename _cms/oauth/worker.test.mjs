import test from "node:test";
import assert from "node:assert/strict";
import vm from "node:vm";
import worker from "./worker.mjs";

const origin = "https://ust-search-lab.github.io";
const env = { SITE_ORIGIN: origin, GITHUB_REPO: "ust-search-lab/ust-search-lab.github.io", GITHUB_CLIENT_ID: "test-client", GITHUB_CLIENT_SECRET: "test-secret" };
const host = "https://auth.example.org";
const request = (path, options) => new Request(host + path, options);
async function start() {
  const response = await worker.fetch(request("/auth?provider=github&site_id=ust-search-lab.github.io&scope=repo"), env);
  return { response, authorize: new URL(response.headers.get("Location")), cookie: response.headers.get("Set-Cookie").split(";")[0] };
}

test("setup, route, method and origin checks", async () => {
  assert.equal((await worker.fetch(request("/health"), {})).status, 503);
  assert.equal((await worker.fetch(request("/health"), env)).status, 200);
  assert.equal((await worker.fetch(request("/other"), env)).status, 404);
  assert.equal((await worker.fetch(request("/auth", { method: "POST" }), env)).status, 405);
  assert.equal((await worker.fetch(request("/auth?provider=github&site_id=evil.example"), env)).status, 400);
  assert.equal((await worker.fetch(request("/auth?provider=gitlab&site_id=ust-search-lab.github.io"), env)).status, 400);
  assert.equal((await worker.fetch(request("/health"), { ...env, SITE_ORIGIN: origin + "/" })).status, 503);
});

test("OAuth uses random state, PKCE, fixed callback, protected cookie and public scope", async () => {
  const { response, authorize, cookie } = await start();
  assert.equal(response.status, 302);
  assert.equal(authorize.origin, "https://github.com");
  assert.equal(authorize.searchParams.get("redirect_uri"), host + "/callback");
  assert.equal(authorize.searchParams.get("scope"), "public_repo");
  assert.equal(authorize.searchParams.get("code_challenge_method"), "S256");
  const [state, verifier] = cookie.split("=")[1].split(".");
  assert.equal(authorize.searchParams.get("state"), state);
  const digest = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(verifier));
  assert.equal(authorize.searchParams.get("code_challenge"), Buffer.from(digest).toString("base64url"));
  assert.match(response.headers.get("Set-Cookie"), /HttpOnly; Secure; SameSite=Lax/);
  assert.match(response.headers.get("Set-Cookie"), /Max-Age=600/);
  assert.notEqual((await start()).authorize.searchParams.get("state"), state);
});

test("callbacks with absent or mismatched state never contact GitHub", async (t) => {
  t.mock.method(globalThis, "fetch", () => { throw new Error("Must not contact GitHub"); });
  const { cookie } = await start();
  for (const headers of [{}, { Cookie: cookie }, { Cookie: "__Host-decap-oauth=forged.verifier" }]) {
    const response = await worker.fetch(request("/callback?code=code&state=invalid", { headers }), env);
    assert.equal(response.status, 400);
    assert.match(response.headers.get("Set-Cookie"), /Max-Age=0/);
  }
  assert.equal(globalThis.fetch.mock.callCount(), 0);
});

test("valid callback verifies repository permission and sends token only after an origin-bound handshake", async (t) => {
  const { authorize, cookie } = await start();
  const verifier = cookie.split("=")[1].split(".")[1];
  t.mock.method(globalThis, "fetch", async (url, options) => {
    if (url.endsWith("/access_token")) {
      assert.equal(options.body.get("client_secret"), env.GITHUB_CLIENT_SECRET);
      assert.equal(options.body.get("code_verifier"), verifier);
      return Response.json({ access_token: "test-token", token_type: "bearer" });
    }
    assert.equal(url, "https://api.github.com/repos/" + env.GITHUB_REPO);
    assert.equal(options.headers.Authorization, "Bearer test-token");
    return Response.json({ permissions: { push: true } });
  });
  const response = await worker.fetch(request("/callback?code=code&state=" + authorize.searchParams.get("state"), { headers: { Cookie: cookie } }), env);
  const html = await response.text();
  assert.equal(response.status, 200);
  assert.equal(response.headers.get("Cache-Control"), "no-store");
  assert.match(response.headers.get("Content-Security-Policy"), /default-src 'none'/);
  assert.doesNotMatch(html, /test-secret/);
  const sent = [];
  let receive;
  let closed = false;
  const opener = { postMessage: (...args) => sent.push(args) };
  const window = { opener, addEventListener: (_, handler) => { receive = handler; }, removeEventListener() {}, close() { closed = true; } };
  vm.runInNewContext(html.match(/<script nonce="[^"]+">([\s\S]+)<\/script>/)[1], { window });
  assert.deepEqual(sent, [["authorizing:github", origin]]);
  receive({ origin: "https://evil.example", source: opener, data: "authorizing:github" });
  receive({ origin, source: {}, data: "authorizing:github" });
  receive({ origin, source: opener, data: "wrong-message" });
  assert.equal(sent.length, 1);
  receive({ origin, source: opener, data: "authorizing:github" });
  assert.equal(sent[1][0], 'authorization:github:success:{"token":"test-token","provider":"github"}');
  assert.equal(sent[1][1], origin);
  assert.equal(closed, true);
});

test("denied repository permission, GitHub errors and cancellation never return a token", async (t) => {
  for (const failure of ["permission", "token", "network", "cancelled"]) {
    const mock = t.mock.method(globalThis, "fetch", async (url) => {
      if (failure === "network") throw new Error("Private error details");
      if (url.endsWith("/access_token")) return Response.json(failure === "token" ? { error: "bad_code" } : { access_token: "do-not-leak", token_type: "bearer" });
      return Response.json({ permissions: { push: false } });
    });
    const { authorize, cookie } = await start();
    const query = failure === "cancelled" ? "error=access_denied" : "code=code";
    const response = await worker.fetch(request(`/callback?${query}&state=${authorize.searchParams.get("state")}`, { headers: { Cookie: cookie } }), env);
    const html = await response.text();
    assert.match(html, /authorization:github:error:/);
    assert.doesNotMatch(html, /do-not-leak|test-secret|Private error details/);
    assert.match(response.headers.get("Set-Cookie"), /Max-Age=0/);
    mock.mock.restore();
  }
});
