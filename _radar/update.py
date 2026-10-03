#!/usr/bin/env python3
"""Refresh a small, topic-filtered Crossref snapshot for the static website.

Only bibliographic metadata is saved. Abstracts are used for matching in memory.
Curl uses the OS certificate store on both macOS and GitHub's Ubuntu runners.
"""

import argparse
from datetime import date, datetime, timedelta
from html import unescape
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
import sys
import unicodedata
from urllib.parse import quote, urlencode
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
API = "https://api.crossref.org"
USER_AGENT = "SEARCHLabResearchRadar/1.0 (https://ust-search-lab.github.io/)"


class PlainText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_data(self, data):
        self.parts.append(data)


def plain(value):
    parser = PlainText()
    parser.feed(str(value or ""))
    return " ".join(unescape("".join(parser.parts)).split())


def normalized(value):
    return " ".join(re.sub(r"[^\w]+", " ", unicodedata.normalize("NFKC", plain(value)).casefold()).split())


def canonical_doi(value):
    value = re.sub(r"^(?:https?://(?:dx\.)?doi\.org/|doi:)\s*", "", str(value).strip(), flags=re.I).lower()
    if not re.fullmatch(r"10\.\d{4,9}/\S+", value):
        raise ValueError(f"Invalid DOI: {value!r}")
    return value


def includes(text, phrase):
    return f" {normalized(phrase)} " in f" {text} "


def match_topics(work, settings):
    text = normalized(" ".join(work.get("title", [])) + " " + str(work.get("abstract", "")))
    space = any(includes(text, phrase) for phrase in settings["space_context"])
    return [topic["id"] for topic in settings["topics"]
            if (space or not topic.get("requires_space_context"))
            and any(includes(text, phrase) for phrase in topic["keywords"])]


def publication_date(work, today):
    # Prefer online publication; do not substitute deposit/indexing timestamps.
    # Preserve year/month precision instead of inventing a publication day.
    for field in ["published-online", "published-print", "published", "issued"]:
        record = work.get(field)
        groups = record.get("date-parts") if isinstance(record, dict) else None
        if not isinstance(groups, list) or not groups:
            continue
        parts = groups[0]
        if not isinstance(parts, list) or not 1 <= len(parts) <= 3:
            continue
        try:
            parsed = date(*(parts + [1] * (3 - len(parts))))
        except (TypeError, ValueError):
            continue
        if parsed > today:
            continue
        value = "-".join([str(parts[0])] + [f"{part:02}" for part in parts[1:]])
        return value, field
    return None, None


def normalize_work(work, journal, settings, today, require_match=True):
    if work.get("type") != "journal-article":
        return None
    if not set(work.get("ISSN", [])) & set(journal["issns"]):
        return None
    title = plain(" ".join(work.get("title", [])))
    if not title or re.match(r"^(correction|erratum|corrigendum|retraction|editorial)\b", title, re.I):
        return None
    # Notices about another DOI are not new research articles.
    if work.get("update-to"):
        return None
    try:
        doi = canonical_doi(work.get("DOI", ""))
    except ValueError:
        return None
    published, date_type = publication_date(work, today)
    if not published:
        return None
    topics = match_topics(work, settings)
    if require_match and not topics:
        return None
    authors = []
    for author in work.get("author", []):
        name = plain(author.get("name") or " ".join(filter(None, [author.get("given"), author.get("family")])))
        if name:
            authors.append(name)
    return {"doi": doi, "url": "https://doi.org/" + quote(doi, safe="/():._-"),
            "title": title, "authors": authors, "journal_id": journal["id"],
            "journal": journal["name"], "journal_short": journal["short_name"],
            "date": published, "date_type": date_type, "topics": topics}


def request_json(url):
    result = subprocess.run(
        ["curl", "--silent", "--show-error", "--fail", "--location",
         "--connect-timeout", "10", "--max-time", "40", "--retry", "2",
         "--retry-delay", "5", "--retry-max-time", "90",
         "--user-agent", USER_AGENT, "--header", "Accept: application/json", url],
        capture_output=True, text=True, timeout=140, check=False,
    )
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or f"curl exited with {result.returncode}")
    data = json.loads(result.stdout)
    if data.get("status") != "ok" or "message" not in data:
        raise ValueError("Unexpected Crossref response")
    return data["message"]


def fetch_journal(journal, settings, today):
    start = today - timedelta(days=settings["lookback_days"])
    params = {"filter": f"type:journal-article,from-pub-date:{start},until-pub-date:{today}",
              "rows": 200, "cursor": "*", "sort": "indexed", "order": "desc",
              "select": "DOI,title,author,published-online,published-print,published,issued,ISSN,type,abstract,update-to"}
    works = []
    cursors = set()
    for _ in range(5):
        message = request_json(f"{API}/journals/{journal['issn']}/works?{urlencode(params)}")
        batch = message.get("items")
        if not isinstance(batch, list):
            raise ValueError("Crossref did not return an article list")
        works.extend(batch)
        if len(batch) < params["rows"]:
            return works
        cursor = message.get("next-cursor")
        if not cursor or cursor in cursors:
            raise ValueError("Crossref pagination did not advance")
        cursors.add(cursor)
        params["cursor"] = cursor
    raise ValueError("Unexpectedly large journal response; preserving previous snapshot")


def newest(items):
    unique = {}
    for item in items:
        unique[item["doi"]] = item
    return sorted(unique.values(), key=lambda item: (item["date"], item["doi"]), reverse=True)


def refresh(settings, curation, previous, now, fetch=fetch_journal, lookup=request_json):
    today = now.date()
    timestamp = now.isoformat(timespec="seconds")
    excluded = {canonical_doi(doi) for doi in curation["excluded_dois"]}
    pin_config = curation["pinned"]
    pin_ids = [canonical_doi(pin["doi"]) for pin in pin_config]
    if len(set(pin_ids)) != len(pin_ids):
        raise ValueError("Duplicate pinned DOI")
    journals, warnings, successes, candidates = [], [], 0, {}
    previous_journals = {item["id"]: item for item in previous.get("journals", [])}
    for journal in settings["journals"]:
        print(f"Fetching {journal['short_name']}…", flush=True)
        try:
            works = fetch(journal, settings, today)
            if not works:
                raise ValueError("Empty journal response; preserving previous snapshot")
            matches = []
            for work in works:
                item = normalize_work(work, journal, settings, today)
                if item:
                    # A forthcoming print issue can have an older online date.
                    if item["date"] >= (today - timedelta(days=settings["lookback_days"])).isoformat():
                        matches.append(item)
                if str(work.get("DOI", "")).lower() in pin_ids:
                    pin = normalize_work(work, journal, settings, today, require_match=False)
                    if pin:
                        candidates[pin["doi"]] = pin
            record = {**journal, "last_success_at": timestamp, "status": "ok",
                      "items": newest([item for item in matches if item["doi"] not in excluded])[:settings["items_per_journal"]]}
            successes += 1
        except (RuntimeError, ValueError, subprocess.SubprocessError) as error:
            warnings.append(f"{journal['short_name']}: {error}")
            record = {**journal, **previous_journals.get(journal["id"], {}), "status": "stale"}
            record["items"] = [item for item in record.get("items", []) if item["doi"] not in excluded]
        journals.append(record)
        for cached in record.get("items", []):
            if cached["doi"] in pin_ids:
                candidates.setdefault(cached["doi"], cached)
    if successes == 0:
        raise RuntimeError("All journal requests failed; snapshot was not changed. " + "; ".join(warnings))

    old_pins = {item["doi"]: item for item in previous.get("pinned", [])}
    pinned, missing_pins = [], []
    for config, doi in zip(pin_config, pin_ids):
        if doi in excluded:
            continue
        item = candidates.get(doi)
        if not item:
            try:
                work = lookup(f"{API}/works/{quote(doi, safe='')}")
                for journal in settings["journals"]:
                    item = normalize_work(work, journal, settings, today, require_match=False)
                    if item:
                        break
                if not item or item["doi"] != doi:
                    raise ValueError("Pinned DOI is not a published research article in a configured journal")
            except (RuntimeError, ValueError, subprocess.SubprocessError) as error:
                item = old_pins.get(doi)
                warnings.append(f"Pinned DOI {doi}: {error}")
                if not item:
                    missing_pins.append(doi)
        if item:
            pinned.append({**item, "note": {lang: plain(config.get("note", {}).get(lang, "")) for lang in ["ko", "en"]}})
    items = newest([item for journal in journals for item in journal["items"]
                    if item["doi"] not in set(pin_ids)])
    snapshot = {"source": "Crossref", "updated_at": timestamp,
                "lookback_days": settings["lookback_days"],
                "partial": successes < len(journals), "missing_pins": missing_pins,
                "journals": journals, "pinned": pinned, "items": items}
    return snapshot, warnings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--settings", type=Path, default=ROOT / "_data/radar-settings.json")
    parser.add_argument("--curation", type=Path, default=ROOT / "_data/radar-curation.json")
    parser.add_argument("--output", type=Path, default=ROOT / "_data/research-radar.json")
    args = parser.parse_args()
    try:
        settings = json.loads(args.settings.read_text())
        curation = json.loads(args.curation.read_text())
        previous = json.loads(args.output.read_text()) if args.output.exists() else {}
        snapshot, warnings = refresh(settings, curation, previous, datetime.now(ZoneInfo("Asia/Seoul")))
        args.output.parent.mkdir(parents=True, exist_ok=True)
        temporary = args.output.with_suffix(".tmp")
        temporary.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n")
        temporary.replace(args.output)
        for warning in warnings:
            print(f"Warning: {warning}", file=sys.stderr)
        print(f"Saved {len(snapshot['items'])} recent articles and {len(snapshot['pinned'])} pinned articles.")
    except (OSError, ValueError, RuntimeError, KeyError) as error:
        print(f"Research Radar update failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
