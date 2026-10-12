"""Exercise supported Crossref queries, pagination, and partial recovery."""
from datetime import date
import unittest
from urllib.parse import parse_qs, urlsplit

from update import collect_crossref, date_parts
from test_update import article, IDENTITY

TODAY = date(2026, 10, 12)
SETTINGS = {"identity": IDENTITY, "lookback_years": 2, "crossref_max_pages": 3}


class FakeClient:
    def __init__(self, respond):
        self.respond = respond
        self.warnings = []
        self.queries = []

    def optional_json(self, url):
        query = parse_qs(urlsplit(url).query)
        self.queries.append(query)
        return self.respond(query)


class CrossrefTests(unittest.TestCase):
    def test_pending_title_uses_supported_bibliographic_lookup_and_alias(self):
        def respond(query):
            self.assertNotIn("query.title", query)
            works = [article()] if "query.bibliographic" in query else []
            return {"message": {"items": works, "total-results": len(works)}}
        client = FakeClient(respond)
        known = [{"id": "accepted:test", "title": "Trajectory design", "title_aliases": ["궤적 설계"],
                  "status": "accepted", "authors": ["Jae-ik Park"], "category": "conference"}]
        records = collect_crossref(client, SETTINGS, known, TODAY)
        self.assertEqual(len(records), 1)
        self.assertEqual(client.queries[0]["query.bibliographic"], ["Trajectory design Jae-ik Park"])
        self.assertEqual(client.queries[1]["query.bibliographic"], ["궤적 설계 Jae-ik Park"])

    def test_second_page_work_is_collected_and_duplicates_merge(self):
        def respond(query):
            if "query.author" not in query:
                return {"message": {"items": [], "total-results": 0}}
            if query["offset"] == ["0"]:
                return {"message": {"items": [{"type": "book"}] * 100, "total-results": 101}}
            return {"message": {"items": [article()], "total-results": 101}}
        client = FakeClient(respond)
        records = collect_crossref(client, SETTINGS, [], TODAY)
        self.assertEqual(len(records), 1)
        self.assertTrue(any(q["offset"] == ["100"] for q in client.queries))
        latest = [q for q in client.queries if q.get("sort") == ["published"]]
        self.assertTrue(latest)
        self.assertTrue(all(q["order"] == ["desc"] and "cursor" not in q for q in latest))
        self.assertIn("until-pub-date:2026-10-12", latest[0]["filter"][0])

    def test_bounded_discovery_reports_unread_results(self):
        client = FakeClient(lambda _: {"message": {"items": [{"type": "book"}] * 100, "total-results": 1000}})
        self.assertEqual(collect_crossref(client, SETTINGS, [], TODAY), [])
        self.assertTrue(client.warnings)
        self.assertTrue(all(int(q["offset"][0]) <= 200 for q in client.queries))

    def test_later_schema_failure_keeps_earlier_verified_work(self):
        def respond(query):
            if query["offset"] == ["0"]:
                return {"message": {"items": [article()] * 100, "total-results": 101}}
            return {"message": {"items": None}}
        client = FakeClient(respond)
        self.assertEqual(len(collect_crossref(client, SETTINGS, [], TODAY)), 1)
        self.assertIn("Crossref response schema changed", client.warnings)

    def test_malformed_date_does_not_abort_collection(self):
        for value in (None, {}, {"date-parts": []}, {"date-parts": [None]}, {"date-parts": [[2026, 13]]}):
            self.assertEqual(date_parts({"published-online": value, "published": {"date-parts": [[2026, 9]]}}, TODAY), "2026-09")


if __name__ == "__main__":
    unittest.main()
