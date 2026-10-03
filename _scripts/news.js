/* Keep NEW labels current even when a cached static page is viewed later. */
{
  const updateNewBadges = () => {
    const now = Date.now();
    document.querySelectorAll(".news-new-badge").forEach((badge) => {
      const published = Date.parse(badge.dataset.publishedAt);
      const days = Number(badge.dataset.newDays);
      const age = now - published;
      badge.hidden = !(
        Number.isFinite(published) &&
        Number.isFinite(days) &&
        days > 0 &&
        age >= 0 &&
        age < days * 86400000
      );
    });
  };

  document.addEventListener("DOMContentLoaded", () => {
    updateNewBadges();
    if (document.querySelector(".news-new-badge")) {
      window.setInterval(updateNewBadges, 60000);
    }
  });
  window.addEventListener("pageshow", updateNewBadges);
  document.addEventListener("visibilitychange", () => {
    if (!document.hidden) updateNewBadges();
  });
}
