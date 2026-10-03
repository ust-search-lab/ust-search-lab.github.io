import copy
from contextlib import redirect_stdout
from datetime import date, datetime
import io
import json
from pathlib import Path
import unittest
from unittest.mock import patch
from urllib.parse import parse_qs, urlparse
from zoneinfo import ZoneInfo

import update

SETTINGS = json.loads((Path(__file__).resolve().parents[1] / "_data/radar-settings.json").read_text())
TODAY = date(2026, 10, 3)
NOW = datetime(2026, 10, 3, 16, 30, tzinfo=ZoneInfo("Asia/Seoul"))


def article(journal=0, **overrides):
    doi = f"10.1016/j.actaastro.test{journal}" if SETTINGS["journals"][journal]["id"] == "acta-astronautica" else f"10.2514/1.test{journal}"
    return {"DOI": doi, "type": "journal-article",
            "title": ["Solar Sailing to Lunar Orbits"], "ISSN": [SETTINGS["journals"][journal]["issn"]],
            "author": [{"given": "Jane", "family": "Researcher"}],
            "published-online": {"date-parts": [[2026, 10, 1]]}, **overrides}


def compute(fetch, previous=None, curation=None, lookup=None):
    with redirect_stdout(io.StringIO()):
        return update.refresh(SETTINGS, curation or {"pinned": [], "excluded_dois": []}, previous or {}, NOW,
                              fetch=fetch, lookup=lookup or (lambda _: {}))


def fetch_all(journal, settings, today):
    return [article(settings["journals"].index(journal))]


class RadarTests(unittest.TestCase):
    def test_space_topics_exclude_generic_aircraft_optimization(self):
        unrelated = article(title=["Optimal Control for Uncrewed Aircraft Trajectory Optimization"])
        self.assertEqual(update.match_topics(unrelated, SETTINGS), [])
        circling = article(title=["Occlusion-Aware Ground Target Tracking by a Dubins Vehicle"],
                           abstract="A UAV tracks a ground target using circular standoff orbits and a steering controller.")
        self.assertEqual(update.match_topics(circling, SETTINGS), [])
        relevant = article(title=["Optimal Control"], abstract="<jats:p>Lunar spacecraft guidance.</jats:p>")
        self.assertIn("control", update.match_topics(relevant, SETTINGS))

    def test_hyphens_markup_and_word_boundaries(self):
        work = article(title=["<i>Solar</i>-Sailing Around Small Bodies"])
        item = update.normalize_work(work, SETTINGS["journals"][0], SETTINGS, TODAY)
        self.assertEqual(item["title"], "Solar-Sailing Around Small Bodies")
        self.assertIn("sail", item["topics"])
        self.assertFalse(update.includes("marsupial dynamics", "mars"))

    def test_online_date_precedes_forthcoming_print_issue(self):
        work = article(**{"published-print": {"date-parts": [[2027, 1]]}})
        self.assertEqual(update.publication_date(work, TODAY), ("2026-10-01", "published-online"))

    def test_partial_dates_are_not_invented(self):
        work = article(**{"published-online": {}, "published-print": {"date-parts": [[2026, 9]]}})
        self.assertEqual(update.publication_date(work, TODAY), ("2026-09", "published-print"))
        self.assertEqual(update.publication_date({"published": {"date-parts": [[2025]]}}, TODAY)[0], "2025")

    def test_future_or_undated_articles_do_not_appear(self):
        for work in [article(**{"published-online": {"date-parts": [[2027, 1, 1]]}}), article(**{"published-online": {}})]:
            self.assertIsNone(update.normalize_work(work, SETTINGS["journals"][0], SETTINGS, TODAY))

    def test_malformed_dates_do_not_drop_other_valid_dates(self):
        for malformed in [None, {}, {"date-parts": []}, {"date-parts": [None]}, {"date-parts": [[2026, 13]]}]:
            work = article(**{"published-online": malformed, "published-print": {"date-parts": [[2026, 9]]}})
            self.assertEqual(update.publication_date(work, TODAY), ("2026-09", "published-print"))

    def test_other_journals_and_correction_notices_are_rejected(self):
        for work in [article(ISSN=["1234-5678"]), article(title=["Correction: Lunar Orbits"]),
                     article(**{"update-to": [{"type": "retraction"}]}), article(type="proceedings-article")]:
            self.assertIsNone(update.normalize_work(work, SETTINGS["journals"][0], SETTINGS, TODAY))

    def test_deduplication_and_recent_date_order(self):
        def fetch(journal, settings, today):
            base = fetch_all(journal, settings, today)[0]
            return [base, copy.deepcopy(base), {**base, "DOI": base["DOI"] + "old", "published-online": {"date-parts": [[2026, 7, 1]]}}]
        snapshot, _ = compute(fetch)
        self.assertEqual(len(snapshot["items"]), len(SETTINGS["journals"]))
        self.assertEqual({item["journal_id"] for item in snapshot["items"]}, {journal["id"] for journal in SETTINGS["journals"]})
        self.assertTrue(all(item["date"] == "2026-10-01" for item in snapshot["items"]))

    def test_one_failed_journal_preserves_its_snapshot_and_timestamp(self):
        previous, _ = compute(fetch_all)
        previous["journals"][0]["last_success_at"] = "2026-10-02T10:17:00+09:00"
        original = copy.deepcopy(previous)
        def fetch(journal, settings, today):
            if journal["id"] == "jgcd":
                raise RuntimeError("HTTP 429")
            return fetch_all(journal, settings, today)
        snapshot, warnings = compute(fetch, previous)
        self.assertTrue(snapshot["partial"])
        self.assertEqual(snapshot["journals"][0]["last_success_at"], "2026-10-02T10:17:00+09:00")
        self.assertEqual(snapshot["journals"][0]["status"], "stale")
        self.assertEqual(len(snapshot["items"]), len(SETTINGS["journals"]))
        self.assertEqual(previous, original)
        self.assertEqual(len(warnings), 1)

    def test_total_outage_and_empty_responses_leave_snapshot_untouched(self):
        previous, _ = compute(fetch_all)
        original = copy.deepcopy(previous)
        with self.assertRaisesRegex(RuntimeError, "snapshot was not changed"):
            compute(lambda *_: [], previous)
        self.assertEqual(previous, original)

    def test_manual_pins_are_separate_and_exclusion_wins(self):
        curation = {"pinned": [{"doi": "https://doi.org/10.2514/1.TEST0", "note": {"ko": "세미나 추천"}}], "excluded_dois": []}
        snapshot, _ = compute(fetch_all, curation=curation)
        self.assertEqual(snapshot["pinned"][0]["note"]["ko"], "세미나 추천")
        self.assertEqual({item["doi"] for item in snapshot["items"]}, {article(index)["DOI"] for index in range(1, len(SETTINGS["journals"]))})
        curation["excluded_dois"] = ["10.2514/1.test0"]
        snapshot, _ = compute(fetch_all, curation=curation)
        self.assertEqual(snapshot["pinned"], [])
        self.assertNotIn("10.2514/1.test0", [item["doi"] for item in snapshot["items"]])

    def test_older_pinned_paper_is_resolved_without_topic_filter(self):
        work = article(DOI="10.2514/1.old", title=["A Foundational Control Method"], **{"published-online": {"date-parts": [[2010, 1, 1]]}})
        snapshot, _ = compute(fetch_all, curation={"pinned": [{"doi": "10.2514/1.old"}], "excluded_dois": []}, lookup=lambda _: work)
        self.assertEqual(snapshot["pinned"][0]["date"], "2010-01-01")
        self.assertEqual(snapshot["pinned"][0]["topics"], [])

    def test_invalid_or_unresolved_pins_cannot_fabricate_papers(self):
        with self.assertRaisesRegex(ValueError, "Invalid DOI"):
            compute(fetch_all, curation={"pinned": [{"doi": "not-a-doi"}], "excluded_dois": []})
        snapshot, _ = compute(fetch_all, curation={"pinned": [{"doi": "10.2514/1.unknown"}], "excluded_dois": []})
        self.assertEqual(snapshot["pinned"], [])
        self.assertEqual(snapshot["missing_pins"], ["10.2514/1.unknown"])

    def test_cursors_do_not_use_unsupported_publication_sort(self):
        calls = []
        def request(url):
            params = parse_qs(urlparse(url).query)
            calls.append(params)
            if len(calls) == 1:
                return {"items": [article()] * 200, "next-cursor": "next-page"}
            return {"items": [article()]}
        with patch.object(update, "request_json", side_effect=request):
            results = update.fetch_journal(SETTINGS["journals"][0], SETTINGS, TODAY)
        self.assertEqual(len(results), 201)
        self.assertEqual(calls[1]["cursor"], ["next-page"])
        self.assertEqual(calls[0]["sort"], ["indexed"])


if __name__ == "__main__":
    unittest.main()
