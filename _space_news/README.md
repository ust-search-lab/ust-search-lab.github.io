# Space News

A separate official-news feed for `/space-news/` and `/en/space-news/`.
Home shows the three newest Korean-source items and three newest international
items. The existing News posts remain lab announcements; Research Radar remains
journal metadata. Titles retain their original language on both site languages.
No API keys, subscriptions, runtime translation or browser feed requests are used.

The domestic heading also links to a Korean Google News search for space
exploration, lunar exploration, Danuri, constellations, CubeSats and deep space,
limited to the last 30 days. `google_news_search_url` in the settings controls
this link. It opens Google News; those results are not collected or republished
in the site's automatic list. On 2026-10-05, the Google News RSS response's
`copyright` field explicitly limited the feed to personal, non-commercial feed
readers. The public lab website therefore uses a search link rather than that
feed. The checked endpoint was `https://news.google.com/rss/search` with the
same `q`, `hl=ko`, `gl=KR`, and `ceid=KR:ko` parameters as the search link.

## Sources

- KARI: [official press releases](https://www.kari.re.kr/kor/article/ATCL87374b48c), first three list pages.
- KASA: [official releases republished by Korea Policy Briefing](https://www.korea.kr/briefing/pressReleaseList.do?repCode=B00026), first three list pages. Records must identify the publishing agency as `우주항공청`. KASA's direct website blocked automated requests during setup; this government source carries the same official releases. Policy Briefing discontinued RSS on 2026-07-01, so this integration reads public list metadata, not the discontinued RSS endpoint.
- NASA: recent content, technology and Artemis feeds from the [official RSS directory](https://www.nasa.gov/rss-feeds/).
- NASA/JPL: the NASA-hosted JPL feed listed in the same directory. The separate JPL feed failed during setup.
- ESA: science, engineering/technology and operations feeds from the [official RSS directory](https://www.esa.int/Services/RSS_Feeds).
- JAXA: [official press-release RDF feed](https://global.jaxa.jp/rss/press.rdf), linked from its [media page](https://global.jaxa.jp/media.html).

Sources and matching rules live in `_data/space-news-settings.json`. Only titles,
published dates, official article URLs, source identifiers, region/language and
topic tags are saved. Feed descriptions and government list excerpts are used
for matching in memory; article bodies and publisher images are not stored.

## Collection and recovery

- Collect from bounded latest lists, retain matching items within 90 days, and
  cap each source at 12 items. This does **not** promise complete 90-day coverage:
  RSS feeds expose limited history, and the two domestic lists use three pages.
- Use publication dates, not feed modification timestamps. Missing, invalid,
  future-dated and expired records are excluded. Article dates keep the source's
  calendar date; collection timestamps use Asia/Seoul.
- Match normalized English phrases with word boundaries, and Korean phrases
  without requiring word endings/spaces. Ignore configured promotional topics
  and irrelevant URL paths. Matching is automatic relevance screening, not an
  editorial endorsement or a guarantee of relevance.
- Deduplicate canonical URLs and identical normalized titles, including
  syndicated copies. Different reports of the same event can remain.
- Preserve recent previously collected items when short RSS lists roll over.
  Apply `excluded_urls`, excluded title phrases and URL paths to cached items
  too. Use canonical article links in `excluded_urls` for manual removal.
- Refresh six sources concurrently, with bounded sequential pagination within
  each source. Curl verifies TLS, bounds response size/time and retries once.
- If any feed/page for a source fails, keep that source's last recent items and
  original success timestamp, mark it delayed, and update the other sources.
  If all sources fail, exit nonzero without modifying the snapshot. Writes are
  atomic. The browser also flags a snapshot older than 36 hours; it sends no
  request to news sources. Source details show individual retrieval times.
- Never manually edit `_data/space-news.json`, the generated snapshot.

## Local validation

Python 3.11+, curl and Beautiful Soup are required. Use a virtual environment:

```sh
python3 -m venv /tmp/search-space-news-venv
/tmp/search-space-news-venv/bin/python -m pip install -r _space_news/requirements.txt
/tmp/search-space-news-venv/bin/python -m unittest discover -s _space_news -p 'test_*.py'
/tmp/search-space-news-venv/bin/python _space_news/update.py
bundle exec jekyll build
```

Parser tests cover RSS/RDF/Atom, domestic list markup, agency verification,
publication dates, URL allowlists, keyword boundaries, safe text, duplicates,
retention, exclusions, pagination and partial/total source failures. `_space_news`
is excluded from the built website.

## Scheduled updates

After this change is pushed to `main`, `.github/workflows/update-space-news.yaml`
runs at **10:47 and 22:47 KST** (`47 1,13 * * *` UTC). GitHub may delay scheduled
runs. It can also be started with **Run workflow**. It tests, collects, commits
only `_data/space-news.json`, rebases onto current `main`, pushes, then explicitly
calls the existing `build-site` workflow because `GITHUB_TOKEN` commits do not
trigger `on-push`. Deployment shares the site's existing concurrency group.

UI: `_includes/space-news.html`, `_data/space-news-ui.yaml`,
`_styles/space-news.scss`, `_scripts/space-news.js`. The list is linked from both
home pages and the two News pages, with News highlighted as its parent menu.
