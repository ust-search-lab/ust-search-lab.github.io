// Progressive enhancements for the student guide only.
window.addEventListener("DOMContentLoaded", () => {
  const guide = document.querySelector('main[data-page="ai-coding-guide"]');
  if (!guide) return;
  const korean = document.documentElement.lang.startsWith("ko");

  // Open the OS panel before the shared heading-navigation code scrolls to it.
  const revealTarget = () => {
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)); }
    catch { return; }
    const target = document.getElementById(id);
    if (!target || !guide.contains(target)) return;
    let panel = target.closest("details");
    while (panel) {
      panel.open = true;
      panel = panel.parentElement.closest("details");
    }
  };
  revealTarget();
  window.addEventListener("hashchange", revealTarget, { capture: true });
  guide.querySelectorAll('a[href^="#"]').forEach((link) => {
    link.addEventListener("click", () => {
      const panel = document.getElementById(link.hash.slice(1));
      if (panel && panel.matches("details")) panel.open = true;
    });
  });

  if (navigator.clipboard?.writeText) {
    guide.querySelectorAll("div.highlighter-rouge").forEach((block) => {
      const code = block.querySelector("pre");
      if (!code) return;
      const wrapper = document.createElement("div");
      wrapper.className = "guide-codeblock";
      block.before(wrapper);
      wrapper.append(block);
      const button = document.createElement("button");
      button.type = "button";
      button.className = "guide-copy";
      const label = korean ? "복사" : "Copy";
      button.textContent = label;
      button.setAttribute("aria-label", korean ? "이 코드 블록 복사" : "Copy this code block");
      button.setAttribute("aria-live", "polite");
      let resetTimer;
      button.addEventListener("click", async () => {
        clearTimeout(resetTimer);
        try {
          await navigator.clipboard.writeText(code.textContent.trimEnd() + "\n");
          button.textContent = korean ? "복사됨" : "Copied";
        } catch {
          button.textContent = korean ? "직접 선택해 복사" : "Select text to copy";
        }
        resetTimer = setTimeout(() => { button.textContent = label; }, 2500);
      });
      wrapper.prepend(button);
    });
  }

  // Print all operating systems and reference code, then restore reading state.
  let readingState = null;
  const expandForPrint = () => {
    if (readingState) return;
    readingState = Array.from(guide.querySelectorAll("details"), (panel) => [panel, panel.open]);
    readingState.forEach(([panel]) => { panel.open = true; });
  };
  const restoreAfterPrint = () => {
    readingState?.forEach(([panel, open]) => { panel.open = open; });
    readingState = null;
  };
  window.addEventListener("beforeprint", expandForPrint);
  window.addEventListener("afterprint", restoreAfterPrint);
  const printButton = guide.querySelector("[data-guide-print]");
  printButton.hidden = false;
  printButton.addEventListener("click", () => window.print());
});
