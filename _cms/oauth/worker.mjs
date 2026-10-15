// A GitHub OAuth broker for Decap's popup handshake. Deploy separately from Pages.
const COOKIE = "__Host-decap-oauth";
const random = () => Array.from(crypto.getRandomValues(new Uint8Array(32)), (n) => n.toString(16).padStart(2, "0")).join("");
const cookie = (value, age) => `${COOKIE}=${value}; Path=/; Max-Age=${age}; HttpOnly; Secure; SameSite=Lax`;
const scriptJSON = (value) => JSON.stringify(value).replaceAll("<", "\\u003c");

function response(body, status = 200, extra = {}) {
  return new Response(body, {
    status,
    headers: {
      "Content-Type": "text/plain; charset=utf-8",
      "Cache-Control": "no-store",
      "Referrer-Policy": "no-referrer",
      "X-Content-Type-Options": "nosniff",
      "X-Frame-Options": "DENY",
      ...extra,
    },
  });
}

function popup(origin, payload, success) {
  const nonce = random();
  const result = `authorization:github:${success ? "success" : "error"}:${JSON.stringify(payload)}`;
  return response(`<!doctype html><html lang="ko"><meta charset="utf-8"><title>GitHub 로그인</title>
<p>관리자 화면으로 돌아가 주세요. 이 창은 닫아도 됩니다.</p>
<script nonce="${nonce}">
const origin = ${scriptJSON(origin)};
const result = ${scriptJSON(result)};
if (window.opener) {
  const receive = (event) => {
    if (event.origin !== origin || event.source !== window.opener || event.data !== "authorizing:github") return;
    window.removeEventListener("message", receive);
    window.opener.postMessage(result, origin);
    window.close();
  };
  window.addEventListener("message", receive);
  window.opener.postMessage("authorizing:github", origin);
}
</script></html>`, 200, {
    "Content-Type": "text/html; charset=utf-8",
    "Content-Security-Policy": `default-src 'none'; script-src 'nonce-${nonce}'; frame-ancestors 'none'; base-uri 'none'; form-action 'none'`,
    "Set-Cookie": cookie("", 0),
  });
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (request.method !== "GET") return response("Method not allowed", 405, { Allow: "GET" });
    if (!["/auth", "/callback", "/health"].includes(url.pathname)) return response("Not found", 404);
    let site;
    try {
      site = new URL(env.SITE_ORIGIN);
      if (site.protocol !== "https:" || site.origin !== env.SITE_ORIGIN) throw new Error();
      if (!env.GITHUB_CLIENT_ID || !env.GITHUB_CLIENT_SECRET || !/^[\w.-]+\/[\w.-]+$/.test(env.GITHUB_REPO)) throw new Error();
    } catch {
      return response("OAuth setup is incomplete. See _guides/cms-setup.md.", 503);
    }
    if (url.pathname === "/health") return response("OAuth service ready");
    if (url.protocol !== "https:") return response("HTTPS required", 400);

    if (url.pathname === "/auth") {
      if (url.searchParams.get("provider") !== "github" || url.searchParams.get("site_id") !== site.hostname) {
        return response("Unsupported provider or site", 400);
      }
      const state = random();
      const verifier = random();
      const digest = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(verifier));
      const challenge = btoa(String.fromCharCode(...new Uint8Array(digest))).replaceAll("+", "-").replaceAll("/", "_").replaceAll("=", "");
      const authorize = new URL("https://github.com/login/oauth/authorize");
      authorize.search = new URLSearchParams({
        client_id: env.GITHUB_CLIENT_ID,
        redirect_uri: `${url.origin}/callback`,
        scope: "public_repo", // This CMS only edits the public website repository.
        state,
        code_challenge: challenge,
        code_challenge_method: "S256",
      }).toString();
      return response("Redirecting to GitHub", 302, { Location: authorize.href, "Set-Cookie": cookie(`${state}.${verifier}`, 600) });
    }

    const stored = request.headers.get("Cookie")?.split(";").map((part) => part.trim()).find((part) => part.startsWith(`${COOKIE}=`))?.slice(COOKIE.length + 1) || "";
    const [state, verifier] = stored.split(".");
    if (!state || !/^[a-f0-9]{64}$/.test(state) || !/^[a-f0-9]{64}$/.test(verifier || "") || state !== url.searchParams.get("state")) {
      return response("Invalid or expired login. Close this window and try again.", 400, { "Set-Cookie": cookie("", 0) });
    }
    const fail = (message) => popup(site.origin, { message }, false);
    if (url.searchParams.has("error") || !url.searchParams.get("code")) return fail("GitHub 로그인이 취소되었거나 승인되지 않았습니다.");
    try {
      const tokenResponse = await fetch("https://github.com/login/oauth/access_token", {
        method: "POST",
        headers: { Accept: "application/json", "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({
          client_id: env.GITHUB_CLIENT_ID,
          client_secret: env.GITHUB_CLIENT_SECRET,
          code: url.searchParams.get("code"),
          redirect_uri: `${url.origin}/callback`,
          code_verifier: verifier,
        }),
        signal: AbortSignal.timeout(10000),
      });
      if (!tokenResponse.ok) return fail("GitHub 인증에 실패했습니다. 잠시 후 다시 로그인해 주세요.");
      const token = await tokenResponse.json();
      if (!token.access_token || token.token_type?.toLowerCase() !== "bearer") return fail("GitHub에서 로그인 토큰을 발급하지 못했습니다.");
      const repository = await fetch(`https://api.github.com/repos/${env.GITHUB_REPO}`, {
        headers: {
          Accept: "application/vnd.github+json", Authorization: `Bearer ${token.access_token}`,
          "User-Agent": "SEARCH-Lab-Decap-OAuth",
        },
        signal: AbortSignal.timeout(10000),
      });
      if (!repository.ok || !(await repository.json()).permissions?.push) {
        return fail("이 사이트 저장소의 쓰기 권한이 필요합니다. GitHub 조직의 앱 승인과 저장소 권한을 확인해 주세요.");
      }
      return popup(site.origin, { token: token.access_token, provider: "github" }, true);
    } catch {
      return fail("로그인 서비스 연결에 실패했습니다. 잠시 후 다시 시도해 주세요.");
    }
  },
};
