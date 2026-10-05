"""Offline checks for changing publisher formats and safe scheduled refreshes."""
import copy
from datetime import date, datetime
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from zoneinfo import ZoneInfo

import update

SETTINGS = json.loads((update.ROOT / '_data/space-news-settings.json').read_text())
NOW = datetime(2026, 10, 5, 10, 47, tzinfo=ZoneInfo('Asia/Seoul'))
SOURCE = next(s for s in SETTINGS['sources'] if s['id'] == 'nasa')


def article(**changes):
    return {'title': 'New lunar lander guidance test', 'url': 'https://www.nasa.gov/test/',
            'date': '2026-10-01', 'summary': 'Testing autonomous navigation.', **changes}


class NewsChecks(unittest.TestCase):
    def test_rss_rdf_and_atom_dates_and_links(self):
        samples = [
            b'<rss><channel><item><title>Lunar guidance</title><link>https://www.nasa.gov/a/</link><pubDate>Thu, 01 Oct 2026 23:00:00 -0400</pubDate></item></channel></rss>',
            b'<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns="http://purl.org/rss/1.0/" xmlns:dc="http://purl.org/dc/elements/1.1/"><item><title>Lunar guidance</title><link>https://www.nasa.gov/a/</link><dc:date>2026-10-01T10:00:00+09:00</dc:date></item></rdf:RDF>',
            b'<feed xmlns="http://www.w3.org/2005/Atom"><entry><title>Lunar guidance</title><link rel="self" href="https://invalid.test/"/><link href="https://www.nasa.gov/a/"/><published>2026-10-01T10:00:00Z</published><updated>2026-10-05T10:00:00Z</updated></entry></feed>',
        ]
        for xml in samples:
            item = update.normalize_record(update.parse_feed(xml)[0], SOURCE, SETTINGS, NOW.date())
            self.assertEqual(item['date'], '2026-10-01')
            self.assertEqual(item['url'], 'https://www.nasa.gov/a/')

    def test_atom_update_is_not_a_publication_date(self):
        row = update.parse_feed(b'<feed><entry><title>Lunar guidance</title><link href="https://www.nasa.gov/a/"/><updated>2026-10-01T00:00:00Z</updated></entry></feed>')[0]
        self.assertIsNone(update.normalize_record(row, SOURCE, SETTINGS, NOW.date()))

    def test_empty_malformed_and_entity_feeds_fail(self):
        for xml in [b'<rss><channel/></rss>', b'<html>Blocked</html>', b'<rss>', b'<!DOCTYPE rss><rss/>']:
            with self.assertRaises(ValueError if b'<rss>' != xml else update.ET.ParseError):
                update.parse_feed(xml)

    def test_korean_boards_isolate_title_date_and_agency(self):
        kari = '<div class="notice_list"><li><p class="subject"><a href="/kor/article/a/1"><strong>다누리 달 궤도 실증</strong></a></p><p class="date"><span>등록일</span>2026-10-01</p><p>조회수 999</p></li></div>'
        self.assertEqual(update.parse_kari(kari)[0]['title'], '다누리 달 궤도 실증')
        self.assertEqual(update.parse_kari(kari)[0]['date'], '2026-10-01')
        kasa = '<a href="/briefing/pressReleaseView.do?newsId=123"><strong>위성 운용개념서</strong><span class="lead">우주임무 설계</span><span class="source"><span>2026-10-01</span><span>우주항공청</span></span></a>'
        self.assertEqual(len(update.parse_kasa(kasa)), 1)
        with self.assertRaises(ValueError):
            update.parse_kasa(kasa.replace('우주항공청', '다른부처'))
        with self.assertRaises(ValueError):
            update.parse_kari('<html>Maintenance</html>')

    def test_url_validation_and_canonicalization(self):
        self.assertEqual(update.canonical_url('/briefing/pressReleaseView.do?newsId=123&pageIndex=2&utm_source=x#top', 'https://www.korea.kr/', ['www.korea.kr']), 'https://www.korea.kr/briefing/pressReleaseView.do?newsId=123')
        for url in ['javascript:alert(1)', 'https://www.nasa.gov.evil.test/a', 'https://user@www.nasa.gov/a', 'https://www.nasa.gov:8080/a']:
            self.assertIsNone(update.normalize_record(article(url=url), SOURCE, SETTINGS, NOW.date()))

    def test_topic_matching_does_not_match_mars_inside_words(self):
        self.assertIsNone(update.normalize_record(article(title='Marshland climate', summary='Marsh and marshes.'), SOURCE, SETTINGS, NOW.date()))
        source = SETTINGS['sources'][0]
        item = update.normalize_record(article(title='달탐사 궤도설계', summary='', url=source['url']+'/1'), source, SETTINGS, NOW.date())
        self.assertIn('exploration', item['topics'])
        self.assertIn('mission', item['topics'])

    def test_publication_window_and_missing_dates(self):
        for value in ['2026-10-06', '2026-02-30', '2025-10-01', '', None]:
            self.assertIsNone(update.normalize_record(article(date=value), SOURCE, SETTINGS, NOW.date()))

    def test_exclusions_and_no_script_content(self):
        self.assertIsNone(update.normalize_record(article(title='Astronaut to join NFL fans in Philadelphia'), SOURCE, SETTINGS, NOW.date()))
        self.assertIsNone(update.normalize_record(article(url='https://www.nasa.gov/earth-observatory/moon/'), SOURCE, SETTINGS, NOW.date()))
        item = update.normalize_record(article(title='<b>Lunar lander</b><script>evil()</script>'), SOURCE, SETTINGS, NOW.date())
        self.assertEqual(item['title'], 'Lunar lander')
        self.assertNotIn('summary', item)

    def test_deduplicate_urls_and_syndicated_titles(self):
        first = update.normalize_record(article(), SOURCE, SETTINGS, NOW.date())
        copies = [first, {**first, 'title': 'Old lunar guidance title'}, {**first, 'url': 'https://www.nasa.gov/other/'}]
        self.assertEqual(update.newest_unique(copies), [first])

    def test_partial_failure_preserves_only_recent_cached_items(self):
        settings = copy.deepcopy(SETTINGS)
        settings['sources'] = [SOURCE, {**SOURCE, 'id': 'other', 'name': 'Other'}]
        cached = update.normalize_record(article(), SOURCE, SETTINGS, NOW.date())
        previous = {'sources': [{'id': 'other', 'last_success_at': '2026-10-01T09:00:00+09:00', 'items': [cached, {**cached, 'date': '2025-10-01', 'url': 'https://www.nasa.gov/old/'}]}]}
        def fetch(source):
            if source['id'] == 'other': raise RuntimeError('offline')
            return [article(title='Mars rover test', url='https://www.nasa.gov/new/')]
        snapshot, warnings = update.refresh(settings, previous, NOW, fetch)
        self.assertTrue(snapshot['partial'])
        self.assertEqual(len(warnings), 1)
        self.assertEqual(len(snapshot['sources'][1]['items']), 1)
        self.assertTrue(snapshot['sources'][1]['items'][0]['stale'])
        self.assertEqual(snapshot['sources'][1]['last_success_at'], '2026-10-01T09:00:00+09:00')
        self.assertEqual(snapshot['updated_at'], '2026-10-05T10:47:00+09:00')

    def test_short_feeds_retain_previous_news_and_apply_new_exclusions(self):
        settings = copy.deepcopy(SETTINGS)
        settings['sources'] = [SOURCE]
        cached = update.normalize_record(article(), SOURCE, SETTINGS, NOW.date())
        previous = {'sources': [{'id': SOURCE['id'], 'items': [cached]}]}
        def fetch(_): return [article(title='Mars rover test', url='https://www.nasa.gov/new/')]
        snapshot, _ = update.refresh(settings, previous, NOW, fetch)
        self.assertEqual(len(snapshot['items']), 2)
        settings['excluded_urls'] = [cached['url']]
        snapshot, _ = update.refresh(settings, previous, NOW, fetch)
        self.assertEqual(len(snapshot['items']), 1)

    def test_all_failures_leave_output_file_unchanged(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / 'snapshot.json'
            output.write_text('{"sources": []}\n')
            original = output.read_bytes()
            with patch('sys.argv', ['update.py', '--output', str(output)]), patch.object(update, 'fetch_source'):
                # main's refresh is replaced only to simulate total network outage.
                with patch.object(update, 'refresh', side_effect=RuntimeError('all sources offline')):
                    self.assertEqual(update.main(), 1)
            self.assertEqual(output.read_bytes(), original)

    def test_all_sources_fail_raises(self):
        def fail(_): raise RuntimeError('offline')
        with self.assertRaisesRegex(RuntimeError, 'All news sources failed'):
            update.refresh(SETTINGS, {}, NOW, fail)

    def test_bounded_board_pagination(self):
        urls = []
        def request(url):
            urls.append(url)
            return b'<div class="notice_list"><li><p class="subject"><a href="/kor/article/1">Lunar test</a></p><p class="date">2026-10-01</p></li></div>'
        update.fetch_source(SETTINGS['sources'][0], request)
        self.assertEqual(len(urls), 3)
        self.assertTrue(urls[-1].endswith('?pageIndex=3'))


if __name__ == '__main__':
    unittest.main()
