"""Prevent attribution leakage between PI and collaborator output views."""
from datetime import date
import unittest
from unittest.mock import patch

from update import (Client, collect_orcid, collect_software, migrate_previous, normalize_crossref,
                    normalize_program, reconcile, request_budgets, run_collectors, same_record)
from test_update import article, IDENTITY
from bs4 import BeautifulSoup

TODAY = date(2026, 10, 8)
PARK = {**IDENTITY, "id": "jae-ik-park"}
OH = {"id": "seung-ryeol-oh", "names": ["Snyoll Oghim", "Seungryeol Oh", "오승렬"],
      "orcid": "0009-0000-5985-6143", "affiliations": ["KAIST", "한국항공우주연구원"],
      "allow_affiliation_match": False}
BAE = {"id": "jungju-bae", "names": ["Jungju Bae", "배정주"], "orcid": "0000-0003-4397-5740",
       "affiliations": ["Inha University", "인하대학교"], "allow_affiliation_match": False}
SETTINGS = {"researchers": [PARK, OH, BAE], "approved_source_ids": [], "excluded_source_ids": [],
            "max_requests": 48, "conference_sites": [], "source_budget_weights": {}}


class ResearcherAttributionTests(unittest.TestCase):
    def test_kaist_homonym_is_review_without_orcid_or_known_participation(self):
        work = article()
        work["author"] = [{"given": "Seungryeol", "family": "Oh", "affiliation": [{"name": "KAIST"}]}]
        record = normalize_crossref(work, OH, TODAY, [])
        self.assertEqual(record["_identity"], "review")
        self.assertEqual(reconcile([record], [], [], SETTINGS)[0], [])
        self.assertEqual(normalize_crossref(work, OH, TODAY, [], orcid_linked=True)["_identity"], "confirmed")

    def test_public_orcid_doi_cannot_override_conflicting_author_orcid(self):
        work = article()
        work["author"] = [{"given": "Seungryeol", "family": "Oh", "ORCID": "https://orcid.org/0000-0000-0000-0001"}]
        self.assertIsNone(normalize_crossref(work, OH, TODAY, [], orcid_linked=True))

    def test_correction_requires_review_even_with_confirmed_orcid(self):
        work = article()
        work["title"] = ["Correction to: Trajectory design"]
        work["author"][0]["ORCID"] = "https://orcid.org/" + PARK["orcid"]
        record = normalize_crossref(work, PARK, TODAY, [], orcid_linked=True)
        self.assertEqual(record["_identity"], "review")
        self.assertEqual(reconcile([record], [], [], SETTINGS)[0], [])

    def test_coworker_known_title_does_not_confirm_homonym(self):
        work = article()
        work["author"].append({"given": "Jungju", "family": "Bae"})
        known = {"doi": "10.1234/test", "category": "conference", "researcher_ids": [PARK["id"]]}
        record = normalize_crossref(work, BAE, TODAY, [known])
        self.assertEqual(record["_identity"], "review")

    def test_one_shared_doi_unions_verified_people_without_duplicate(self):
        work = article()
        work["author"].append({"given": "Jungju", "family": "Bae", "ORCID": "https://orcid.org/" + BAE["orcid"]})
        records = [normalize_crossref(work, i, TODAY, []) for i in (PARK, BAE)]
        result, _ = reconcile(records, [], [], SETTINGS)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["researcher_ids"], [PARK["id"], BAE["id"]])

    def test_collaborator_only_never_acquires_pi_id(self):
        work = article()
        work["author"] = [{"given": "Jungju", "family": "Bae", "ORCID": "https://orcid.org/" + BAE["orcid"]}]
        self.assertIsNone(normalize_crossref(work, PARK, TODAY, []))
        result, _ = reconcile([normalize_crossref(work, BAE, TODAY, [])], [], [], SETTINGS)
        self.assertEqual(result[0]["researcher_ids"], [BAE["id"]])

    def test_target_patch_retains_prior_collaborator_when_pi_adds_no_new_metadata(self):
        known = dict(id="curated:1", category="journal", title="Test", doi="10.1234/test",
                     researcher_ids=[PARK["id"]])
        base = dict(category="journal", title="Test", doi="10.1234/test", _identity="confirmed",
                    _source="crossref", _source_id="doi:10.1234/test", verification_source="https://example.org/test")
        records = [{**base, "researcher_ids": [BAE["id"]]}, {**base, "researcher_ids": [PARK["id"]]}]
        result, _ = reconcile(records, [known], [], SETTINGS)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["_target"], "curated:1")
        self.assertEqual(result[0]["researcher_ids"], [PARK["id"], BAE["id"]])

    def test_review_participant_does_not_leak_through_curated_target(self):
        known = dict(id="curated:1", category="journal", title="Test", doi="10.1234/test",
                     researcher_ids=[PARK["id"]])
        incoming = {**known, "researcher_ids": [BAE["id"]], "publisher": "A journal", "_identity": "review",
                    "_source": "crossref", "_source_id": "doi:10.1234/test", "verification_source": "https://example.org/test"}
        result, candidates = reconcile([incoming], [known], [], SETTINGS)
        self.assertEqual(result[0]["researcher_ids"], [PARK["id"]])
        self.assertEqual(candidates[0]["researcher_ids"], [BAE["id"]])

    def test_same_target_different_patent_publications_union_ids(self):
        common = dict(_target="curated:1", category="patent", title="Test", _identity="confirmed")
        previous = [{**common, "_source_id": "patent:KR123A", "researcher_ids": [PARK["id"]]},
                    {**common, "_source_id": "patent:KR123B", "researcher_ids": [BAE["id"]]}]
        result, _ = reconcile([], [], previous, SETTINGS)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["researcher_ids"], [PARK["id"], BAE["id"]])

    def test_existing_automatic_grant_does_not_downgrade_on_same_source_id(self):
        prior = dict(_source_id="patent:KR123B", category="patent", title="Test", country="KR",
                     application_number="123", _identity="confirmed", status="registered",
                     researcher_ids=[PARK["id"]], details="Verified grant")
        incoming = {**prior, "status": "application", "details": "Old application", "researcher_ids": [BAE["id"]]}
        result, _ = reconcile([incoming], [], [prior], SETTINGS)
        self.assertEqual(result[0]["status"], "registered")
        self.assertEqual(result[0]["details"], "Verified grant")
        self.assertEqual(result[0]["researcher_ids"], [PARK["id"], BAE["id"]])

    def test_prior_confirmed_pi_snapshot_migrates_without_loss(self):
        prior = [dict(_target="old:1", _source_id="doi:10.1234/test", _identity="confirmed")]
        result = migrate_previous(prior, [])
        self.assertEqual(result[0]["researcher_ids"], [PARK["id"]])
        self.assertNotIn("researcher_ids", prior[0])
        self.assertEqual(reconcile([], [], result, SETTINGS)[0], result)

    def test_existing_corporate_software_retains_curated_individuals(self):
        known = dict(id="software:1", category="software", title="Program", registration_number="C-2026-000001",
                     copyright_author="한국항공우주연구원", researcher_ids=[PARK["id"], BAE["id"]])
        incoming = {**known, "registration_date": "2026-01-01", "_identity": "review",
                    "_source_id": "software:C-2026-000001", "_source": "cros", "verification_source": "https://example.org/test"}
        incoming.pop("researcher_ids")
        result, _ = reconcile([incoming], [known], [], SETTINGS)
        self.assertEqual(result[0]["researcher_ids"], [PARK["id"], BAE["id"]])
        new, candidates = reconcile([incoming], [], [], {**SETTINGS, "approved_source_ids": [incoming["_source_id"]]})
        self.assertEqual(new, [])
        self.assertEqual(len(candidates), 1)

    def test_conference_person_is_parameterized(self):
        card = BeautifulSoup('<div class="papertitle">[1] Solar sail</div><div class="authors">배정주(인하대학교)</div>', 'html.parser')
        session = BeautifulSoup('<div class="s_date">5월 10일</div>', 'html.parser')
        record = normalize_program(card, 'https://ksas.or.kr/proceedings/2026a/', 'KSAS', TODAY, session, BAE)
        self.assertEqual(record["researcher_ids"], [BAE["id"]])
        self.assertEqual(record["_identity"], "confirmed")
        self.assertIsNone(normalize_program(card, 'https://ksas.or.kr/proceedings/2026a/', 'KSAS', TODAY, session, PARK))

    def test_same_title_at_different_conference_is_not_merged(self):
        spring = dict(category="conference", title="Solar sail", year=2026,
                      link="https://ksas.or.kr/proceedings/2026a/SessionPaperList.asp?code=1")
        fall = {**spring, "link": "https://sase.or.kr/proceedings/2026c/SessionPaperList.asp?code=2"}
        self.assertFalse(same_record(spring, fall))
        self.assertFalse(same_record({**spring, "date": "2026-05"}, {**spring, "date": "2026-10-08"}))
        self.assertTrue(same_record({**spring, "date": "2026"}, {**spring, "date": "2026-05-08"}))
        self.assertTrue(same_record({**spring, "doi": "10.1234/test"}, {**fall, "doi": "10.1234/test"}))

    def test_orcid_only_uses_public_self_doi_with_matching_crossref_author(self):
        work = article()
        work["author"] = [{"given": "Jungju", "family": "Bae"}]
        entries = [{"type": "journal-article", "visibility": "public", "external-ids": {"external-id": [
            {"external-id-type": "doi", "external-id-value": "10.1234/test", "external-id-relationship": "self"},
            {"external-id-type": "doi", "external-id-value": "10.1234/not-this-work", "external-id-relationship": "part-of"}]}}]
        class FakeClient:
            warnings = []
            def json(self, url):
                return {"group": [{"work-summary": entries}]}
            def optional_json(self, url):
                self.url = url
                return {"message": work}
        client = FakeClient()
        result = collect_orcid(client, {"identity": BAE}, [], TODAY)
        self.assertEqual(len(result), 1)
        self.assertTrue(client.url.endswith("10.1234%2Ftest"))
        self.assertEqual(result[0]["researcher_ids"], [BAE["id"]])
        self.assertEqual(result[0]["_identity"], "confirmed")

    def test_budget_reserved_per_person_and_failure_does_not_skip_others(self):
        budgets = request_budgets([3, 3, 3, 1, 1, 1], 48)
        self.assertEqual(sum(budgets), 48)
        self.assertTrue(all(b > 0 for b in budgets))
        def collect(client, settings, known, today):
            if settings["identity"]["id"] == PARK["id"]:
                raise RuntimeError("Request budget reached")
            return [{"researcher_ids": [settings["identity"]["id"]]}]
        with patch("update.collect_orcid", collect):
            records, coverage = run_collectors(SETTINGS, [], TODAY, source_filter=["orcid"])
        self.assertEqual([r["researcher_ids"] for r in records], [[OH["id"]], [BAE["id"]]])
        self.assertEqual([c["status"] for c in coverage], ["failed", "ok", "ok"])
        self.assertEqual(sum(c["budget"] for c in coverage), 48)
        self.assertEqual(coverage[-1]["available_requests"], 48)

    def test_partial_cros_detail_failure_preserves_earlier_valid_records(self):
        detail = dict(regId="C-2026-000001", regDt="2026-01-01", contTitle="Orbit", authorNm="한국항공우주연구원",
                      rgdcKdCd="S", isOpenYn="Y")
        documents = [dict(SYS_ID=str(i), REG_ID=f"C-2026-00000{i}", RGDC_KD_CD="S", isopenyn="Y", CONT_TITLE="Orbit") for i in (1, 2)]
        class FakeClient:
            warnings = []
            def optional_json(self, url, **kwargs):
                if "wisenut/search" in url:
                    return dict(document=documents, TotalCount=2)
                if kwargs["body"]["dm_regDtlSchMap"]["sysId"] == "1":
                    return {"dl_regDtlList": [detail]}
                self.warnings.append("Request budget reached")
                return None
        client = FakeClient()
        results = collect_software(client, {"software_keywords": ["Orbit"], "lookback_years": 2}, [], TODAY)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["registration_number"], "C-2026-000001")
        self.assertTrue(client.warnings)


if __name__ == "__main__":
    unittest.main()
