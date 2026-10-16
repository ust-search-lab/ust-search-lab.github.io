// Loaded inside Decap's authenticated editor; bibliography is fetched by its
// GitHub backend, never embedded in public pages or copied to a public JSON feed.
window.registerPublicationArchive = function (policy) {
  const normalize = (name) => String(name || "").normalize("NFKC").toLowerCase().replace(/[^\p{L}\p{N}]/gu, "");
  const hidden = new Set((policy?.hidden_first_authors || []).map(normalize).filter(Boolean));
  const h = window.h;
  if (!window.jsyaml || !h) throw new Error("실적 조회 도구를 불러오지 못했습니다. 새로고침해 주세요.");

  CMS.registerCustomFormat("publication-archive", "yaml", {
    fromFile(text) {
      const records = jsyaml.load(text, { schema: jsyaml.JSON_SCHEMA });
      if (!Array.isArray(records)) throw new Error("실적 목록 형식이 올바르지 않습니다.");
      return { records };
    },
    toFile() {
      throw new Error("숨긴 실적은 조회 전용입니다. 원본 실적은 변경되지 않습니다.");
    },
  });

  const Archive = window.createClass({
    render() {
      const records = this.props.value?.toJS?.();
      if (!Array.isArray(records)) {
        return h("p", { role: "alert" }, "실적 목록을 읽지 못했습니다. 새로고침한 뒤 다시 열어 주세요.");
      }
      const matches = records.filter((record) => !record.exclude && hidden.has(normalize(record.authors?.[0])))
        .sort((a, b) => Number(b.year || String(b.date || "").slice(0, 4)) - Number(a.year || String(a.date || "").slice(0, 4)));
      return h("div", { id: this.props.forID, className: "publication-archive" },
        h("p", { className: "publication-archive-note" }, "공개 화면에서 숨긴 실적을 조회합니다. 원본은 보존되며 이 화면에서는 수정하지 않습니다."),
        h("p", { role: "status" }, `이 목록에서 숨긴 실적 ${matches.length}건`),
        ...matches.map((record, index) => {
          const href = record.link || (record.doi ? `https://doi.org/${record.doi}` : "");
          const safeLink = /^https:\/\//i.test(href);
          return h("article", { key: record.id || record.audit_key || index },
            h("p", { className: "publication-archive-meta" }, `${record.year || String(record.date || "").slice(0, 4)} · ${record.category === "conference" ? "학술대회" : "논문"}`),
            h("h3", {}, record.title),
            h("p", {}, (record.authors || []).join(", ")),
            h("p", {}, record.details || record.publisher || ""),
            safeLink ? h("a", { href, target: "_blank", rel: "noopener noreferrer" }, "원문·출처 보기 ↗") : null);
        }),
        matches.length ? null : h("p", {}, "현재 이 목록에는 해당 첫 저자의 실적이 없습니다."));
    },
  });
  CMS.registerWidget("publication-archive", Archive);
};
