"""Collect public research outputs; publish identity-confirmed metadata only.

No logins, API keys, full papers, patent claims, or personal registration fields.
Source failures retain the previous snapshot. Uncertain ownership goes to review.
"""
from __future__ import annotations

import argparse
from datetime import date, datetime, timezone
import hashlib
import html
import json
from pathlib import Path
import re
import subprocess
import unicodedata
from urllib.parse import quote, urlencode, urljoin, urlsplit
from zoneinfo import ZoneInfo

from bs4 import BeautifulSoup
import yaml

ROOT = Path(__file__).resolve().parents[1]
CURATED = ("legacy-publications", "discovered-publications", "ip-publications", "accepted-publications")
CROSSREF = "https://api.crossref.org/works"
CROS = "https://www.cros.or.kr/psnsys/cmmn/wisenut/search.do"
PUBLIC_FIELDS = {
    "id", "title", "authors", "category", "subtype", "doi", "link", "date", "year",
    "publisher", "details", "details_en", "status", "scope", "country",
    "application_number", "application_date", "registration_number", "registration_date",
    "copyright_author", "contributor_role", "applicant", "inventors", "year_basis", "publication_number",
    "source", "verification_source", "_source", "_target", "_identity", "_source_id",
}


def clean(value):
    return " ".join(BeautifulSoup(str(value or ""), "html.parser").get_text(" ").split())


def norm(value):
    return re.sub(r"[^\w]", "", unicodedata.normalize("NFKC", str(value or "")).lower())


def safe_record(record):
    # Explicit allowlist: source JSON can contain IDs, addresses and access codes.
    return {k: v for k, v in record.items() if k in PUBLIC_FIELDS and v not in (None, "", [])}


def load_yaml(path):
    return yaml.safe_load(path.read_text()) or [] if path.exists() else []


def known_key(record):
    return record.get("audit_key") or record.get("id")


def doi(record):
    value = record.get("doi") or record.get("id", "")
    value = re.sub(r"^(doi:|https?://(?:dx\.)?doi\.org/)", "", value, flags=re.I)
    return value.lower() if re.match(r"^10\.\d{4,9}/\S+$", value) else ""


def titles(record):
    return {norm(t) for t in [record.get("title", ""), *record.get("title_aliases", [])] if t}


def country(record):
    if record.get("country"):
        return record["country"]
    text = record.get("registration_number", "") + " " + record.get("link", "")
    match = re.search(r"(?:patent/|^)(US|KR|JP|EP|WO)\d", text)
    if match:
        return match[1]
    if re.match(r"(?:10|20|30|40)-", record.get("application_number", "")):
        return "KR"
    return ""


def number(value):
    return re.sub(r"[^0-9]", "", value or "")


def same_record(left, right):
    if left.get("category") != right.get("category"):
        return False
    if doi(left) and doi(right):
        return doi(left) == doi(right)
    if left.get("category") in ("patent", "intellectual-property"):
        if not country(left) or country(left) != country(right):
            return False
        return any(number(left.get(k)) and number(left.get(k)) == number(right.get(k))
                   for k in ("application_number", "registration_number"))
    if left.get("category") == "software":
        if left.get("registration_number") and right.get("registration_number"):
            return norm(left["registration_number"]) == norm(right["registration_number"])
        return bool(titles(left) & titles(right)) and norm(right.get("copyright_author")) == norm("한국항공우주연구원")
    if left.get("year") and right.get("year") and int(left["year"]) != int(right["year"]):
        return False
    return bool(titles(left) & titles(right))


class Client:
    def __init__(self, limit=160):
        self.limit, self.count, self.cache = limit, 0, {}
        self.warnings = []

    def get(self, url, body=None, post=False):
        key = (url, json.dumps(body, sort_keys=True), post)
        if key in self.cache:
            return self.cache[key]
        self.count += 1
        if self.count > self.limit:
            raise RuntimeError("Request budget reached")
        args = ["curl", "--fail", "--silent", "--show-error", "--location", "--max-time", "30",
                "--retry", "1", "--retry-all-errors", "--retry-delay", "2", "--retry-max-time", "35",
                "--user-agent", "SEARCH-Lab-Publications/1.0 (+https://ust-search-lab.github.io)", url]
        if body is not None:
            args += ["-H", "Content-Type: application/json", "--data", json.dumps(body)]
        elif post:
            args += ["-X", "POST", "--data", ""]
        result = subprocess.run(args, capture_output=True, timeout=70)
        if result.returncode:
            raise RuntimeError(f"Request failed ({urlsplit(url).netloc}, curl {result.returncode})")
        self.cache[key] = result.stdout
        return result.stdout

    def json(self, url, **kwargs):
        return json.loads(self.get(url, **kwargs))

    def optional_json(self, url, **kwargs):
        try:
            return self.json(url, **kwargs)
        except (RuntimeError, ValueError, subprocess.TimeoutExpired) as exc:
            self.warnings.append(str(exc)[:180])
            return None


def date_parts(work, today):
    for key in ("published-online", "published-print", "published"):
        parts = work.get(key, {}).get("date-parts", [[]])[0]
        if not parts:
            continue
        text = "-".join(str(n) if i == 0 else f"{n:02d}" for i, n in enumerate(parts))
        # Do not silently use a print date if the preferred online date is future.
        if text > today.isoformat()[:len(text)]:
            return None
        return text
    return None


def normalize_crossref(work, identity, today, known):
    kind = work.get("type")
    if kind not in ("journal-article", "proceedings-article"):
        return None
    published = date_parts(work, today)
    title = clean(next(iter(work.get("title", [])), ""))
    identifier = work.get("DOI", "").lower()
    if not published or not title or not re.match(r"^10\.\d{4,9}/\S+$", identifier):
        return None
    authors = work.get("author", [])
    aliases = {norm(n) for n in identity["names"]}
    people = [a for a in authors if norm(a.get("given", "") + " " + a.get("family", "")) in aliases]
    exact = [a for a in authors if a.get("ORCID", "").rstrip("/").endswith("/" + identity["orcid"])]
    if not people and not exact:
        return None
    # A conflicting ORCID on the named person rules out automatic attribution.
    if people and any(a.get("ORCID") and not a["ORCID"].endswith(identity["orcid"]) for a in people):
        return None
    affiliations = {norm(n) for n in identity["affiliations"]}
    affiliated = any(any(term in norm(aff.get("name")) for term in affiliations)
                     for a in people for aff in a.get("affiliation", []))
    venue = clean(next(iter(work.get("container-title", [])), work.get("publisher", "")))
    category = "conference" if kind == "proceedings-article" else "journal"
    detail = ", ".join(filter(None, [venue, str(work.get("volume", "")),
                                    f"No. {work['issue']}" if work.get("issue") else "",
                                    str(work.get("page") or work.get("article-number") or ""), published]))
    record = dict(id="doi:" + identifier, doi=identifier, title=title,
                  authors=[clean(a.get("given", "") + " " + a.get("family", "")) for a in authors],
                  category=category, date=published, year=int(published[:4]), publisher=venue,
                  details=detail, details_en=detail, status="published", link="https://doi.org/" + identifier,
                  _source="crossref", _source_id="doi:" + identifier,
                  verification_source=CROSSREF + "/" + quote(identifier, safe=""))
    known_match = any(same_record(r, record) for r in known if not r.get("exclude"))
    record["_identity"] = "confirmed" if exact or affiliated or known_match else "review"
    return record


def collect_crossref(client, settings, known, today):
    identity = settings["identity"]
    start = f"{today.year - settings['lookback_years']}-01-01"
    queries = [dict(filter="orcid:" + identity["orcid"], rows=100),
               {"query.author": '"Jae-ik Park"', "query.affiliation": "Korea Aerospace Research Institute",
                "filter": "from-pub-date:" + start, "rows": 100}]
    queries += [{"query.title": r["title"], "query.author": "Jae-ik Park", "rows": 3}
                for r in known if r.get("status") == "accepted"]
    results, successes = {}, 0
    for query in queries:
        response = client.optional_json(CROSSREF + "?" + urlencode(query))
        if response is None:
            continue
        message = response.get("message", {})
        if not isinstance(message.get("items"), list):
            raise ValueError("Crossref response schema changed")
        successes += 1
        for work in message["items"]:
            record = normalize_crossref(work, identity, today, known)
            if record:
                results[record["id"]] = record
    if not successes:
        raise RuntimeError("All Crossref queries failed")
    return list(results.values())


def soup_bytes(raw):
    # The society proceedings use EUC-KR, including their search query encoding.
    head = raw[:3000].lower()
    encoding = "cp949" if b"euc-kr" in head or b"ks_c_5601" in head else "utf-8"
    return BeautifulSoup(raw.decode(encoding, errors="replace"), "html.parser")


def normalize_program(card, root, venue, today, session):
    heading, people = card.select_one(".papertitle"), card.select_one(".authors")
    if not heading or not people:
        return None
    author_text = people.get_text(" ", strip=True)
    groups = re.findall(r"([^()]+)\(([^()]*)\)", author_text)
    confirmed = any("박재익" in [x.strip() for x in names.split(",")] and
                    "한국항공우주연구원" in affiliation for names, affiliation in groups)
    if "박재익" not in author_text:
        return None
    authors = [n.strip() for n in re.sub(r"\([^()]*\)", "", author_text).split(",") if n.strip()]
    title = re.sub(r"^\[\d+\]\s*", "", heading.get_text(" ", strip=True)).strip()
    year = int(re.search(r"/proceedings/(\d{4})", root)[1])
    session_date = session.select_one(".s_date")
    match = re.search(r"(\d+)월\s*(\d+)일", session_date.get_text() if session_date else "")
    if not match:
        return None
    published = date(year, int(match[1]), int(match[2]))
    if published > today:
        return None
    code = card.select_one(".roomnumber")
    code = code.get_text(" ", strip=True) if code else ""
    uid = "program:" + hashlib.sha256((root + title).encode()).hexdigest()[:20]
    return dict(id=uid, title=title, authors=authors, category="conference", scope="domestic",
                date=published.isoformat(), year=year, publisher=venue,
                details=f"{venue} 학술대회, {published.isoformat()}, {code} (공개 프로그램)",
                details_en=f"{venue}, {published.isoformat()}, {code} (public conference program)",
                _source_id=uid, _identity="confirmed" if confirmed else "review")


def collect_society(client, settings, known, today, site):
    roots = set()
    host = urlsplit(site["home"]).netloc
    pattern = r"(?:https?://[^\s\"'<>]+)?/proceedings/(\d{4})[a-z]+/"
    # Known public programs bootstrap discovery; event listings find new editions.
    texts = [str(r.get("link", "")) + " " + " ".join(r.get("verification_sources", [])) for r in known]
    landing = []
    for url in (site["home"], site["listing"]):
        page = soup_bytes(client.get(url))
        texts.append(str(page))
        landing += [urljoin(url, a["href"]) for a in page.select('a[href*="ConferenceView.asp"]')][:8]
    for url in sorted(set(landing))[:8]:
        texts.append(str(soup_bytes(client.get(url))))
    for text in texts:
        for m in re.finditer(pattern, html.unescape(text)):
            root = urljoin(site["home"], m[0])
            if urlsplit(root).netloc == host and today.year - settings["lookback_years"] <= int(m[1]) <= today.year:
                roots.add(root)
    if not roots:
        raise ValueError("No public proceedings links found")
    results = []
    for root in sorted(roots):
        page = soup_bytes(client.get(root + "SessionSearch.asp?" + urlencode({"SrchText": "박재익"}, encoding="cp949")))
        if not page.select(".paperinfo") and "검색된 정보가 없습니다" not in page.get_text():
            raise ValueError("Conference search response schema changed")
        for card in page.select(".paperinfo"):
            match = re.search(r"popSessionView\.asp\?code=(\d+)", str(card))
            if not match:
                continue
            link = root + "SessionPaperList.asp?code=" + match[1]
            session = soup_bytes(client.get(link))
            record = normalize_program(card, root, site["name"], today, session)
            if record:
                record.update(link=link, verification_source=link, _source=site["id"])
                results.append(record)
    return results


def patent_field(page, field):
    e = page.select_one('[itemprop="' + field + '"]')
    return (e.get("content") or e.get_text(" ", strip=True)) if e else ""


def normalize_patent(raw, identity, today):
    page = soup_bytes(raw)
    publication = patent_field(page, "publicationNumber")
    nation = patent_field(page, "countryCode")
    application = patent_field(page, "applicationNumber")
    filing = patent_field(page, "filingDate")
    published = patent_field(page, "publicationDate")
    inventors = [e.get_text(" ", strip=True) for e in page.select('[itemprop="inventor"]')]
    applicant = patent_field(page, "assigneeOriginal")
    if not publication or not application or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", filing):
        raise ValueError("Patent bibliographic fields missing")
    if not published or published > today.isoformat():
        return None
    aliases = {norm(n) for n in identity["names"]}
    if not any(norm(n) in aliases for n in inventors):
        return None
    confirmed = any(norm(n) in norm(applicant) for n in identity["affiliations"])
    granted = patent_field(page, "kindCode").startswith("B")
    link = "https://patents.google.com/patent/" + publication + "/en"
    record = dict(id="patent:" + publication, title=patent_field(page, "title"), authors=inventors,
                  inventors=inventors, category="patent", country=nation, applicant=applicant,
                  application_number=application, application_date=filing, year=int(filing[:4]),
                  year_basis="application_year", publication_number=publication,
                  status="registered" if granted else "application", link=link,
                  scope="domestic" if nation == "KR" else "international", _source="patents",
                  _source_id="patent:" + publication, _identity="confirmed" if confirmed else "review",
                  verification_source=link)
    if nation == "KR" and len(number(application)) == 13:
        n = number(application)
        record["application_number"] = f"{n[:2]}-{n[2:6]}-{n[6:]}"
    if granted:
        registration = publication
        if nation == "KR":
            match = re.fullmatch(r"KR(\d{2})(\d{7})B\d?", publication)
            if match:
                registration = match[1] + "-" + match[2]
        record["registration_number"] = registration
        # Grant and publication dates may differ. Use the explicit grant event.
        grant_dates = [patent_field(e, "date") for e in page.select('[itemprop="events"]')
                       if patent_field(e, "type") == "granted"]
        if grant_dates and re.fullmatch(r"\d{4}-\d{2}-\d{2}", grant_dates[0]) and grant_dates[0] <= today.isoformat():
            record["registration_date"] = grant_dates[0]
    record["details"] = f"출원 {record['application_number']} ({filing})"
    record["details_en"] = f"Application {record['application_number']} ({filing})"
    if granted:
        suffix = " (" + record["registration_date"] + ")" if record.get("registration_date") else ""
        record["details"] += "; 등록 " + record["registration_number"] + suffix
        record["details_en"] += "; Grant " + record["registration_number"] + suffix
    return record


def collect_patents(client, settings, known, today):
    identifiers = set()
    for inventor, applicant in [("박재익", "한국항공우주연구원"), ("Jae Ik Park", "Korea Aerospace Research Institute")]:
        query = urlencode({"inventor": inventor, "assignee": applicant, "num": 100})
        result = client.json("https://patents.google.com/xhr/query?" + urlencode({"url": query, "exp": ""})).get("results", {})
        if "total_num_results" not in result:
            raise ValueError("Patent search response schema changed")
        if int(result.get("total_num_pages", 1)) > 1:
            raise ValueError("Patent search exceeds configured single-page coverage")
        for group in result.get("cluster", []):
            for item in group.get("result", []):
                if item.get("patent", {}).get("publication_number"):
                    identifiers.add(item["patent"]["publication_number"])
    for record in known:
        if record.get("category") == "patent" and not record.get("exclude"):
            m = re.search(r"patents\.google\.com/patent/([^/]+)", record.get("link", ""))
            if m:
                identifiers.add(m[1])
    results = []
    for identifier in sorted(identifiers):
        raw = client.get("https://patents.google.com/patent/" + quote(identifier, safe="") + "/en")
        record = normalize_patent(raw, settings["identity"], today)
        if record:
            results.append(record)
            # Search can still return the A publication after a B grant appears.
            # Only follow direct same-country publications of the same application.
            if record["status"] == "application":
                page = soup_bytes(raw)
                for node in page.select('[itemprop="directAssociations"] [itemprop="publicationNumber"]'):
                    other = node.get_text(" ", strip=True)
                    if re.fullmatch(re.escape(record["country"]) + r"\d+B\d?", other) and other not in identifiers:
                        grant = normalize_patent(client.get("https://patents.google.com/patent/" + other + "/en"), settings["identity"], today)
                        if grant and same_record(record, grant):
                            results.append(grant)
    return results


def normalize_software(document, detail, today):
    regid = detail.get("regId", "")
    regdate = detail.get("regDt", "")
    title = clean(detail.get("contTitle"))
    author = clean(detail.get("authorNm"))
    if (detail.get("rgdcKdCd") != "S" or detail.get("isOpenYn") != "Y" or
            not re.fullmatch(r"[CS]-\d{4}-\d{6}", regid) or
            not re.fullmatch(r"\d{4}-\d{2}-\d{2}", regdate) or regdate > today.isoformat()):
        return None
    if not title or not author:
        return None
    link = "https://www.cros.or.kr/page.do?w2xPath=/ui/main/main.xml"
    return dict(id="software:" + regid, title=title, category="software", status="registered",
                registration_number=regid, registration_date=regdate, year=int(regdate[:4]),
                year_basis="registration_year", copyright_author=author,
                details=f"컴퓨터프로그램 저작권 등록 {regid}, 등록일 {regdate}",
                details_en=f"Computer program copyright registration {regid}, registered {regdate}",
                link=link, verification_source=CROS + "?" + urlencode({"query": regid, "collection": "reg_copyright"}),
                _source="cros", _source_id="software:" + regid, _identity="review")


def collect_software(client, settings, known, today):
    # Institution-only new registrations remain candidates: corporate ownership
    # does not establish this lab's participation or individual authorship.
    def search(query, start=1):
        url = CROS + "?" + urlencode(dict(query=query, sort="SYS_ID", sortOrder="DESC", startCount=start,
                                         listCount=100, TOTALVIEWCOUNT=100, collection="reg_copyright"))
        result = client.json(url, post=True)
        if not isinstance(result.get("document"), list):
            raise ValueError("CROS search response schema changed")
        return result
    docs = {}
    for record in known:
        if record.get("category") == "software" and not record.get("exclude"):
            query = record.get("registration_number") or record["title"]
            for doc in search(query)["document"]:
                docs[doc["SYS_ID"]] = doc
    # Bounded recent discovery: up to 400 institution records, detailed only if relevant.
    for start in (1, 101, 201, 301):
        result = search("한국항공우주연구원", start)
        for doc in result["document"]:
            if any(norm(k) in norm(doc.get("CONT_TITLE")) for k in settings["software_keywords"]):
                docs[doc["SYS_ID"]] = doc
        if not result["document"] or start + 99 >= int(result["TotalCount"]):
            break
        years = [int(d["REG_ID"].split("-")[1]) for d in result["document"] if re.fullmatch(r"[CS]-\d{4}-\d{6}", d.get("REG_ID", ""))]
        if years and max(years) < today.year - settings["lookback_years"]:
            break
    results = []
    for doc in docs.values():
        if doc.get("RGDC_KD_CD") != "S" or doc.get("isopenyn") != "Y":
            continue
        body = {"dm_regDtlSchMap": {"sysId": doc["SYS_ID"], "regId": doc["REG_ID"], "rgdcKdCd": "S"}}
        data = client.json("https://www.cros.or.kr/req/reg/selectRegDtlList3.do", body=body)
        if not isinstance(data.get("dl_regDtlList"), list):
            raise ValueError("CROS detail response schema changed")
        for item in data["dl_regDtlList"]:
            if item.get("regId") != doc["REG_ID"]:
                continue
            record = normalize_software(doc, item, today)
            if record:
                results.append(record)
                break
    return results


def update_patch(old, new):
    """Only add verified facts or advance publication/grant status; never erase curation."""
    fields = ("doi", "date", "year", "publisher", "application_number", "application_date",
              "registration_number", "registration_date", "copyright_author", "year_basis", "country")
    patch = {k: new[k] for k in fields if new.get(k) and not old.get(k)}
    published = old.get("status") == "accepted" and new.get("status") == "published"
    granted = old.get("status") in ("application", "unknown", None) and new.get("status") == "registered"
    if published or granted:
        patch.update({k: new[k] for k in ("status", "details", "details_en", "link") if new.get(k)})
    if published:
        patch.update({k: new[k] for k in ("year", "date", "doi", "publisher") if new.get(k)})
    if "doi" in patch:
        patch.update(id="doi:" + patch["doi"], link="https://doi.org/" + patch["doi"])
    if old.get("category") == "software" and any(k in patch for k in ("registration_number", "registration_date")):
        patch.update({k: new[k] for k in ("status", "details", "details_en", "year", "year_basis") if new.get(k)})
    if old.get("category") == "software" and old.get("year_basis") == "internal_reference_year" and new.get("registration_date"):
        patch.update({k: new[k] for k in ("status", "details", "details_en", "year", "year_basis") if new.get(k)})
    if old.get("category") == "software" and old.get("authors") and new.get("copyright_author") and not old.get("contributor_role"):
        patch["contributor_role"] = "research_contributor"
    return patch


def reconcile(incoming, known, previous, settings):
    updates = {r["_source_id"]: r for r in previous}
    candidates = {}
    approved, excluded = set(settings["approved_source_ids"]), set(settings["excluded_source_ids"])
    for record in incoming:
        record = safe_record(record)
        uid = record["_source_id"]
        if uid in excluded or any(r.get("exclude") and same_record(r, record) for r in known):
            updates.pop(uid, None)
            continue
        matches = [r for r in known if not r.get("exclude") and same_record(r, record)]
        if len(matches) > 1:
            record["reason"] = "Multiple curated matches"
            candidates[uid] = record
            continue
        if matches:
            match = matches[0]
            if record["category"] == "software" and norm(record.get("copyright_author")) != norm(match.get("copyright_author") or "한국항공우주연구원"):
                record["reason"] = "Software owner differs"
                candidates[uid] = record
                continue
            patch = update_patch(match, record)
            if not patch:
                updates.pop(uid, None)
                continue
            record = {**patch, "_target": known_key(match), "_source_id": uid,
                      "_source": record["_source"], "verification_source": record["verification_source"],
                      "_identity": "confirmed", "category": record["category"], "title": record["title"]}
        # A same-title foreign family member must not replace or expand a curated patent.
        elif record["category"] == "patent" and any(titles(r) & titles(record) for r in known):
            record["_identity"] = "review"
        elif record["category"] == "patent" and any(r.get("exclude") and r.get("category") == "patent" and
                                                     r.get("year") == record.get("year") for r in known):
            # An excluded filing without a public number cannot be conclusively
            # ruled out by an English translation of its title alone.
            record["_identity"] = "review"
        if record.get("_identity") == "confirmed" or uid in approved:
            updates[uid] = {**updates.get(uid, {}), **record}
        else:
            record["reason"] = "Confirm individual participation / author identity"
            candidates[uid] = record
    # Explicit exclusions also apply to records preserved from an earlier run.
    records = [r for uid, r in updates.items() if uid not in excluded and not any(
        k.get("exclude") and same_record(k, r) for k in known)]
    # New, automatically discovered applications and their later grants represent
    # one work even when the public document identifier changes from A to B.
    combined = []
    ranks = {"registered": 2, "published": 2, "application": 1}
    for record in records:
        index = next((i for i, other in enumerate(combined) if not other.get("_target") and
                      not record.get("_target") and same_record(other, record)), None)
        if index is None:
            combined.append(record)
        else:
            old = combined[index]
            better = ranks.get(record.get("status"), 0) >= ranks.get(old.get("status"), 0)
            combined[index] = {**old, **record} if better else {**record, **old}
    return sorted(combined, key=lambda r: r["_source_id"]), sorted(candidates.values(), key=lambda r: r["_source_id"])


def atomic_write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(text, encoding="utf-8")
    temp.replace(path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=ROOT)
    args = parser.parse_args()
    settings = json.loads((ROOT / "_data/publication-automation.json").read_text())
    known = [r for name in CURATED for r in load_yaml(ROOT / f"_data/{name}.yaml")]
    previous = load_yaml(ROOT / "_data/auto-publications.yaml")
    today = datetime.now(ZoneInfo("Asia/Seoul")).date()
    client = Client(settings["max_requests"])
    collectors = [("crossref", lambda: collect_crossref(client, settings, known, today)),
                  *[(s["id"], lambda s=s: collect_society(client, settings, known, today, s)) for s in settings["conference_sites"]],
                  ("patents", lambda: collect_patents(client, settings, known, today)),
                  ("cros", lambda: collect_software(client, settings, known, today))]
    incoming, coverage = [], []
    for name, collect in collectors:
        print(f"Collecting {name}...", flush=True)
        client.warnings = []
        try:
            records = collect()
            incoming.extend(records)
            coverage.append(dict(source=name, status="partial" if client.warnings else "ok",
                                 records=len(records), warnings=client.warnings[:10]))
            print(f"  {len(records)} records", flush=True)
        except Exception as exc:
            coverage.append(dict(source=name, status="failed", error=str(exc)[:180]))
            print(f"  Failed: {exc}", flush=True)
    if not any(c["status"] in ("ok", "partial") for c in coverage):
        raise RuntimeError("All sources failed; previous files preserved")
    records, candidates = reconcile(incoming, known, previous, settings)
    report = dict(checked_at=datetime.now(timezone.utc).isoformat(), coverage=coverage,
                  requests=client.count, automatic_records=len(records), candidates=candidates,
                  limitations=["Public sources only; not an exhaustive inventory.",
                               "Conference programs verify listings, not attendance.",
                               "Google Patents bibliographic grant facts do not establish current legal validity.",
                               "Corporate software ownership does not establish individual participation.",
                               "Unpublished filings and login-only databases are not collected.",
                               "Trademark/design discovery is not connected; curated entries are retained."])
    atomic_write(args.output_dir / "_data/auto-publications.yaml", "# Generated by _publications/update.py\n" + yaml.safe_dump(records, allow_unicode=True, sort_keys=False))
    atomic_write(args.output_dir / "_publications/review.json", json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(f"Saved {len(records)} automatic records and {len(candidates)} review candidates", flush=True)


if __name__ == "__main__":
    main()
