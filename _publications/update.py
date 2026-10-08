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
CURATED = ("legacy-publications", "discovered-publications", "ip-publications", "accepted-publications",
           "under-review-publications", "collaborator-publications-oh", "collaborator-publications-bae")
CROSSREF = "https://api.crossref.org/works"
ORCID = "https://pub.orcid.org/v3.0"
CROS = "https://www.cros.or.kr/psnsys/cmmn/wisenut/search.do"
PUBLIC_FIELDS = {
    "id", "title", "authors", "category", "subtype", "doi", "link", "date", "year",
    "publisher", "details", "details_en", "status", "scope", "country",
    "application_number", "application_date", "registration_number", "registration_date",
    "copyright_author", "contributor_role", "applicant", "inventors", "year_basis", "publication_number",
    "source", "verification_source", "verification_sources", "researcher_ids", "_source", "_target", "_identity", "_source_id",
}

LEGACY_IDENTITY = {"id": "jae-ik-park", "names": ["Jae-ik Park", "Jae Ik Park", "박재익"],
                   "orcid": "0000-0001-6227-0442",
                   "affiliations": ["Korea Aerospace Research Institute", "한국항공우주연구원"]}


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


def researcher_id(identity):
    return identity.get("id", "jae-ik-park")


def identity_on_record(record, identity):
    """Curated participation is authoritative; a title alone proves no coauthorship."""
    if record.get("researcher_ids"):
        return researcher_id(identity) in record["researcher_ids"]
    aliases = {norm(n) for n in identity["names"]}
    return any(norm(n) in aliases for n in record.get("inventors", record.get("authors", [])))


def merge_record(old, new):
    ranks = {"registered": 2, "published": 2, "application": 1, "accepted": 1, "under_review": 0}
    older_is_further = (old.get("status") and new.get("status") and
                        ranks.get(old["status"], 0) > ranks.get(new["status"], 0))
    result = {**new, **old} if older_is_further else {**old, **new}
    for field in ("researcher_ids", "verification_sources"):
        values = sorted(set(old.get(field, []) + new.get(field, [])))
        if values:
            result[field] = values
    return result


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


def proceedings_roots(record):
    urls = [record.get("link", ""), record.get("verification_source", ""), *record.get("verification_sources", [])]
    roots = set()
    for value in urls:
        match = re.search(r"https?://(?:www\.)?([^/]+)(/proceedings/\d{4}[a-z]+/)", str(value), re.I)
        if match:
            roots.add((match[1] + match[2]).lower())
    return roots


def same_record(left, right):
    if left.get("category") != right.get("category"):
        return False
    if doi(left) and doi(right):
        return doi(left) == doi(right)
    if left.get("category") == "conference":
        lroots, rroots = proceedings_roots(left), proceedings_roots(right)
        if lroots and rroots and lroots.isdisjoint(rroots):
            return False
        ldate, rdate = str(left.get("date", "")), str(right.get("date", ""))
        if re.fullmatch(r"\d{4}(?:-\d{2}){0,2}", ldate) and re.fullmatch(r"\d{4}(?:-\d{2}){0,2}", rdate):
            precision = min(len(ldate), len(rdate))
            if ldate[:precision] != rdate[:precision]:
                return False
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
    def __init__(self, limit=160, cache=None):
        self.limit, self.count, self.cache = limit, 0, {} if cache is None else cache
        self.warnings = []

    def get(self, url, body=None, post=False):
        key = (url, json.dumps(body, sort_keys=True), post)
        if key in self.cache:
            return self.cache[key]
        if self.count >= self.limit:
            raise RuntimeError("Request budget reached")
        self.count += 1
        args = ["curl", "--fail", "--silent", "--show-error", "--location", "--max-time", "30",
                "--retry", "1", "--retry-all-errors", "--retry-delay", "2", "--retry-max-time", "35",
                "--user-agent", "SEARCH-Lab-Publications/1.0 (+https://ust-search-lab.github.io)", url]
        if url.startswith(ORCID + "/"):
            args += ["-H", "Accept: application/json"]
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


def normalize_crossref(work, identity, today, known, orcid_linked=False):
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
    affiliated = affiliated and identity.get("allow_affiliation_match", True)
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
    known_match = any(same_record(r, record) and identity_on_record(r, identity)
                      for r in known if not r.get("exclude"))
    correction = (re.match(r"^(correction|erratum|corrigendum|retraction)\b", title, re.I) or
                  work.get("subtype") in ("correction", "erratum", "retraction") or
                  work.get("relation", {}).get("is-correction-of") or
                  any(u.get("type") in ("correction", "erratum", "corrigendum", "retraction")
                      for u in work.get("update-to", [])))
    record["_identity"] = "confirmed" if (exact or affiliated or known_match or orcid_linked) and not correction else "review"
    record["researcher_ids"] = [researcher_id(identity)]
    return record


def collect_orcid(client, settings, known, today):
    """Resolve public career DOI works against Crossref; never invent missing authors."""
    identity = settings["identity"]
    url = ORCID + "/" + identity["orcid"] + "/works"
    response = client.json(url)
    if not isinstance(response.get("group"), list):
        raise ValueError("ORCID works response schema changed")
    identifiers = set()
    unsupported = 0
    for group in response["group"]:
        for work in group.get("work-summary", []):
            if str(work.get("visibility", "")).lower() != "public":
                continue
            if work.get("type") not in ("journal-article", "conference-paper", "conference-abstract", "conference-poster"):
                continue
            found = False
            for external in (work.get("external-ids") or {}).get("external-id", []):
                if external.get("external-id-type") != "doi" or external.get("external-id-relationship") != "self":
                    continue
                identifier = doi({"doi": external.get("external-id-value", "")})
                if identifier:
                    identifiers.add(identifier)
                    found = True
            if not found:
                unsupported += 1
    if unsupported:
        client.warnings.append(f"{unsupported} public ORCID journal/conference entries have no self DOI; manual source verification required")
    results = []
    # Always read career DOI entries: ORCID records can gain an older work at any time.
    for identifier in sorted(identifiers):
        response = client.optional_json(CROSSREF + "/" + quote(identifier, safe=""))
        if response is None:
            continue
        record = normalize_crossref(response.get("message", {}), identity, today, known, orcid_linked=True)
        if record:
            record["_source"] = "orcid-crossref"
            record["verification_sources"] = [url, record["verification_source"]]
            results.append(record)
    return results


def collect_crossref(client, settings, known, today):
    identity = settings["identity"]
    start = f"{settings.get('backfill_start_year', 1990) if settings.get('backfill') else today.year - settings['lookback_years']}-01-01"
    query_names = identity.get("query_names", [identity.get("query_name", identity["names"][0])])
    queries = [dict(filter="orcid:" + identity["orcid"], rows=100),
               *[{"query.author": '"' + name + '"', "filter": "from-pub-date:" + start, "rows": 100}
                 for name in query_names]]
    queries += [{"query.title": r["title"], "query.author": query_names[0], "rows": 3}
                for r in known if r.get("status") in ("accepted", "under_review") and identity_on_record(r, identity)]
    results, successes = {}, 0
    for query in queries:
        response = client.optional_json(CROSSREF + "?" + urlencode(query))
        if response is None:
            continue
        message = response.get("message", {})
        if not isinstance(message.get("items"), list):
            raise ValueError("Crossref response schema changed")
        successes += 1
        if message.get("total-results", 0) > len(message["items"]):
            client.warnings.append("Crossref query exceeds first-page coverage; use ORCID DOI discovery and curated backfill")
        for work in message["items"]:
            record = normalize_crossref(work, identity, today, known)
            if record:
                results[record["id"]] = merge_record(results.get(record["id"], {}), record)
    if not successes:
        raise RuntimeError("All Crossref queries failed")
    return list(results.values())


def soup_bytes(raw):
    # The society proceedings use EUC-KR, including their search query encoding.
    head = raw[:3000].lower()
    encoding = "cp949" if b"euc-kr" in head or b"ks_c_5601" in head else "utf-8"
    return BeautifulSoup(raw.decode(encoding, errors="replace"), "html.parser")


def normalize_program(card, root, venue, today, session, identity=None):
    identity = identity or LEGACY_IDENTITY
    heading, people = card.select_one(".papertitle"), card.select_one(".authors")
    if not heading or not people:
        return None
    author_text = people.get_text(" ", strip=True)
    groups = re.findall(r"([^()]+)\(([^()]*)\)", author_text)
    authors = [n.strip() for n in re.sub(r"\([^()]*\)", "", author_text).split(",") if n.strip()]
    aliases = {norm(n) for n in identity["names"]}
    if not any(norm(n) in aliases for n in authors):
        return None
    confirmed = any(any(norm(n.strip()) in aliases for n in names.split(",")) and
                    any(norm(a) in norm(affiliation) for a in identity["affiliations"])
                    for names, affiliation in groups)
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
                researcher_ids=[researcher_id(identity)],
                _source_id=uid, _identity="confirmed" if confirmed else "review")


def collect_society(client, settings, known, today, site):
    identity = settings["identity"]
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
            start_year = settings.get("backfill_start_year", 1990) if settings.get("backfill") else today.year - settings["lookback_years"]
            if urlsplit(root).netloc == host and start_year <= int(m[1]) <= today.year:
                roots.add(root)
    if not roots:
        raise ValueError("No public proceedings links found")
    results = []
    for root in sorted(roots, reverse=True):
        try:
            query = identity.get("conference_name", next(n for n in identity["names"] if re.search("[가-힣]", n)))
            page = soup_bytes(client.get(root + "SessionSearch.asp?" + urlencode({"SrchText": query}, encoding="cp949")))
            if not page.select(".paperinfo") and "검색된 정보가 없습니다" not in page.get_text():
                raise ValueError("Conference search response schema changed")
            for card in page.select(".paperinfo"):
                match = re.search(r"popSessionView\.asp\?code=(\d+)", str(card))
                if not match:
                    continue
                link = root + "SessionPaperList.asp?code=" + match[1]
                session = soup_bytes(client.get(link))
                record = normalize_program(card, root, site["name"], today, session, identity)
                if record:
                    record.update(link=link, verification_source=link, _source=site["id"])
                    results.append(record)
        except (RuntimeError, ValueError, subprocess.TimeoutExpired) as exc:
            client.warnings.append(str(exc)[:180])
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
    applicants = list(dict.fromkeys(clean(e.get("content") or e.get_text(" ", strip=True))
                                   for e in page.select('[itemprop="assigneeOriginal"]')))
    applicant = "; ".join(a for a in applicants if a)
    if not publication or not application or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", filing):
        raise ValueError("Patent bibliographic fields missing")
    if not published or published > today.isoformat():
        return None
    aliases = {norm(n) for n in identity["names"]}
    if not any(norm(n) in aliases for n in inventors):
        return None
    confirmed = identity.get("allow_affiliation_match", True) and any(norm(n) in norm(applicant) for n in identity["affiliations"])
    granted = patent_field(page, "kindCode").startswith("B")
    link = "https://patents.google.com/patent/" + publication + "/en"
    record = dict(id="patent:" + publication, title=patent_field(page, "title"), authors=inventors,
                  inventors=inventors, category="patent", country=nation, applicant=applicant,
                  application_number=application, application_date=filing, year=int(filing[:4]),
                  year_basis="application_year", publication_number=publication,
                  status="registered" if granted else "application", link=link,
                  scope="domestic" if nation == "KR" else "international", _source="patents",
                  _source_id="patent:" + publication, _identity="confirmed" if confirmed else "review",
                  verification_source=link, researcher_ids=[researcher_id(identity)])
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
        # KR Google "granted" events can report the B-publication date rather
        # than the registry's actual registration date (e.g. KR102685079B1).
        # Keep the grant number/status, but require primary-register/PDF curation
        # for Korean registration dates. Non-KR explicit grant events stay usable.
        grant_dates = [patent_field(e, "date") for e in page.select('[itemprop="events"]')
                       if patent_field(e, "type") == "granted"]
        if nation != "KR" and grant_dates and re.fullmatch(r"\d{4}-\d{2}-\d{2}", grant_dates[0]) and grant_dates[0] <= today.isoformat():
            record["registration_date"] = grant_dates[0]
    record["details"] = f"출원 {record['application_number']} ({filing})"
    record["details_en"] = f"Application {record['application_number']} ({filing})"
    if granted:
        suffix = " (" + record["registration_date"] + ")" if record.get("registration_date") else ""
        record["details"] += "; 등록 " + record["registration_number"] + suffix
        record["details_en"] += "; Grant " + record["registration_number"] + suffix
    return record


def collect_patents(client, settings, known, today):
    identity = settings["identity"]
    identifiers = set()
    successes = 0
    for inventor in identity.get("patent_names", identity["names"]):
        query = urlencode({"inventor": inventor, "num": 100})
        response = client.optional_json("https://patents.google.com/xhr/query?" + urlencode({"url": query, "exp": ""}))
        if response is None:
            continue
        result = response.get("results", {})
        if "total_num_results" not in result:
            client.warnings.append("Patent search response schema changed")
            continue
        successes += 1
        if int(result.get("total_num_pages", 1)) > 1:
            client.warnings.append("Patent search exceeds configured first-page coverage")
        for group in result.get("cluster", []):
            for item in group.get("result", []):
                if item.get("patent", {}).get("publication_number"):
                    identifiers.add(item["patent"]["publication_number"])
    for record in known:
        if record.get("category") == "patent" and not record.get("exclude") and identity_on_record(record, identity):
            m = re.search(r"patents\.google\.com/patent/([^/]+)", record.get("link", ""))
            if m:
                identifiers.add(m[1])
    results = []
    for identifier in sorted(identifiers):
        try:
            raw = client.get("https://patents.google.com/patent/" + quote(identifier, safe="") + "/en")
            record = normalize_patent(raw, identity, today)
            successes += 1
            if record:
                if any(not r.get("exclude") and same_record(r, record) and identity_on_record(r, identity) for r in known):
                    record["_identity"] = "confirmed"
                results.append(record)
                # Search can still return the A publication after a B grant appears.
                # Only follow direct same-country publications of the same application.
                if record["status"] == "application":
                    page = soup_bytes(raw)
                    for node in page.select('[itemprop="directAssociations"] [itemprop="publicationNumber"]'):
                        other = node.get_text(" ", strip=True)
                        if re.fullmatch(re.escape(record["country"]) + r"\d+B\d?", other) and other not in identifiers:
                            grant = normalize_patent(client.get("https://patents.google.com/patent/" + other + "/en"), identity, today)
                            if grant and same_record(record, grant):
                                results.append(grant)
        except (RuntimeError, ValueError, subprocess.TimeoutExpired) as exc:
            client.warnings.append(str(exc)[:180])
    if not successes:
        raise RuntimeError("All patent queries failed")
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
    successful_requests = 0
    def search(query, start=1):
        nonlocal successful_requests
        url = CROS + "?" + urlencode(dict(query=query, sort="SYS_ID", sortOrder="DESC", startCount=start,
                                         listCount=100, TOTALVIEWCOUNT=100, collection="reg_copyright"))
        result = client.optional_json(url, post=True)
        if result is None:
            return {"document": [], "TotalCount": 0}
        if not isinstance(result.get("document"), list):
            client.warnings.append("CROS search response schema changed")
            return {"document": [], "TotalCount": 0}
        successful_requests += 1
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
        data = client.optional_json("https://www.cros.or.kr/req/reg/selectRegDtlList3.do", body=body)
        if data is None:
            continue
        if not isinstance(data.get("dl_regDtlList"), list):
            client.warnings.append("CROS detail response schema changed")
            continue
        successful_requests += 1
        for item in data["dl_regDtlList"]:
            if item.get("regId") != doc["REG_ID"]:
                continue
            record = normalize_software(doc, item, today)
            if record:
                results.append(record)
                break
    if not successful_requests:
        raise RuntimeError("All CROS requests failed")
    return results


def update_patch(old, new):
    """Only add verified facts or advance publication/grant status; never erase curation."""
    fields = ("doi", "date", "year", "publisher", "application_number", "application_date",
              "registration_number", "registration_date", "copyright_author", "year_basis", "country")
    patch = {k: new[k] for k in fields if new.get(k) and not old.get(k)}
    people = sorted(set(old.get("researcher_ids", []) + new.get("researcher_ids", [])))
    if people and people != sorted(old.get("researcher_ids", [])):
        patch["researcher_ids"] = people
    published = old.get("status") in ("accepted", "under_review") and new.get("status") == "published"
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
    updates = {r["_source_id"]: dict(r) for r in previous}
    candidates = {}
    approved, excluded = set(settings["approved_source_ids"]), set(settings["excluded_source_ids"])
    for record in incoming:
        record = safe_record(record)
        uid = record["_source_id"]
        if uid in excluded or any(r.get("exclude") and same_record(r, record) for r in known):
            updates.pop(uid, None)
            continue
        matches = [r for r in known if not r.get("exclude") and same_record(r, record)]
        if len(matches) > 1 and not (doi(record) and all(doi(r) == doi(record) for r in matches)):
            record["reason"] = "Multiple curated matches"
            candidates[uid] = record
            continue
        if matches:
            match = matches[0]
            for other in matches[1:]:
                match = merge_record(other, match)
            if record["category"] == "software" and norm(record.get("copyright_author")) != norm(match.get("copyright_author") or "한국항공우주연구원"):
                record["reason"] = "Software owner differs"
                candidates[uid] = record
                continue
            if record.get("_identity") != "confirmed" and uid not in approved:
                # Matching a work does not confirm that another same-name researcher
                # participated in it. Software can inherit previously curated people.
                unknown_people = set(record.get("researcher_ids", [])) - set(match.get("researcher_ids", []))
                if unknown_people:
                    candidates[uid] = {**record, "reason": "Confirm additional participant identity"}
                record["researcher_ids"] = match.get("researcher_ids", [])
            patch = update_patch(match, record)
            if not patch:
                continue
            record = {**patch, "_target": known_key(match), "_source_id": uid,
                      "_source": record["_source"], "verification_source": record["verification_source"],
                      "_identity": "confirmed", "category": record["category"], "title": record["title"]}
            people = sorted(set(match.get("researcher_ids", []) + record.get("researcher_ids", [])))
            if people:
                record["researcher_ids"] = people
        # A same-title foreign family member must not replace or expand a curated patent.
        elif record["category"] == "patent" and any(titles(r) & titles(record) for r in known):
            record["_identity"] = "review"
        elif record["category"] == "patent" and any(r.get("exclude") and r.get("category") == "patent" and
                                                     r.get("year") == record.get("year") for r in known):
            # An excluded filing without a public number cannot be conclusively
            # ruled out by an English translation of its title alone.
            record["_identity"] = "review"
        if record.get("_identity") == "confirmed" or uid in approved:
            if not record.get("researcher_ids") and settings.get("researchers"):
                candidates[uid] = {**record, "reason": "Verified individual participant ids required"}
                continue
            updates[uid] = merge_record(updates.get(uid, {}), record)
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
        index = next((i for i, other in enumerate(combined)
                      if (record.get("_target") and record.get("_target") == other.get("_target")) or
                      (not other.get("_target") and not record.get("_target") and same_record(other, record))), None)
        if index is None:
            combined.append(record)
        else:
            old = combined[index]
            better = ranks.get(record.get("status"), 0) >= ranks.get(old.get("status"), 0)
            combined[index] = merge_record(old, record) if better else merge_record(record, old)
    return sorted(combined, key=lambda r: r["_source_id"]), sorted(candidates.values(), key=lambda r: r["_source_id"])


def atomic_write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(text, encoding="utf-8")
    temp.replace(path)


def prepare_known(settings):
    identities = settings["researchers"]
    known = [dict(r) for name in CURATED for r in load_yaml(ROOT / f"_data/{name}.yaml")]
    for record in known:
        if not record.get("researcher_ids"):
            record["researcher_ids"] = sorted(researcher_id(i) for i in identities if identity_on_record(record, i))
    return known


def migrate_previous(previous, known):
    """One-time attribution of the pre-multi-person, PI-only verified snapshot."""
    targets = {known_key(r): r for r in known}
    migrated = []
    for old in previous:
        record = dict(old)
        if not record.get("researcher_ids") and record.get("_identity") == "confirmed":
            target = targets.get(record.get("_target"), {})
            record["researcher_ids"] = target.get("researcher_ids") or ["jae-ik-park"]
        migrated.append(record)
    return migrated


def request_budgets(weights, maximum):
    if maximum < len(weights):
        raise ValueError("Request budget must reserve at least one request per collector")
    available = maximum - len(weights)
    budgets = [1 + available * weight // sum(weights) for weight in weights]
    for i in range(maximum - sum(budgets)):
        budgets[i % len(budgets)] += 1
    return budgets


def run_collectors(settings, known, today, researcher_filter=None, source_filter=None):
    people = [r for r in settings["researchers"] if not researcher_filter or r["id"] in researcher_filter]
    jobs = []
    for source in ("orcid", "crossref", *[s["id"] for s in settings["conference_sites"]], "patents"):
        if not source_filter or source in source_filter:
            jobs.extend((source, person) for person in people)
    if not source_filter or "cros" in source_filter:
        jobs.append(("cros", None))
    if not jobs:
        raise ValueError("No collectors selected")
    weights = settings.get("source_budget_weights", {})
    budgets = request_budgets([weights.get(source, 1) for source, _ in jobs], settings["max_requests"])
    incoming, coverage, cache = [], [], {}
    unused = 0
    for (source, person), budget in zip(jobs, budgets):
        # Reuse earlier unused requests while protecting every later reserved share.
        client = Client(budget + unused, cache)
        scoped = {**settings, "identity": person} if person else settings
        label = source + (" / " + person["id"] if person else "")
        print(f"Collecting {label}...", flush=True)
        row = dict(source=source, researcher_id=person["id"] if person else "shared", budget=budget,
                   available_requests=client.limit)
        try:
            if source == "orcid":
                records = collect_orcid(client, scoped, known, today)
            elif source == "crossref":
                records = collect_crossref(client, scoped, known, today)
            elif source == "patents":
                records = collect_patents(client, scoped, known, today)
            elif source == "cros":
                records = collect_software(client, scoped, known, today)
            else:
                site = next(s for s in settings["conference_sites"] if s["id"] == source)
                records = collect_society(client, scoped, known, today, site)
            incoming.extend(records)
            row.update(status="partial" if client.warnings else "ok", records=len(records), warnings=client.warnings[:10])
            print(f"  {len(records)} records", flush=True)
        except Exception as exc:
            row.update(status="failed", error=str(exc)[:180])
            print(f"  Failed: {exc}", flush=True)
        row["requests"] = client.count
        row["warnings"] = client.warnings[:10]
        unused += budget - client.count
        coverage.append(row)
    return incoming, coverage


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=ROOT)
    parser.add_argument("--backfill", action="store_true", help="Search public historical records as well as recent works")
    parser.add_argument("--researcher", action="append", help="Limit collection to a configured researcher id; may repeat")
    parser.add_argument("--source", action="append", help="Limit collection to a source id; may repeat")
    args = parser.parse_args()
    settings = json.loads((ROOT / "_data/publication-automation.json").read_text())
    settings["backfill"] = args.backfill
    if args.researcher and set(args.researcher) - {r["id"] for r in settings["researchers"]}:
        parser.error("Unknown researcher id")
    if args.source and set(args.source) - {"orcid", "crossref", "patents", "cros", *[s["id"] for s in settings["conference_sites"]]}:
        parser.error("Unknown source id")
    known = prepare_known(settings)
    previous = migrate_previous(load_yaml(ROOT / "_data/auto-publications.yaml"), known)
    # A previously verified discovery also anchors subsequent status updates,
    # without turning automatic records into curated _target patches.
    collection_known = known + [r for r in previous if not r.get("_target") and
                               r.get("_identity") == "confirmed" and r.get("researcher_ids") and
                               r.get("_source_id") not in settings["excluded_source_ids"]]
    today = datetime.now(ZoneInfo("Asia/Seoul")).date()
    incoming, coverage = run_collectors(settings, collection_known, today, args.researcher, args.source)
    records, candidates = reconcile(incoming, known, previous, settings)
    report = dict(checked_at=datetime.now(timezone.utc).isoformat(), backfill=args.backfill, coverage=coverage,
                  requests=sum(c["requests"] for c in coverage), automatic_records=len(records), candidates=candidates,
                  limitations=["Public sources only; bounded searches are not an exhaustive inventory.",
                               "ORCID discovery resolves public journal/conference DOIs through Crossref; unsupported records require manual verification.",
                               "Collaborator name plus affiliation alone cannot confirm a Crossref author or patent inventor.",
                               "Conference programs verify listings, not attendance.",
                               "Google Patents bibliographic grant facts do not establish current legal validity.",
                               "Corporate software ownership does not establish individual participation.",
                               "Unpublished filings and login-only databases are not collected.",
                               "Trademark/design discovery is not connected; curated entries are retained."])
    atomic_write(args.output_dir / "_publications/review.json", json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    if not any(c["status"] in ("ok", "partial") for c in coverage):
        raise RuntimeError("All sources failed; previous publication files preserved (see review.json)")
    atomic_write(args.output_dir / "_data/auto-publications.yaml", "# Generated by _publications/update.py\n" + yaml.safe_dump(records, allow_unicode=True, sort_keys=False))
    print(f"Saved {len(records)} automatic records and {len(candidates)} review candidates", flush=True)


if __name__ == "__main__":
    main()
