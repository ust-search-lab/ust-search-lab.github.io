// Enhance the server-rendered resource list; downloads also work without JavaScript.
window.addEventListener("DOMContentLoaded", () => {
  const library = document.querySelector("[data-library]");
  if (!library) return;
  const controls = library.querySelector(".library-controls");
  if (!controls) return;
  const search = library.querySelector("[data-library-search]");
  const category = library.querySelector("[data-library-category]");
  const items = [...library.querySelectorAll("[data-library-item]")];
  const count = library.querySelector("[data-library-count]");
  const empty = library.querySelector("[data-library-no-results]");
  const normalize = (value) => value.normalize("NFKC").toLocaleLowerCase().trim();
  const update = () => {
    const terms = normalize(search.value).split(/\s+/).filter(Boolean);
    let visible = 0;
    for (const item of items) {
      item.hidden = Boolean(
        (category.value && item.dataset.category !== category.value) ||
        !terms.every((term) => normalize(item.dataset.search).includes(term))
      );
      if (!item.hidden) visible++;
    }
    count.textContent = count.dataset.template.replace("$X", visible.toLocaleString());
    empty.hidden = visible !== 0;
  };
  controls.hidden = false;
  search.addEventListener("input", update);
  category.addEventListener("change", update);
  update();
});
