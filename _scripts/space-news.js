// A failed scheduled job does not rebuild the site. Flag old snapshots in the
// browser as well, without fetching feeds or sending visitor information.
window.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("[data-space-news-updated]").forEach((section) => {
    const updated = Date.parse(section.dataset.spaceNewsUpdated);
    const notice = section.querySelector("[data-space-news-delayed]");
    if (notice && Number.isFinite(updated)) {
      notice.hidden = Date.now() - updated < 36 * 60 * 60 * 1000;
    }
  });
});
