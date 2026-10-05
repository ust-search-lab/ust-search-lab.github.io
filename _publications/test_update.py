import copy
from datetime import date
import unittest

from bs4 import BeautifulSoup
from update import (normalize_crossref, normalize_patent, normalize_software,
                    normalize_program, reconcile, safe_record, same_record, update_patch)

TODAY = date(2026, 10, 5)
IDENTITY = {"names": ["Jae-ik Park", "Jae Ik Park", "박재익"],
            "orcid": "0000-0001-6227-0442", "affiliations": ["Korea Aerospace Research Institute", "한국항공우주연구원"]}
SETTINGS = {"approved_source_ids": [], "excluded_source_ids": []}


def article():
    return {"DOI": "10.1234/test", "title": ["Trajectory design"], "type": "proceedings-article",
            "published": {"date-parts": [[2026, 9]]}, "container-title": ["Conference"],
            "author": [{"given": "Jae-ik", "family": "Park", "affiliation": [{"name": "Korea Aerospace Research Institute"}]}]}


class IdentityTests(unittest.TestCase):
    def test_same_name_without_affiliation_is_review_only(self):
        work = article()
        work['author'][0]['affiliation'] = []
        record = normalize_crossref(work, IDENTITY, TODAY, [])
        self.assertEqual(record['_identity'], 'review')
        records, candidates = reconcile([record], [], [], SETTINGS)
        self.assertEqual(records, [])
        self.assertEqual(len(candidates), 1)

    def test_conflicting_orcid_is_rejected_even_with_same_name(self):
        work = article()
        work['author'][0]['ORCID'] = 'https://orcid.org/0000-0000-0000-0001'
        self.assertIsNone(normalize_crossref(work, IDENTITY, TODAY, []))

    def test_conference_and_partial_dates_preserved(self):
        record = normalize_crossref(article(), IDENTITY, TODAY, [])
        self.assertEqual((record['category'], record['date'], record['_identity']), ('conference', '2026-09', 'confirmed'))

    def test_future_online_article_not_published_using_old_print_date(self):
        work = article()
        work['published-online'] = {'date-parts': [[2027, 1, 1]]}
        self.assertIsNone(normalize_crossref(work, IDENTITY, TODAY, []))

    def test_accepted_becomes_published_without_new_duplicate(self):
        old = {'id': 'accepted:test', 'title': 'Trajectory design', 'authors': ['Jae-ik Park'], 'category': 'journal', 'status': 'accepted'}
        work = article()
        work['type'] = 'journal-article'
        record = normalize_crossref(work, IDENTITY, TODAY, [old])
        records, _ = reconcile([record], [old], [], SETTINGS)
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]['_target'], 'accepted:test')
        self.assertEqual(records[0]['status'], 'published')
        self.assertNotIn('authors', records[0])

    def test_article_and_conference_with_same_title_are_distinct(self):
        a = {'title': 'Trajectory design', 'year': 2026, 'category': 'journal'}
        self.assertFalse(same_record(a, {**a, 'category': 'conference'}))

    def test_exclusions_and_failed_source_preservation(self):
        record = normalize_crossref(article(), IDENTITY, TODAY, [])
        prior = [record]
        self.assertEqual(reconcile([], [], prior, SETTINGS)[0], prior)
        excluded = {**record, 'exclude': True}
        self.assertEqual(reconcile([record], [excluded], prior, SETTINGS)[0], [])

    def test_patent_numbers_never_match_across_countries(self):
        a = {'category': 'patent', 'country': 'US', 'application_number': '12345'}
        self.assertFalse(same_record(a, {**a, 'country': 'KR'}))

    def test_existing_registered_record_never_downgraded(self):
        old = {'category': 'patent', 'status': 'registered', 'details': 'Verified grant'}
        self.assertNotIn('status', update_patch(old, {'status': 'application', 'details': 'Old application'}))

    def test_new_automatic_application_merges_with_later_grant(self):
        old = dict(category='patent', title='Patent', country='KR', application_number='10-2025-0001234',
                   status='application', _source_id='patent:KR20260001234A', _identity='confirmed')
        new = {**old, 'status': 'registered', '_source_id': 'patent:KR102000000B1', 'registration_number': '10-2000000'}
        result, _ = reconcile([new], [], [old], SETTINGS)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['status'], 'registered')
        self.assertEqual(result[0]['registration_number'], '10-2000000')

    def test_grant_date_is_not_publication_date(self):
        raw = b'''<meta charset="utf-8"><span itemprop="publicationNumber">KR102091031B1</span>
        <span itemprop="countryCode">KR</span><span itemprop="kindCode">B1</span>
        <span itemprop="title">Lunar orbit</span><span itemprop="applicationNumber">KR1020180131171A</span>
        <span itemprop="inventor">Jae Ik Park</span><span itemprop="assigneeOriginal">Korea Aerospace Research Institute</span>
        <time itemprop="filingDate">2018-10-30</time><time itemprop="publicationDate">2020-04-29</time>
        <dd itemprop="events"><time itemprop="date">2020-04-24</time><span itemprop="type">granted</span></dd>'''
        record = normalize_patent(raw, IDENTITY, TODAY)
        self.assertEqual(record['registration_date'], '2020-04-24')
        self.assertEqual(record['application_number'], '10-2018-0131171')
        self.assertEqual(record['registration_number'], '10-2091031')

    def test_corporate_software_requires_participation_confirmation(self):
        detail = {'regId': 'C-2026-000123', 'regDt': '2026-09-01', 'contTitle': 'Orbit program',
                  'authorNm': '한국항공우주연구원', 'rgdcKdCd': 'S', 'isOpenYn': 'Y', 'authorJumin': 'DO-NOT-COPY'}
        record = normalize_software({}, detail, TODAY)
        records, candidates = reconcile([record], [], [], SETTINGS)
        self.assertEqual(records, [])
        self.assertEqual(len(candidates), 1)
        self.assertNotIn('authors', record)
        self.assertNotIn('authorJumin', record)
        self.assertNotIn('authorJumin', safe_record(detail))
        old = {**record, 'audit_key': 'sw-1', 'authors': ['Jae-ik Park']}
        old.pop('registration_date')
        records, _ = reconcile([record], [old], [], SETTINGS)
        self.assertEqual(records[0]['_target'], 'sw-1')

    def test_software_nonpublic_and_future_records_rejected(self):
        detail = {'regId': 'C-2026-000123', 'regDt': '2027-01-01', 'contTitle': 'Program',
                  'authorNm': 'Org', 'rgdcKdCd': 'S', 'isOpenYn': 'Y'}
        self.assertIsNone(normalize_software({}, detail, TODAY))
        detail.update(regDt='2026-01-01', isOpenYn='N')
        self.assertIsNone(normalize_software({}, detail, TODAY))

    def test_program_future_sessions_not_added(self):
        card = BeautifulSoup('<div class="papertitle">[123] Test</div><div class="authors">박재익(한국항공우주연구원)</div>', 'html.parser')
        session = BeautifulSoup('<div class="s_date">11월 10일</div>', 'html.parser')
        self.assertIsNone(normalize_program(card, 'https://ksas.or.kr/proceedings/2026c/', 'KSAS', TODAY, session))
        session = BeautifulSoup('<div class="s_date">5월 10일</div>', 'html.parser')
        record = normalize_program(card, 'https://ksas.or.kr/proceedings/2026a/', 'KSAS', TODAY, session)
        self.assertEqual(record['authors'], ['박재익'])
        self.assertEqual(record['_identity'], 'confirmed')


if __name__ == '__main__':
    unittest.main()
