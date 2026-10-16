window.addEventListener("DOMContentLoaded", () => {
  for (const photo of document.querySelectorAll("[data-album-photo]")) {
    const button = photo.querySelector("[data-photo-copy]");
    const status = photo.querySelector("[data-photo-status]");
    const input = photo.querySelector("[data-photo-url]");
    button.hidden = false;
    button.addEventListener("click", async () => {
      const url = photo.querySelector("[data-photo-original]").href;
      try {
        await navigator.clipboard.writeText(url);
        status.textContent = status.dataset.success;
        input.hidden = true;
      } catch {
        status.textContent = status.dataset.fallback;
        input.value = url;
        input.hidden = false;
        input.focus();
        input.select();
      }
    });
  }
});
