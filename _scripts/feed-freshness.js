// A failed scheduled job does not rebuild the site. Flag old snapshots in the
// browser as well, without fetching feeds or sending visitor information.
window.addEventListener("DOMContentLoaded", () => {
  const check = () => {
    document.querySelectorAll("[data-feed-updated]").forEach((section) => {
      const updated = Date.parse(section.dataset.feedUpdated);
      const hours = Number(section.dataset.feedMaxAge || 36);
      const notice = section.querySelector("[data-feed-delayed]");
      if (notice && Number.isFinite(updated)) {
        notice.hidden = Date.now() - updated < hours * 60 * 60 * 1000;
      }
    });
  };
  check();
  window.addEventListener("pageshow", check);
  document.addEventListener("visibilitychange", () => {
    if (!document.hidden) check();
  });
});
