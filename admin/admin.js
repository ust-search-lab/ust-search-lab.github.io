(async () => {
  const status = document.getElementById("cms-status");
  const message = document.getElementById("cms-message");
  try {
    const response = await fetch("./settings.json", { cache: "no-store" });
    if (!response.ok) throw new Error("설정 파일을 불러오지 못했습니다.");
    const settings = await response.json();
    if (!settings.auth_base_url) {
      message.textContent = "최초 연결 설정이 필요합니다.";
      document.getElementById("cms-setup").hidden = false;
      return;
    }
    const authUrl = new URL(settings.auth_base_url);
    if (authUrl.protocol !== "https:" || authUrl.username || authUrl.password || authUrl.search || authUrl.hash || authUrl.pathname !== "/") {
      throw new Error("인증 서비스 주소는 https://로 시작하는 호스트 주소로 설정해 주세요.");
    }
    if (!window.CMS) throw new Error("Decap CMS를 불러오지 못했습니다. 인터넷 연결을 확인하고 새로고침해 주세요.");

    window.registerPublicationArchive(settings.publication_visibility);

    CMS.registerEventListener({
      name: "preSave",
      handler: ({ entry }) => {
        if (entry.get("collection") === "publication_archive") {
          throw new Error("숨긴 실적은 조회 전용입니다. 원본 실적은 변경되지 않습니다.");
        }
        const data = entry.get("data");
        const rows = (data.get("items") || data.get("courses") || data.get("albums"))?.toJS() || [];
        const ids = new Set();
        for (const row of rows) {
          if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(row.id) || ids.has(row.id)) {
            throw new Error("각 항목의 ID는 중복 없이 영문 소문자·숫자·하이픈으로 입력해 주세요.");
          }
          ids.add(row.id);
          const weeks = new Set();
          for (const week of row.weeks || []) {
            if (weeks.has(week.number)) throw new Error("같은 과목에 주차 번호가 중복되어 있습니다.");
            weeks.add(week.number);
          }
        }
        return data;
      },
    });
    CMS.init({ config: { backend: { base_url: authUrl.origin, auth_endpoint: "auth" } } });
    status.hidden = true;
  } catch (error) {
    message.textContent = error.message || "관리자 화면을 불러오지 못했습니다.";
  }
})();
