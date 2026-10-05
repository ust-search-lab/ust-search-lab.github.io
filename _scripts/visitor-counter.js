// Busuanzi's public JSON API: https://github.com/soxft/busuanzi/wiki/api
// One request per document, across both languages. No count on preview hosts.
window.addEventListener("DOMContentLoaded", async () => {
  const counter = document.querySelector("[data-visitor-counter]");
  if (!counter || counter.dataset.initialized) return;
  counter.dataset.initialized = "true";
  counter.hidden = false;

  const status = counter.querySelector("[data-counter-status]");
  const showStatus = (message) => {
    status.textContent = message;
    status.hidden = false;
  };

  if (location.protocol !== "https:" || location.host !== counter.dataset.host) {
    showStatus(counter.dataset.preview);
    return;
  }

  const identityKey = "search-lab-visitor-id";
  // Only site totals are used: do not send paths, query strings or referrers.
  const headers = { "x-bsz-referer": location.origin + "/" };
  try {
    const identity = localStorage.getItem(identityKey);
    if (identity) headers.Authorization = "Bearer " + identity;
  } catch {
    // Storage may be disabled. The provider can still estimate visitors.
  }

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 8000);
  try {
    const response = await fetch("https://busuanzi.9420.ltd/api", {
      method: "POST",
      headers,
      credentials: "omit",
      referrerPolicy: "no-referrer",
      cache: "no-store",
      signal: controller.signal,
    });
    if (!response.ok) throw new Error("Counter request failed");
    const result = await response.json();
    const visitors = result.data?.site_uv;
    if (!result.success || !Number.isSafeInteger(visitors) || visitors < 0) {
      throw new Error("Invalid counter response");
    }

    const format = new Intl.NumberFormat(document.documentElement.lang || "ko");
    counter.querySelector("[data-counter-visitors]").textContent = format.format(visitors);
    try {
      const identity = response.headers.get("Set-Bsz-Identity");
      if (identity) localStorage.setItem(identityKey, identity);
    } catch {
      // The displayed counts do not depend on local storage being available.
    }
  } catch {
    // Do not show zero or invent counts when the public service is unavailable.
    // No retries: a timed-out POST may already have been counted by the service.
    showStatus(counter.dataset.unavailable);
  } finally {
    clearTimeout(timeout);
  }
}, { once: true });
