#!/usr/bin/env python3
"""Collect official space-news metadata for the static website.

RSS descriptions / list-page excerpts are used for matching in memory only.
No article bodies or publisher images are stored or republished.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timedelta
from email.utils import parsedate_to_datetime
from html import unescape
import json
from pathlib import Path
import re
import subprocess
import sys
import unicodedata
from urllib.parse import parse_qsl, urlencode, urljoin, urlsplit, urlunsplit
import xml.etree.ElementTree as ET
from zoneinfo import ZoneInfo

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
KST = ZoneInfo("Asia/Seoul")
USER_AGENT = "SEARCHLabSpaceNews/1.0 (+https://ust-search-lab.github.io/)"


def plain(value):
    soup = BeautifulSoup(str(value or ""), "html.parser")
    for node in soup.select("script, style"):
        node.decompose()
    return " ".join(unescape(soup.get_text(" ", strip=True)).split())


def normalized(value):
    return " ".join(re.sub(r"[^\w]+", " ", unicodedata.normalize("NFKC", value).casefold()).split())


def contains(text, phrase):
    phrase = normalized(phrase)
    if re.search(r"[가-힣]", phrase):
        return phrase.replace(" ", "") in text.replace(" ", "")
    return f" {phrase} " in f" {text} "


def canonical_url(value, base, hosts):
    parts = urlsplit(urljoin(base, unescape(value)))
    if (parts.scheme not in ("http", "https") or parts.hostname not in hosts
            or parts.username or parts.password or parts.port not in (None, 80, 443)):
        raise ValueError("Article URL is outside its official source")
    # Government list URLs repeat pagination/search parameters on each article.
    query = parse_qsl(parts.query, keep_blank_values=True)
    if parts.hostname == "www.korea.kr":
        query = [(k, v) for k, v in query if k == "newsId"]
        if len(query) != 1 or not query[0][1].isdigit():
            raise ValueError("Missing policy-briefing article identifier")
    else:
        query = [(k, v) for k, v in query if not k.lower().startswith("utm_")
                 and k.lower() not in ("fbclid", "gclid")]
    return urlunsplit(("https", parts.hostname, parts.path, urlencode(sorted(query)), ""))


def publication_date(value):
    value = str(value or "").strip()
    if re.fullmatch(r"\d{4}[-.]\d{2}[-.]\d{2}", value):
        return date.fromisoformat(value.replace(".", "-")).isoformat()
    try:
        stamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        stamp = parsedate_to_datetime(value)
    # Retain the publication's calendar date rather than shifting it to KST.
    return stamp.date().isoformat()


def parse_feed(content):
    # RSS 2.0, RDF/RSS 1.0 (JAXA), and Atom; never use updated as publication date.
    if b"<!DOCTYPE" in content.upper() or b"<!ENTITY" in content.upper():
        raise ValueError("Unexpected XML declarations")
    root = ET.fromstring(content)
    if root.tag.split("}")[-1] not in ("rss", "RDF", "feed"):
        raise ValueError("Expected an RSS/Atom feed")
    records = []
    for node in root.iter():
        if node.tag.split("}")[-1] not in ("item", "entry"):
            continue
        fields = {child.tag.split("}")[-1]: "".join(child.itertext()) for child in node}
        link = fields.get("link", "")
        if node.tag.split("}")[-1] == "entry":
            link = next((child.get("href", "") for child in node
                         if child.tag.split("}")[-1] == "link"
                         and child.get("rel", "alternate") == "alternate"), "")
        records.append({"title": fields.get("title", ""), "url": link,
                        "date": fields.get("pubDate") or fields.get("date") or fields.get("published"),
                        "summary": fields.get("description") or fields.get("summary", "")})
    if not records:
        raise ValueError("Empty feed; keep the last successful snapshot")
    return records


def parse_kari(content):
    soup = BeautifulSoup(content, "html.parser")
    records = []
    for row in soup.select(".notice_list li"):
        link, dated = row.select_one(".subject a[href]"), row.select_one(".date")
        if not link or not dated:
            continue
        match = re.search(r"\d{4}-\d{2}-\d{2}", dated.get_text())
        if match:
            records.append({"title": link.get_text(" ", strip=True), "url": link["href"],
                            "date": match[0], "summary": ""})
    if not records:
        raise ValueError("KARI list structure changed or empty response")
    return records


def parse_kasa(content):
    # The government portal republishes KASA's official press releases.
    soup = BeautifulSoup(content, "html.parser")
    records = []
    for link in soup.select('a[href*="/briefing/pressReleaseView.do?"]'):
        title, source = link.select_one("strong"), link.select_one(".source")
        summary = link.select_one(".lead")
        if not title or not source or "우주항공청" not in source.get_text():
            continue
        match = re.search(r"\d{4}-\d{2}-\d{2}", source.get_text())
        if match:
            records.append({"title": title.get_text(" ", strip=True), "url": link["href"],
                            "date": match[0], "summary": summary.get_text(" ", strip=True) if summary else ""})
    if not records:
        raise ValueError("KASA list structure changed, agency mismatch or empty response")
    return records


def request_bytes(url):
    result = subprocess.run(
        ["curl", "--silent", "--show-error", "--fail", "--location",
         "--proto", "=https", "--proto-redir", "=https",
         "--connect-timeout", "10", "--max-time", "25", "--max-filesize", "8000000",
         "--retry", "1", "--retry-delay", "2", "--retry-max-time", "55",
         "--user-agent", USER_AGENT, url], capture_output=True, timeout=65, check=False)
    if result.returncode:
        raise RuntimeError(result.stderr.decode(errors="replace").strip() or "Source request failed")
    return result.stdout


def fetch_source(source, request=request_bytes):
    parser = {"rss": parse_feed, "kari": parse_kari, "kasa": parse_kasa}[source["kind"]]
    records = []
    for feed in source["feeds"]:
        for page in range(1, source.get("pages", 1) + 1):
            url = feed
            if page > 1:
                url += ("&" if "?" in feed else "?") + urlencode({"pageIndex": page})
            batch = parser(request(url))
            for record in batch:
                record["url"] = urljoin(feed, record["url"])
            records.extend(batch)
    return records


def excluded_item(title, url, settings):
    return (url in settings.get("excluded_urls", [])
            or any(part.casefold() in url.casefold() for part in settings["excluded_url_parts"])
            or any(contains(normalized(title), phrase) for phrase in settings["excluded_title_phrases"]))


def normalize_record(record, source, settings, today):
    title = plain(record.get("title"))
    title = re.sub(r"^\[release\]\s*", "", title, flags=re.I)
    try:
        url = canonical_url(record.get("url", ""), source["url"], source["hosts"])
        published = publication_date(record.get("date"))
    except (ValueError, TypeError, OverflowError):
        return None
    if not title or len(title) > 600 or not record.get("url"):
        return None
    if not (today - timedelta(days=settings["lookback_days"])).isoformat() <= published <= today.isoformat():
        return None
    if excluded_item(title, url, settings):
        return None
    context = normalized(title + " " + plain(record.get("summary"))[:3000])
    topics = [t["id"] for t in settings["topics"] if any(contains(context, k) for k in t["keywords"])]
    if not topics:
        return None
    return {"title": title, "url": url, "date": published, "source_id": source["id"],
            "source": source["name"], "region": source["region"],
            "language": source["language"], "topics": topics}


def newest_unique(items):
    # Prefer the first (fresh) record for a canonical URL, then remove syndication
    # with identical normalized titles. Different reports of an event remain.
    seen_urls, seen_titles, result = set(), set(), []
    for item in items:
        title_key = normalized(item["title"])
        if item["url"] in seen_urls or title_key in seen_titles:
            continue
        seen_urls.add(item["url"])
        seen_titles.add(title_key)
        result.append(item)
    return sorted(result, key=lambda item: (item["date"], item["url"]), reverse=True)


def refresh(settings, previous, now, fetch=fetch_source):
    now = now.astimezone(KST)
    timestamp, today = now.isoformat(timespec="seconds"), now.date()
    cutoff = (today - timedelta(days=settings["lookback_days"])).isoformat()
    old = {s["id"]: s for s in previous.get("sources", [])}
    sources, warnings = [], []
    successes = 0
    # Independent official sources can be fetched concurrently; each source's
    # pages are sequential and bounded. Source order keeps deduplication stable.
    with ThreadPoolExecutor(max_workers=6) as pool:
        futures = [pool.submit(fetch, source) for source in settings["sources"]]
        for source, future in zip(settings["sources"], futures):
            cached = old.get(source["id"], {})
            retained = []
            for item in cached.get("items", []):
                if (cutoff <= item["date"] <= today.isoformat()
                        and not excluded_item(item["title"], item["url"], settings)):
                    retained.append({**item, "stale": False})
            record = {k: source[k] for k in ("id", "name", "region", "url")}
            try:
                raw = future.result()
                if not raw:
                    raise ValueError("No source records")
                items = [item for row in raw if (item := normalize_record(row, source, settings, today))]
                record.update(status="ok", last_success_at=timestamp,
                              items=newest_unique(items + retained)[:settings["items_per_source"]])
                successes += 1
            except (RuntimeError, ValueError, OSError, subprocess.SubprocessError, ET.ParseError) as error:
                warnings.append(f"{source['name']}: {error}")
                record.update(status="stale", last_success_at=cached.get("last_success_at"),
                              items=[{**item, "stale": True} for item in retained][:settings["items_per_source"]])
            sources.append(record)
    if not successes:
        raise RuntimeError("All news sources failed; snapshot unchanged. " + "; ".join(warnings))
    # Prefer fresh records if the same story also exists in a delayed source.
    all_items = [item for s in sources for item in s["items"]]
    all_items.sort(key=lambda item: bool(item.get("stale")))
    return {"updated_at": timestamp, "lookback_days": settings["lookback_days"],
            "partial": successes < len(sources), "sources": sources,
            "items": newest_unique(all_items)}, warnings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--settings", type=Path, default=ROOT / "_data/space-news-settings.json")
    parser.add_argument("--output", type=Path, default=ROOT / "_data/space-news.json")
    args = parser.parse_args()
    try:
        settings = json.loads(args.settings.read_text())
        previous = json.loads(args.output.read_text()) if args.output.exists() else {}
        snapshot, warnings = refresh(settings, previous, datetime.now(KST))
        args.output.parent.mkdir(parents=True, exist_ok=True)
        temporary = args.output.with_suffix(".tmp")
        temporary.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n")
        temporary.replace(args.output)
        for warning in warnings:
            print(f"Warning: {warning}", file=sys.stderr)
        print(f"Saved {len(snapshot['items'])} news items; {len(warnings)} delayed sources.")
    except (OSError, ValueError, RuntimeError, KeyError) as error:
        print(f"Space News update failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
